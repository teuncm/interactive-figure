# This demo is the script in the usage section.

import interactive_figure as ifig

ifig.create()
# Wait until user input is received.
ifig.wait_for_interaction()
key = ifig.get_last_key_press()
print(f"Pressed key: {key}")
ifig.close()
