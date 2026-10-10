# Test spine hiding.

import interactive_figure as ifig

ifig.create(hide_top_frame=True, hide_left_frame=True, hide_x_labels=True)
while True:
  ifig.wait_for_interaction()
  key = ifig.get_last_key_press()
  print(f"Pressed key: {key}")
  x, y = ifig.get_last_mouse_pos()

  # Exit if q is pressed outside rectangle.
  if (x is None or y is None) and key == "q":
      break

ifig.close()
