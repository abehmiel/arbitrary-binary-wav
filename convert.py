#!/bin/python3
import wave
import click
from io import BytesIO
from os import stat
from numpy import fromfile, int16
from scipy.io.wavfile import write


@click.command()
@click.option('--input_file')
@click.option('--output_file')
@click.option('--rate', default=44100)
def output_sound(input_file, output_file, rate):

    size = stat(input_file).st_size

    with open(input_file, 'rb') as file_data:
        frames = fromfile(file_data, dtype=int16, count=-1)
        output_wave(output_file, frames, rate)


def output_wave(path, frames, rate):

    bytes_wav = bytes()
    byte_io = BytesIO(bytes_wav)
    write(byte_io, rate, frames)
    output_wav = byte_io.read()

    output = wave.open(path,'wb')
    output.setparams((2, 2, rate, 0, 'NONE', 'not compressed'))
    output.writeframes(output_wav)
    output.close()

if __name__ == '__main__':
    output_sound()
