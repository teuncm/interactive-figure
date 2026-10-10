"""
This package contains functions to create and interact with a modified Matplotlib figure.
The figure registers mouse presses, keyboard input and the location of the mouse after any input.

Source: https://github.com/teuncm/interactive-figure
"""

from interactive_figure.interactive_figure import (
    _state as state,
)
from interactive_figure.interactive_figure import (
    clear,
    close,
    create,
    draw,
    get_last_key_press,
    get_last_mouse_pos,
    get_last_mouse_press,
    toggle_fullscreen,
    wait,
    wait_for_interaction,
)

__all__ = [
    "clear",
    "close",
    "create",
    "draw",
    "get_last_key_press",
    "get_last_mouse_pos",
    "get_last_mouse_press",
    "state",
    "toggle_fullscreen",
    "wait",
    "wait_for_interaction",
]
