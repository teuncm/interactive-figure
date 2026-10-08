"""
This module provides functions to create and interact with a Matplotlib figure. The figure registers mouse presses,
keyboard input and the location of the mouse after any input.

Source: https://github.com/teuncm/interactive-figure
"""

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import FigureManagerBase, MouseButton
from matplotlib.figure import Figure


def create(
    *,
    hide_x_labels=False,
    hide_y_labels=False,
    hide_frame=False,
    hide_toolbar=False,
    layout="constrained",
    **kwargs,
):
    """Create the interactive figure.

    Parameters
    ----------
    hide_x_labels : bool, optional
        Hide the x-axis labels, default False.
    hide_y_labels : bool, optional
        Hide the y-axis labels, default False.
    hide_frame : bool, optional
        Hide the frame, default False.
    hide_toolbar : bool, optional
        Hide the toolbar, default False.
    layout : str, optional
        The layout mode for the figure, default 'constrained'. See:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html

    Remaining keyword arguments will be sent to the Matplotlib figure.

    Raises
    ----------
    RuntimeError
        if multiple interactive figures are created at the same time.
    """
    if _state.fig is not None:
        raise RuntimeError("multiple interactive figures are not supported")
    else:
        if hide_toolbar:
            plt.rcParams["toolbar"] = "None"

        _state.hide_x_labels = hide_x_labels
        _state.hide_y_labels = hide_y_labels
        _state.hide_frame = hide_frame

        # Disable interactive mode for explicit control over drawing. See:
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.isinteractive.html#matplotlib.pyplot.isinteractive
        plt.ioff()

        _state.fig = fig = plt.figure(layout=layout, **kwargs)
        manager = _get_manager(fig)
        manager.set_window_title("Interactive Figure")
        # Create drawable axis.
        _state.ax = plt.gca()

        # Show figure but allow the main thread to continue.
        plt.show(block=False)

        # Reset plot state and draw to (attempt to) obtain focus.
        clear()
        draw()

        # Add our custom event handlers. For handlers, see:
        # https://matplotlib.org/stable/api/backend_bases_api.html#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        # For general interaction handling, see:
        # https://matplotlib.org/stable/users/explain/figure/interactive_guide.html
        # For mouse buttons, see:
        # https://matplotlib.org/stable/api/backend_bases_api.html#matplotlib.backend_bases.MouseButton
        fig.canvas.mpl_disconnect(manager.key_press_handler_id)
        fig.canvas.mpl_disconnect(manager.button_press_handler_id)
        fig.canvas.mpl_connect("key_press_event", _key_press_handler)
        fig.canvas.mpl_connect("button_press_event", _button_press_handler)
        fig.canvas.mpl_connect("close_event", _close_handler)

        print("created interactive figure")


def draw():
    """Draw contents of the figure."""
    fig, _ = _check_exists()

    canvas = fig.canvas
    # Mark canvas for a draw.
    canvas.draw_idle()
    # Force update the GUI. This is when the drawing actually happens
    # in the backend.
    canvas.flush_events()


def clear():
    """Clear, but don't draw() the figure."""
    _, ax = _check_exists()
    ax.clear()

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Hide axis spines.
    if _state.hide_frame:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

    # Hide axis labels. Setting empty ticks makes drawing faster.
    if _state.hide_x_labels:
        ax.set_xticks([])
    if _state.hide_y_labels:
        ax.set_yticks([])


def toggle_fullscreen():
    """Toggle fullscreen on/off."""
    fig, _ = _check_exists()

    _get_manager(fig).full_screen_toggle()


def close():
    """Close the figure."""
    fig, _ = _check_exists()

    _state.external_close = False
    plt.close(fig)

    # Handle proper closure so that the figure can be reused.
    _state.reset_fig()
    _state.reset_press()


def wait_for_interaction(timeout=-1):
    """Wait for interaction.

    Optionally use a timeout in seconds.

    Parameters
    ----------
    timeout : int, optional
        Timeout in seconds when waiting for input.

    Returns
    -------
    bool | None
        - True if a key was pressed.
        - False if a mouse button was pressed.
        - None if no input was given within the timeout.
    """
    fig, _ = _check_exists()
    canvas = fig.canvas

    # Reimplementation of:
    # figure.Figure.waitforbuttonpress()
    # _blocking_input.blocking_input_loop()
    #     but without show() to prevent redrawing the figure.

    # Contains the event that was registered.
    event = None

    # Handler to stop blocking event loop.
    def simple_handler(ev):
        nonlocal event
        event = ev
        canvas.stop_event_loop()

    # Connect event handlers and save callback ids.
    callback_ids = [
        canvas.mpl_connect(name, simple_handler)
        for name in ["button_press_event", "key_press_event"]
    ]
    try:
        # Start a blocking event loop.
        canvas.start_event_loop(timeout=timeout)
    finally:
        # Disconnect handlers.
        for callback_id in callback_ids:
            canvas.mpl_disconnect(callback_id)

    interaction_type = None if event is None else event.name == "key_press_event"

    if interaction_type is None:
        # No button was pressed, so reset the press state.
        _state.reset_press()

    return interaction_type


