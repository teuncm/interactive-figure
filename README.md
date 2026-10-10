# Interactive Figure

This package helps students learn the basics of Python, Matplotlib and set up reaction time experiments (visual search task, Stroop task, etc.). For a more accurate timing environment refer to e.g. [PsychoPy](https://www.psychopy.org/).

This is currently used at the University of Amsterdam (UvA) in the courses *Introduction to Python Programming for Neuroscientists* and *Experimentatie - Inleiding Programmeren*.

Development and packaging are managed with [uv](https://docs.astral.sh/uv/).

## Installation

Requires Python 3.11 or newer. To add the package to a uv project:

```shell
uv add interactive-figure
```

You can also install it with pip:

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

Each edge of the frame can be hidden independently. For example, to keep only the bottom and left edges:

```python
ifig.create(hide_top_frame=True, hide_right_frame=True)
```

The four options are `hide_top_frame`, `hide_right_frame`, `hide_bottom_frame`, and `hide_left_frame`, all defaulting to `False`. Set all four to `True` to hide the entire frame. Axis labels are controlled separately with `hide_x_labels` and `hide_y_labels`. Frame options are reapplied when `ifig.clear()` is called.

Demos can be found in the *demo* folder on GitHub.

## Limitations

- Waiting for user input will not work in Jupyter Notebooks and the interactive interpreter due to the way Matplotlib handles events. Only a standalone script with an interactive figure correctly captures user input events in an event loop.
- Automated testing is hard since tests should cover multiple backends (macosx, QtAgg, Tkgg) on multiple platforms (Windows, macOS, Linux). Tips are very welcome!

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run these commands from the repository root:

```bash
# Create the project environment and install development tools.
uv sync

# Run a demo (requires a graphical desktop).
uv run python demo/usage.py

# Run the unit tests without opening GUI windows.
uv run pytest

# Check formatting, lint, and types.
uv run black --check --diff .
uv run ruff check .
uv run mypy src/interactive_figure

# Install the docs dependencies and build the HTML documentation.
./generate_docs.sh
# Or run Sphinx directly.
uv run --group docs sphinx-build -b html docs_source docs

# Format and fix lint issues.
uv run black .
uv run ruff check --fix .
```

uv manages the project environment in `.venv`; `uv run` uses it automatically without manual activation. If your shell has another virtual environment activated, run `deactivate` or open a fresh terminal before using uv.

The `dev` dependency group includes the lint tools and pytest from the `test` group. Documentation dependencies are in the separate `docs` group. Commit `uv.lock` to keep development dependencies reproducible.

### Releases

The package version is maintained in `pyproject.toml`, and packages are built with `uv_build`. For example, to release version 0.6.0:

```bash
# Set the next release version.
uv version 0.6.0

# Build a wheel and source distribution.
uv build

# Publish this release to PyPI using a PyPI API token.
# Set UV_PUBLISH_TOKEN in your environment before running this command.
uv publish dist/interactive_figure-0.6.0*
```

Use the chosen release version in the upload filename pattern so only that release's artifacts are published.

## Links

- [GitHub](https://github.com/teuncm/interactive-figure)
- [PyPI](https://pypi.org/project/interactive-figure/)
- [Documentation](https://teuncm.github.io/interactive-figure/autoapi/interactive_figure/interactive_figure/index.html)
