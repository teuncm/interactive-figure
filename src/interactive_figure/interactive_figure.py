"""
Author: Teun Mathijssen

Source: https://github.com/teuncm/interactive-figure

This module provides functions to create and interact with a Matplotlib figure.

The figure registers mouse presses, keyboard input and the location of the mouse
after any input. The user has fine-grained control over when to wait for input
and when to draw the contents of the figure.
"""

import matplotlib.pyplot as plt
from types import SimpleNamespace


def create(aspect_ratio="auto", hide_toolbar=False, **kwargs):
    """Create the interactive figure.

    Parameters
    ----------
    aspect_ratio : str, optional
        aspect ratio of the Axes, by default "auto"
    hide_toolbar : bool, optional
        whether to hide the toolbar, by default False
  
    remaining arguments will be sent to the figure upon creation

    Raises
    ------
    RuntimeError
        if multiple interactive figures are created.
    """
    if _state.fig is None:
        if hide_toolbar:
            plt.rcParams["toolbar"] = "None"

        # Disable interactive mode for explicit control over drawing. See:
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.isinteractive.html#matplotlib.pyplot.isinteractive
        plt.ioff()

        _state.fig = fig = plt.figure(**kwargs)
        fig.canvas.manager.set_window_title("Interactive Figure")
        # Create drawable axis.
        _state.ax = ax = plt.gca()
        ax.set_aspect(aspect_ratio)

        # Show figure but allow the main thread to continue.
        plt.show(block=False)

        # Reset plot state and draw to obtain focus.
        clear()
        draw()

        # Add our custom event handlers. For handlers, see:
        # https://matplotlib.org/stable/api/backend_bases_api.html#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        # For general interaction handling, see:
        # https://matplotlib.org/stable/users/explain/figure/interactive_guide.html
        # For mouse buttons, see:
        # https://matplotlib.org/stable/api/backend_bases_api.html#matplotlib.backend_bases.MouseButton
        fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
        fig.canvas.mpl_disconnect(fig.canvas.manager.button_press_handler_id)
        fig.canvas.mpl_connect("key_press_event", _key_press_handler)
        fig.canvas.mpl_connect("button_press_event", _button_press_handler)

        print("Successfully created the interactive figure.")
    else:
        raise RuntimeError("Error: you cannot create multiple interactive figures.")


def toggle_fullscreen():
    """Toggle fullscreen."""
    _check_exists()

    _state.figure.canvas.manager.full_screen_toggle()


def clear():
    """Reset the contents and layout of the drawable Axes."""
    _check_exists()

    ax = _state.ax
    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])


def wait(timeout):
    """Timeout for the given number of seconds. During this period it is
    not possible to interact with the figure. For sub-second timeouts use
    time.wait() instead.

    Parameters
    ----------
    timeout : float
        Number of seconds to wait for
    """
    _check_exists()

    _state.fig.canvas.start_event_loop(timeout=timeout)
    # No button was pressed, so reset the state.
    _state_reset_press()


def wait_for_interaction(timeout=-1):
    """Wait for interaction with the interactive figure. Optionally
    use a timeout in seconds.

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
    _check_exists()

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
        _state.fig.canvas.stop_event_loop()

    # Connect event handlers and save callback ids.
    callback_ids = [
        _state.fig.canvas.mpl_connect(name, simple_handler) for name in ["button_press_event", "key_press_event"]
    ]
    try:
        # Start a blocking event loop.
        _state.fig.canvas.start_event_loop(timeout=timeout)
    finally:
        # Disconnect handlers.
        for callback_id in callback_ids:
            _state.fig.canvas.mpl_disconnect(callback_id)

    interaction_type = None if event is None else event.name == "key_press_event"

    if interaction_type is None:
        # No button was pressed, so reset the state.
        _state_reset_press()

    return interaction_type


def draw():
    """Draw the figure."""
    _check_exists()

    canvas = _state.fig.canvas
    # Mark canvas for a draw.
    canvas.draw_idle()
    # Force update the GUI. This is when the drawing actually happens
    # in the backend.
    canvas.flush_events()


def close():
    """Close the figure."""
    _check_exists()

    plt.close(_state.fig)

    _state_reset_fig()
    _state_reset_press()

    print("Successfully closed the interactive figure.")


def get_state():
    """Get all state information of the interactive figure.

    Returns
    -------
    SimpleNamespace
        Namespace with figure state information
    """
    return _state


def gcf():
    """Get current figure.

    Returns
    -------
        Figure handler
    """
    return _state.fig


def gca():
    """Get current Axes.

    Returns
    -------
        Axes handler
    """
    return _state.ax


def get_last_keypress():
    """Get the last keypress and normalize it to lowercase.

    Returns
    -------
    str | None
        The last key that was pressed
    """
    key = _state.last_keypress

    if not key is None:
        return key.lower()
    else:
        return None


def get_last_mousepress():
    """Get the last mousepress and convert it to its integer value.

    Returns
    -------
    int | None
        The identifier of the last mouse button that was pressed
    """
    mouse = _state.last_mousepress

    if not mouse is None:
        return mouse.value
    else:
        return None


def get_last_mouse_pos():
    """Get the last mouse position.

    Returns
    -------
    (x: float, y: float) | None
        The last registered mouse position after any interaction
    """
    return (_state.last_mouse_x, _state.last_mouse_y)


# PRIVATE METHODS


def _check_exists():
    """Check if the interactive figure exists.

    Raises
    ------
    RuntimeError
        If the figure is not available
    """
    if _state.fig is None:
        raise RuntimeError("Error: the interactive figure is not available.")


def _state_reset_fig():
    """Reset figure information."""
    _state.fig = None
    _state.ax = None


def _state_reset_press():
    """Reset last registered press information."""
    _state.last_keypress = None
    _state.last_mousepress = None
    _state.last_mouse_x = None
    _state.last_mouse_y = None


def _key_press_handler(event):
    """Register key and mouse coordinates on press.

    Parameters
    ----------
    event
        The event object that was generated internally
    """
    _state.last_keypress = event.key
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


# Namespace to track the internal state of the interactive figure.
_state = SimpleNamespace(
    fig=None,
    ax=None,
    last_keypress=None,
    last_mousepress=None,
    last_mouse_x=None,
    last_mouse_y=None,
)
