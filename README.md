# Interactive Figure

This package serves for students to learn about basic reaction time experiments (visual search task, Stroop task, etc.). For a more accurate timing environment one should refer to e.g. [PsychoPy](https://www.psychopy.org/).

Most functionality only works correctly in standalone scripts, not in notebooks.

Created using [Hatch](https://hatch.pypa.io).

### Installation

```shell
pip install interactive-figure
```

### Usage

```python
from interactive_figure import interactive_figure

interactive_figure.create()
# Stall until user input is received.
interactive_figure.wait_for_interaction()
interactive_figure.close()
```

A demo using timing can be found in *demo/basic.py*.

### Functionality

User interaction:
- Capture key presses, button presses and mouse location

Figure control:
- Create
- Toggle fullscreen
- Clear
- Wait
- Wait for interaction (optionally timeout)
- Draw
- Close

### Links

- [GitHub](https://github.com/teuncm/interactive-figure)
- [PyPI](https://pypi.org/project/interactive-figure/)