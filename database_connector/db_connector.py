#!/usr/bin/python3.11

__created__ = "06.11.2023"
__last_update__ = "06.11.2023"
__author__ = "https://github.com/pyautoml"


import sys
import argparse
from typing import Any
from dataclasses import dataclass
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine, text
from utils import get_configuration_path, load_json_data, cmd_arguments
# from logger import logger


class AbstractConnector(ABC):
    @abstractmethod
    def _connect(self) -> None:
        pass

    @abstractmethod
    def _disconnect(self) -> None:
        pass

    @abstractmethod
    def _execute_query(self, query: str) -> None:
        pass

    @abstractmethod
    def _update(self, session, model_class, data, condition) -> None:
        pass

    @abstractmethod
    def _insert(self, session: Session, model_class, data) -> None:
        pass


@dataclass
class MsSQLConnector(AbstractConnector):
    args: argparse
    settings_path: str

    def __post_init__(self) -> None:
        print("args: ", self.args)
        self._configuration = self.settings_path
        self._ssh_host = self._configuration["ssh"]["ssh_host"]
        self._ssh_port = self._configuration["ssh"]["ssh_port"]
        self._ssh_user = self._configuration["ssh"]["ssh_user"]
        self._remote_db_port = self._configuration["ssh"]["remote_port"]
        self._remote_db_host = self._configuration["ssh"]["remote_db_host"]
        self._remote_db_user = self._configuration["ssh"]["remote_db_user"]
        self._database_dev = self._configuration["database"]["dev"]["db_name"]
        self._private_key_path = self._configuration["ssh"]["private_key_path"]
        self._database_test = self._configuration["database"]["test"]["db_name"]
        self._database_prod = self._configuration["database"]["prod"]["db_name"]
        self._remote_db_password = self._configuration["ssh"]["remote_db_password"]
        self._local_db_password = self._configuration["ssh"]["remote_user_password"]

    def _connect(self) -> None:
        try:
            if self.args.database == "d":
                selected_database = self._database_dev
            elif self.args.database == "t":
                selected_database = self._database_test
            elif self.args.database == "p":
                selected_database = self._database_prod
            else:
                selected_database = self._database_dev

            self._tunnel = SSHTunnelForwarder(
                (self._ssh_host, self._ssh_port),
                ssh_username=self._ssh_user,
                ssh_pkey=self._private_key_path,
                remote_bind_address=(self._remote_db_host, self._remote_db_port),
            )
            self._tunnel.start()
            self._engine = create_engine(
                f"mysql+pymysql://{self._remote_db_user}:{self._remote_db_password}@"
                f"{self._remote_db_host}:{self._tunnel.local_bind_port}/{selected_database}"
            )
        except Exception as e:
            print("Connection error: ", e)
            # logger.critical(f"{e})
            sys.exit(1)

    def _disconnect(self) -> None:
        if self._tunnel:
            self._tunnel.stop()
        if self._engine:
            self._engine.dispose()

    def _execute_query(self, query: str) -> Any:
        if self._engine:
            try:
                with self._engine.connect() as connection:
                    result = connection.execute(text(query))
                    return result
            except Exception as e:
                print("Query execution error: ", e)
                # logger.critical(f"{e})
                sys.exit(1)
        else:
            print("Database connection is not established.")
            # logger.critical(f"{e})
            sys.exit(1)

    def _insert(self, session: Session, model_class, data) -> None:
        if session:
            try:
                record = model_class(**data)
                session.add(record)
                session.commit()
            except Exception as e:
                print("Insert error: ", e)
                session.rollback()
                # logger.critical(f"{e})
                sys.exit(1)
        else:
            print("Database session is not established.")
            # logger.critical(f"{e})
            sys.exit(1)

    def _update(self, session, model_class, data, condition) -> None:
        if session:
            try:
                record = session.query(model_class).filter(condition).first()
                if record:
                    for key, value in data.items():
                        setattr(record, key, value)
                    session.commit()
                else:
                    print("No records match the condition.")
            except Exception as e:
                print("Update error: ", e)
                session.rollback()
                # logger.critical(f"{e})
                sys.exit(1)
        else:
            print("Database session is not established.")
            # logger.critical(f"{e})
            sys.exit(1)

    def _bulk_insert(self, session, model_class, data_list) -> None:
        if session:
            try:
                records = [model_class(**data) for data in data_list]
                session.add_all(records)
                session.commit()
            except Exception as e:
                print("Bulk Insert error: ", e)
                session.rollback()
                # logger.critical(f"{e})
                sys.exit(1)
        else:
            print("Database session is not established.")
            # logger.critical(f"{e})
            sys.exit(1)

    def _bulk_update(self, session, model_class, data_list, condition) -> None:
        if session:
            try:
                records = session.query(model_class).filter(condition).all()
                if records:
                    for record in records:
                        for data in data_list:
                            for key, value in data.items():
                                setattr(record, key, value)
                    session.commit()
                else:
                    print("No records match the condition.")
            except Exception as e:
                print("Bulk Update error: ", e)
                session.rollback()
                # logger.critical(f"{e})
                sys.exit(1)
        else:
            print("Database session is not established.")
            # logger.critical(f"{e})
            sys.exit(1)


# example ---
# args = cmd_arguments()
# connection = MsSQLConnector(args=args, settings_path=load_json_data(f"{get_configuration_path()}\db_connection.json"))
# connection._connect()
# result = connection._execute_query('SELECT * FROM your_db ORDER BY ID DESC LIMIT 10;')
# data = result.fetchall()
# for row in data:
#     print(row)
# connection._disconnect()
