#!/usr/bin/env python3

# https://gist.github.com/rudolfbyker/8fc0d99ecadad0204813d97fee2c6c06

# What about https://stackoverflow.com/questions/35817013/is-it-possible-to-find-silence-in-audio-file-using-python

from scipy.io import wavfile
import os
import numpy as np
import argparse
from tqdm import tqdm

# Utility functions
def windows(signal, window_size, step_size):
    if type(window_size) is not int:
        raise AttributeError("Window size must be an integer.")
    if type(step_size) is not int:
        raise AttributeError("Step size must be an integer.")
    for i_start in range(0, len(signal), step_size):
        i_end = i_start + window_size
        if i_end >= len(signal):
            break
        yield signal[i_start:i_end]


def energy(samples):
    return np.sum(np.power(samples, 2.)) / float(len(samples))


def rising_edges(binary_signal):
    previous_value = 0
    index = 0
    for x in binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1


def main():
    # Process command line arguments
    parser = argparse.ArgumentParser(description='Split a WAV file at silence.')
    parser.add_argument('input_file', type=str, help='The WAV file to split.')
    parser.add_argument('--output-dir', '-o', type=str, default='.', help='The output folder. Defaults to the current folder.')
    parser.add_argument('--min-silence-length', '-m', type=float, default=3., help='The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.')
    parser.add_argument('--silence-threshold', '-t', type=float, default=1e-6, help='The energy level (between 0.0 and 1.0) below which the signal is regarded as silent. Defaults to 1e-6 == 0.0001%.')
    parser.add_argument('--step-duration', '-s', type=float, default=None, help='The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Don\'t actually write any output files.')

    args = parser.parse_args()

    # FIXME make dict compatible with parser args
    my_args = dict(defaults)
    my_args['input_file'] = args.input_file

    my_args['output_dir'] = args.output_dir
    my_args['min_silence_length'] = args.min_silence_length
    my_args['silence_threshold'] = args.silence_threshold
    my_args['step_duration'] = args.step_duration
    my_args['dry_run'] = args.dry_run

    process(my_args)


defaults = {
    'output_dir': '.',
    'min_silence_length': 3.,
    'silence_threshold': 1e-6,
    'step_duration': None,
    'dry_run': False
}


def split(input_file, args):
    my_args = dict(args)
    my_args['input_file'] = input_file
    process(my_args)


def process(args):
    input_filename = args['input_file']
    window_duration = args['min_silence_length']
    if args['step_duration'] is None:
        step_duration = window_duration / 10.
    else:
        step_duration = args['step_duration']
    silence_threshold = args['silence_threshold']
    output_dir = args['output_dir']
    output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]
    dry_run = args['dry_run']

    print("Splitting {} where energy is below {}% for longer than {}s.".format(
        input_filename,
        silence_threshold * 100.,
        window_duration
    ))

    # Read and split the file

    sample_rate, samples = input_data=wavfile.read(filename=input_filename, mmap=True)

    max_amplitude = np.iinfo(samples.dtype).max
    max_energy = energy([max_amplitude])

    window_size = int(window_duration * sample_rate)
    step_size = int(step_duration * sample_rate)

    signal_windows = windows(
        signal=samples,
        window_size=window_size,
        step_size=step_size
    )

    window_energy = (energy(w) / max_energy for w in tqdm(
        signal_windows,
        total=int(len(samples) / float(step_size))
    ))

    window_silence = (e > silence_threshold for e in window_energy)

    cut_times = (r * step_duration for r in rising_edges(window_silence))

    # This is the step that takes long, since we force the generators to run.
    print ("Finding silences...")
    cut_samples = [int(t * sample_rate) for t in cut_times]
    cut_samples.append(-1)

    cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in range(len(cut_samples) - 1)]

    for i, start, stop in tqdm(cut_ranges):
        output_file_path = "{}_{:03d}.wav".format(
            os.path.join(output_dir, output_filename_prefix),
            i
        )
        if not dry_run:
            print("Writing file {}".format(output_file_path))
            wavfile.write(
                filename=output_file_path,
                rate=sample_rate,
                data=samples[start:stop]
            )
        else:
            print( "Not writing file {}".format(output_file_path))


if __name__ == '__main__':
    main()
