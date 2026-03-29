import argparse
import wave
from io import BytesIO

from numpy import fromfile, int16
from scipy.io.wavfile import write


def output_wave(path, frames, rate):
    bytes_wav = b""
    byte_io = BytesIO(bytes_wav)
    write(byte_io, rate, frames)
    output_wav = byte_io.read()

    with wave.open(path, "wb") as output:
        output.setparams((2, 2, rate, 0, "NONE", "not compressed"))
        output.writeframes(output_wav)


def main():
    parser = argparse.ArgumentParser(
        description="Convert arbitrary binary data to a wav file."
    )
    parser.add_argument("--input_file", required=True, help="Path to input binary file")
    parser.add_argument("--output_file", required=True, help="Path to output wav file")
    parser.add_argument(
        "--rate", type=int, default=44100, help="Sample rate in Hz (default: 44100)"
    )
    args = parser.parse_args()

    with open(args.input_file, "rb") as file_data:
        frames = fromfile(file_data, dtype=int16, count=-1)
        output_wave(args.output_file, frames, args.rate)


if __name__ == "__main__":
    main()
