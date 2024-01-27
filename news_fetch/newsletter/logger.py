import os
import logging
import threading
from enum import Enum
import logging.handlers
from dataclasses import dataclass

class LogLevel(Enum):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    CRITICAL = logging.CRITICAL

@dataclass
class CustomLogger:
    log_level: LogLevel

    def __post_init__(self):
        self.calling_module = str(os.getcwd()).rsplit("\\")[-1]
        self.log_dir = self.setup_logger_directory()
        self.setup_logger()
        self.log_lock = threading.Lock()

    def setup_logger_directory(self):
        folder_name = f"logs_{self.calling_module.lower()}"
        log_dir = os.path.join(os.getcwd(), folder_name)
        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)

        if self.log_level not in LogLevel:
            self.log_level = LogLevel.INFO

        self.logger.setLevel(self.log_level.value)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')

        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, f'{self.calling_module}.log'),
            maxBytes=5 * 1024 * 1024,
            backupCount=1
        )
        file_handler.setLevel(self.log_level.value)
        file_handler.setFormatter(formatter)
        file_handler.createLock()

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level.value)
        console_handler.setFormatter(formatter)
        console_handler.createLock()

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        with self.log_lock:
            self.logger.info(message)

    def error(self, message):
        with self.log_lock:
            self.logger.error(message)

    def critical(self, message):
        with self.log_lock:
            self.logger.critical(message)

    def exception(self, message):
        with self.log_lock:
            self.logger.exception(message)

    def __reduce__(self):
        return (self.__class__, (self.log_level,))