def get_last_key_press():
    """Get the last key press in lowercase.

    Returns
    -------
    str | None
        The last key that was pressed.
    """
    _check_exists()

    key_string = _state.last_keypress

    if key_string is None:
        return None
    else:
        return key_string.lower()


def get_last_mouse_press():
    """Get the ID of the last mouse press.

    Returns
    -------
    int | None
        The identifier of the last mouse button that was pressed.
    """
    _check_exists()

    mouse_button = _state.last_mousepress

    if mouse_button is None:
        return None
    else:
        return mouse_button.value


def get_last_mouse_pos():
    """Get the last mouse position.

    Returns
    -------
    (x: float, y: float) | (None, None)
        The last registered mouse position after any interaction.
    """
    _check_exists()

    return (_state.last_mouse_x, _state.last_mouse_y)


def wait(timeout):
    """Freeze for the given number of seconds.

    During this period it is not possible to interact
    with the figure. For sub-second timeouts use time.wait() instead.

    Parameters
    ----------
    timeout : float
        Number of seconds to wait for.
    """
    fig, _ = _check_exists()

    fig.canvas.start_event_loop(timeout=timeout)
    # Reset the press state.
    _state.reset_press()


#
# PRIVATE METHODS
#


def _check_exists() -> tuple[Figure, Axes]:
    """Return the figure and axes if the interactive figure exists.

    Raises
    ------
    RuntimeError
        If the figure is not available
    """
    fig, ax = _state.fig, _state.ax
    if fig is None or ax is None:
        raise RuntimeError("interactive figure must be created first")
    return fig, ax


def _get_manager(fig: Figure) -> FigureManagerBase:
    """Return the figure manager, accounting for incomplete canvas type hints."""
    manager = getattr(fig.canvas, "manager", None)
    if not isinstance(manager, FigureManagerBase):
        raise RuntimeError("interactive figure must have a figure manager")
    return manager


def _key_press_handler(event):
    """Register key and mouse coordinates on press.

    Parameters
    ----------
    event
        The event object that was generated internally
    """
    _state.last_keypress = event.key
    # Mouse press data is not provided for key press event.
    _state.last_mousepress = None
    _state.last_mouse_x = event.xdata
    _state.last_mouse_y = event.ydata


def _button_press_handler(event):
    """Register key, mouse button and mouse coordinates on press.

    Parameters
    ----------
    event
        The event object that was generated internally
    """
    _state.last_keypress = event.key
    _state.last_mousepress = event.button
    _state.last_mouse_x = event.xdata
    _state.last_mouse_y = event.ydata


def _close_handler(_):
    """Exit when the user presses the red x to close the figure
    to prevent an infinite event loop.

    Parameters
    ----------
    _
        The event object that was generated internally
    """
    # Prevent infinite closing loop on MacOS.
    if _state.closing:
        return

    # Triggered if an external figure close is triggered.
    if _state.external_close:
        print("manually closed interactive figure and automatically exited script")
        _state.closing = True

        raise SystemExit()
    else:
        print("closed interactive figure")


@dataclass
class _State:
    """Track the figure, display options, and last registered interaction."""

    fig: Figure | None = None
    ax: Axes | None = None
    hide_x_labels: bool = False
    hide_y_labels: bool = False
    hide_frame: bool = False
    external_close: bool = True
    closing: bool = False
    last_keypress: str | None = None
    last_mousepress: MouseButton | None = None
    last_mouse_x: float | None = None
    last_mouse_y: float | None = None

    def reset_fig(self):
        """Reset figure information and display options."""
        self.fig = None
        self.ax = None
        self.hide_x_labels = False
        self.hide_y_labels = False
        self.hide_frame = False
        self.external_close = True
        self.closing = False

    def reset_press(self):
        """Reset last registered press information."""
        self.last_keypress = None
        self.last_mousepress = None
        self.last_mouse_x = None
        self.last_mouse_y = None


# Track the state of the interactive figure.
_state = _State()
