interactive_figure
==================

.. py:module:: interactive_figure


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/interactive_figure/interactive_figure/index


Attributes
----------

.. autoapisummary::

   interactive_figure.state


Functions
---------

.. autoapisummary::

   interactive_figure.clear
   interactive_figure.close
   interactive_figure.create
   interactive_figure.draw
   interactive_figure.get_last_key_press
   interactive_figure.get_last_mouse_pos
   interactive_figure.get_last_mouse_press
   interactive_figure.toggle_fullscreen
   interactive_figure.wait
   interactive_figure.wait_for_interaction


Package Contents
----------------

.. py:data:: state

.. py:function:: clear()

   Clear the canvas, but *don't* draw() it.

   :Parameters: **None**

   :returns: *None*


.. py:function:: close()

   Close the figure.

   :Parameters: **None**

   :returns: *None*


.. py:function:: create(hide_x_labels=False, hide_y_labels=False, hide_top_frame=False, hide_right_frame=False, hide_bottom_frame=False, hide_left_frame=False, hide_toolbar=False, layout='constrained', **kwargs)

   Create the interactive figure.

   :Parameters: * **hide_x_labels** (*bool, optional*) -- Hide the x-axis labels, default False.
                * **hide_y_labels** (*bool, optional*) -- Hide the y-axis labels, default False.
                * **hide_top_frame** (*bool, optional*) -- Hide the top edge of the axes frame, default False.
                * **hide_right_frame** (*bool, optional*) -- Hide the right edge of the axes frame, default False.
                * **hide_bottom_frame** (*bool, optional*) -- Hide the bottom edge of the axes frame, default False.
                * **hide_left_frame** (*bool, optional*) -- Hide the left edge of the axes frame, default False.
                * **hide_toolbar** (*bool, optional*) -- Hide the toolbar, default False.
                * **layout** (*str, optional*) -- The layout mode for the figure, default 'constrained'. See:
                  https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html
                * **Remaining keyword arguments will be sent to the Matplotlib figure.**

   :returns: *None*

   :raises RuntimeError: if multiple interactive figures are created at the same time.


.. py:function:: draw()

   Draw contents of the figure canvas.

   :Parameters: **None**

   :returns: *None*


.. py:function:: get_last_key_press()

   Get the last key press.

   :Parameters: **None**

   :returns: *str | None* -- The last key that was pressed.


.. py:function:: get_last_mouse_pos()

   Get the last mouse position.

   :Parameters: **None**

   :returns: **(x** (*float, y: float) | (None, None)*) -- The last registered mouse position after any interaction.


.. py:function:: get_last_mouse_press()

   Get the ID of the last mouse press.

   :Parameters: **None**

   :returns: *int | None* -- The identifier of the last mouse button that was pressed.


.. py:function:: toggle_fullscreen()

   Toggle fullscreen on/off.

   :Parameters: **None**

   :returns: *None*


.. py:function:: wait(timeout)

   Freeze for the given number of seconds.

   During this period it is not possible to interact
   with the figure. For sub-second timeouts use time.wait() instead.

   :Parameters: **timeout** (*float*) -- Number of seconds to wait for.

   :returns: *None*


.. py:function:: wait_for_interaction(timeout=-1)

   Wait for interaction.

   Optionally use a timeout in seconds.

   :Parameters: **timeout** (*int, optional*) -- Timeout in seconds when waiting for input.

   :returns: *bool | None* --

             - True if a key was pressed.
             - False if a mouse button was pressed.
             - None if no input was given within the timeout.


