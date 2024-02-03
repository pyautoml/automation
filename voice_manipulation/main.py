import os
import sys
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


def universal_path(file: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), file))


def save_audio_spectrum_plot(mp3_file_path, output_image_path):
    y, sr = librosa.load(mp3_file_path)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="linear")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram of the Audio")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")

    plt.savefig(output_image_path)
    plt.close()


def butter_highpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    return butter(order, normal_cutoff, btype="high", analog=False)


def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    return lfilter(b, a, data)


def apply_highpass_and_volume(
    audio, sr, parts_from_to, highpass_params, volume_changes
):
    modified_audio = np.copy(audio)

    for (start, end), highpass_cutoff, volume_change in zip(
        parts_from_to, highpass_params, volume_changes
    ):
        start_frame = int(start * sr)
        end_frame = int(end * sr)
        y_filtered = highpass_filter(
            modified_audio[start_frame:end_frame], highpass_cutoff, sr
        )
        modified_audio[start_frame:end_frame] = y_filtered
        modified_audio[start_frame:end_frame] *= 10 ** (volume_change / 20.0)

    return modified_audio


def modify_volume(
    audio_file,
    parts_from_to,
    highpass_cutoffs,
    volume_changes,
    new_file_name: str = "./audio/modified_audio.mp3",
):
    try:
        y, sr = librosa.load(audio_file, sr=None)
    except Exception as e:
        print(f"{[ERROR] Missing audio file: {e}")
        sys.exit(1)
        
    modified_audio = apply_highpass_and_volume(
        y, sr, parts_from_to, highpass_cutoffs, volume_changes
    )
    
    sf.write(universal_path(new_file_name), modified_audio, sr)


def main():
    audio_file = universal_path("./audio/audio.mp3")

    parts_from_to = [[1, 5], [6.7, 12], [13, 20], [22, 30], [32, 40]]
    highpass_cutoffs = [200, 10, 10, 10, 10]
    volume_changes = [0, 0, 0, 20, -5]

    modify_volume(
        audio_file,
        parts_from_to,
        highpass_cutoffs,
        volume_changes,
        "./audio/modified_audio.mp3",
    )
    save_audio_spectrum_plot(audio_file, "./spectrogram/audio_mel_spectrogram.png")
    save_audio_spectrum_plot(
        universal_path("./audio/modified_audio.mp3"),
        "./spectrogram/audio_modified_mel_spectrogram.png",
    )


if __name__ == "__main__":
    main()
