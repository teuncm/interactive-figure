interactive_figure.interactive_figure
=====================================

.. py:module:: interactive_figure.interactive_figure

.. autoapi-nested-parse::

   This module provides functions to create and interact with a Matplotlib figure. The figure registers mouse presses,
   keyboard input and the location of the mouse after any input.

   Source: https://github.com/teuncm/interactive-figure



Functions
---------

.. autoapisummary::

   interactive_figure.interactive_figure.create
   interactive_figure.interactive_figure.draw
   interactive_figure.interactive_figure.clear
   interactive_figure.interactive_figure.toggle_fullscreen
   interactive_figure.interactive_figure.close
   interactive_figure.interactive_figure.wait_for_interaction
   interactive_figure.interactive_figure.get_last_key_press
   interactive_figure.interactive_figure.get_last_mouse_press
   interactive_figure.interactive_figure.get_last_mouse_pos
   interactive_figure.interactive_figure.wait


Module Contents
---------------

.. py:function:: create(hide_x_labels=False, hide_y_labels=False, hide_top_frame=False, hide_right_frame=False, hide_bottom_frame=False, hide_left_frame=False, hide_toolbar=False, layout='constrained', **kwargs) -> None

   Create the interactive figure.

   Parameters
   ----------
   hide_x_labels : bool, optional
       Hide the x-axis labels, default False.
   hide_y_labels : bool, optional
       Hide the y-axis labels, default False.
   hide_top_frame : bool, optional
       Hide the top edge of the axes frame, default False.
   hide_right_frame : bool, optional
       Hide the right edge of the axes frame, default False.
   hide_bottom_frame : bool, optional
       Hide the bottom edge of the axes frame, default False.
   hide_left_frame : bool, optional
       Hide the left edge of the axes frame, default False.
   hide_toolbar : bool, optional
       Hide the toolbar, default False.
   layout : str, optional
       The layout mode for the figure, default 'constrained'. See:
       https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html

   Remaining keyword arguments will be sent to the Matplotlib figure.

   Returns
   -------
   None

   Raises
   ----------
   RuntimeError
       if multiple interactive figures are created at the same time.


.. py:function:: draw() -> None

   Draw contents of the figure.

   Parameters
   ----------
   None

   Returns
   -------
   None


.. py:function:: clear() -> None

   Clear, but don't draw() the figure.

   Parameters
   ----------
   None

   Returns
   -------
   None


.. py:function:: toggle_fullscreen() -> None

   Toggle fullscreen on/off.

   Parameters
   ----------
   None

   Returns
   -------
   None


.. py:function:: close() -> None

   Close the figure.

   Parameters
   ----------
   None

   Returns
   -------
   None


.. py:function:: wait_for_interaction(timeout=-1) -> bool | None

   Wait for interaction.

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


.. py:function:: get_last_key_press() -> str | None

   Get the last key press in lowercase.

   Parameters
   ----------
   None

   Returns
   -------
   str | None
       The last key that was pressed.


.. py:function:: get_last_mouse_press() -> int | None

   Get the ID of the last mouse press.

   Parameters
   ----------
   None

   Returns
   -------
   int | None
       The identifier of the last mouse button that was pressed.


.. py:function:: get_last_mouse_pos() -> tuple[float | None, float | None]

   Get the last mouse position.

   Parameters
   ----------
   None

   Returns
   -------
   (x: float, y: float) | (None, None)
       The last registered mouse position after any interaction.


.. py:function:: wait(timeout) -> None

   Freeze for the given number of seconds.

   During this period it is not possible to interact
   with the figure. For sub-second timeouts use time.wait() instead.

   Parameters
   ----------
   timeout : float
       Number of seconds to wait for.

   Returns
   -------
   None


