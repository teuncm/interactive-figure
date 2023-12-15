# Interactive Figure

This package serves for students to learn the basics of Python, Matplotlib and setting up reaction time experiments (visual search task, Stroop task, etc.). For a more accurate timing environment one should refer to e.g. [PsychoPy](https://www.psychopy.org/).

This is currently used at the University of Amsterdam (UvA) in the course *Introduction to Python Programming for Neuroscientists*.

Package created using [Hatch](https://hatch.pypa.io).

## Installation

```shell
pip install interactive-figure
```

## Usage

```python
from interactive_figure import interactive_figure

interactive_figure.create()
# Stall until user input is received.
interactive_figure.wait_for_interaction()
key = interactive_figure.get_last_keypress()
print(f"Pressed key: {key}")
interactive_figure.close()
```

Demos can be found in the *demo* folder on GitHub.

## Functionality

#### User interaction
- Capture key presses, button presses and mouse location

#### Figure control
- Create
- Toggle fullscreen
- Clear
- Wait
- Wait for interaction (optionally timeout)
- Draw
- Close

## Limitations

- Waiting for user input will not work in Jupyter Notebooks and the interactive interpreter due to the way Matplotlib handles events.
- Automated testing is hard since tests should cover multiple backends (macosx, QtAgg, Tkgg) on multiple platforms (Windows, macOS, Linux). Tips are very welcome!

## Links

- [GitHub](https://github.com/teuncm/interactive-figure)
- [PyPI](https://pypi.org/project/interactive-figure/)
- [Documentation](https://teuncm.github.io/interactive-figure/autoapi/interactive_figure/interactive_figure/index.html)