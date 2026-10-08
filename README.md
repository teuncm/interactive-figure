# Interactive Figure

This package serves for students to learn the basics of Python, Matplotlib and setting up reaction time experiments (visual search task, Stroop task, etc.). For a more accurate timing environment one should refer to e.g. [PsychoPy](https://www.psychopy.org/).

This is currently used at the University of Amsterdam (UvA) in the courses *Introduction to Python Programming for Neuroscientists* and *Experimentatie - Inleiding Programmeren*.

Development and packaging are managed with [uv](https://docs.astral.sh/uv/).

## Installation

```shell
pip install interactive-figure
```

## Usage

```python
import interactive_figure as ifig

ifig.create()
# Wait until user input is received.
ifig.wait_for_interaction()
key = ifig.get_last_key_press()
print(f"Pressed key: {key}")
ifig.close()
```

Demos can be found in the *demo* folder on GitHub.

## Limitations

- Waiting for user input will not work in Jupyter Notebooks and the interactive interpreter due to the way Matplotlib handles events.
- Automated testing is hard since tests should cover multiple backends (macosx, QtAgg, Tkgg) on multiple platforms (Windows, macOS, Linux). Tips are very welcome!

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and use Python 3.11 or newer.

```bash
# Create the project environment and install development tools.
uv sync

# Run a demo (requires a graphical desktop).
uv run python demo/usage.py

# Check formatting, lint, and types.
uv run black --check --diff .
uv run ruff check .
uv run mypy src/interactive_figure

# Format and fix lint issues.
uv run black .
uv run ruff check --fix .

# Build documentation with the docs dependency group.
./generate_docs.sh

# Set the next release version in pyproject.toml.
uv version 0.6.0

# Build a wheel and source distribution.
uv build

# Publish this release to PyPI using a PyPI API token.
# Set UV_PUBLISH_TOKEN in your environment before running this command.
uv publish dist/interactive_figure-0.6.0*
```

The package version is maintained in `pyproject.toml`. Commit `uv.lock` to keep development dependencies reproducible. There is currently no automated test suite; use the demos to check GUI behavior.

## Links

- [GitHub](https://github.com/teuncm/interactive-figure)
- [PyPI](https://pypi.org/project/interactive-figure/)
- [Documentation](https://teuncm.github.io/interactive-figure/autoapi/interactive_figure/interactive_figure/index.html)
