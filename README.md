# arbitrary-binary-wav
Create wav files from arbitrary binary data on your filesystem with Python

## Installation:

- Get poetry https://python-poetry.org/docs/#installation

- Install dependencies from the lockfile using: `poetry install`

## Usage:

```poetry run python convert.py \
--input_file='/path/to/input/file.pdf' \
--output_file='/path/to/output/file.wav'```

You ought to be able to convert any file (up to about 6.5 Gb) to wav specification.

File sizes from 1 Mb to 50 Mb probably work best, as they're very fast to convert and are of a good
length to use in musical compositions.

Fair warning, you're probably gonna get something close to white noise! Maybe! I dunno! Prove me wrong!
