# uv Migration & Pythonic Modernization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate arbitrary-binary-wav from Poetry to uv, replace click with argparse, register a proper CLI entry point, and add ruff linting.

**Architecture:** Single flat module `arbitrary_binary_wav.py` with a `main()` entry point and a pure `output_wave()` helper. No package directory needed. `pyproject.toml` is fully rewritten for uv + hatchling.

**Tech Stack:** Python >=3.11, uv, hatchling, ruff, numpy, scipy, argparse (stdlib), wave (stdlib)

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `arbitrary_binary_wav.py` | Create (rename from `convert.py`) | CLI entry point + WAV conversion logic |
| `pyproject.toml` | Rewrite | Project metadata, deps, entry point, ruff config |
| `uv.lock` | Generate | Locked dependency graph (created by `uv sync`) |
| `README.md` | Modify | Update install/usage instructions |
| `convert.py` | Delete | Replaced by `arbitrary_binary_wav.py` |
| `poetry.lock` | Delete | Replaced by `uv.lock` |

---

### Task 1: Rewrite pyproject.toml

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Overwrite pyproject.toml**

Replace the entire file contents with:

```toml
[project]
name = "arbitrary-binary-wav"
version = "0.1.0"
description = "Convert arbitrary binary data to wav"
authors = [{name = "Abe Hmiel"}]
license = {text = "MIT"}
requires-python = ">=3.11"
dependencies = [
    "scipy>=1",
    "numpy>=1",
]

[project.scripts]
arbitrary-binary-wav = "arbitrary_binary_wav:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
```

- [ ] **Step 2: Delete poetry.lock**

```bash
rm poetry.lock
```

- [ ] **Step 3: Run uv sync to generate lockfile**

```bash
uv sync
```

Expected: uv resolves deps, writes `uv.lock`, creates `.venv/`. No errors.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git rm poetry.lock
git add uv.lock
git commit -m "chore: migrate from poetry to uv, drop click dep"
```

---

### Task 2: Create arbitrary_binary_wav.py

**Files:**
- Create: `arbitrary_binary_wav.py`
- Delete: `convert.py`

- [ ] **Step 1: Create arbitrary_binary_wav.py**

```python
import argparse
import wave
from io import BytesIO

from numpy import fromfile, int16
from scipy.io.wavfile import write


def output_wave(path, frames, rate):
    bytes_wav = bytes()
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
```

- [ ] **Step 2: Delete convert.py**

```bash
git rm convert.py
```

- [ ] **Step 3: Run ruff to verify no lint errors**

```bash
uv run ruff check arbitrary_binary_wav.py
```

Expected: no output (clean).

- [ ] **Step 4: Smoke test the CLI**

```bash
uv run arbitrary-binary-wav --input_file arbitrary_binary_wav.py --output_file /tmp/test.wav
```

Expected: exits with no error, `/tmp/test.wav` exists and is a valid WAV file. You can verify with:

```bash
file /tmp/test.wav
```

Expected output contains: `RIFF (little-endian) data, WAVE audio`

- [ ] **Step 5: Commit**

```bash
git add arbitrary_binary_wav.py
git commit -m "feat: rename to module, replace click with argparse, fix wave context manager"
```

---

### Task 3: Update README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update Installation section**

Replace:
```
## Installation:

- Get poetry https://python-poetry.org/docs/#installation

- Install dependencies from the lockfile using: `poetry install`
```

With:
```
## Installation:

- Get uv https://docs.astral.sh/uv/getting-started/installation/

- Install dependencies from the lockfile using: `uv sync`
```

- [ ] **Step 2: Update Usage section**

Replace:
````
```
poetry run python convert.py \
--input_file='/path/to/input/file.pdf' \
--output_file='/path/to/output/file.wav' \
--rate=44100
```
````

With:
````
```
uv run arbitrary-binary-wav \
  --input_file /path/to/input/file.pdf \
  --output_file /path/to/output/file.wav \
  --rate 44100
```
````

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: update README for uv and new entry point"
```
