# Interactive Figure

Create interactive Matplotlib figures that can be used for simple reaction time experiments. This package serves as a simple playground for students to perform such experiments. For more accurate scientific analysis one should refer to [PsychoPy](https://www.psychopy.org/).

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

A quick example can be found in demo/basic.py.

### Functionality

- Create
- Fullscreen
- Clear
- Wait
- Wait for interaction (optionally timeout)
- Draw
- Close