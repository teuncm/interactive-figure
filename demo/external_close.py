# This demo confirms that the external close functionality works.

import interactive_figure as ifig

ifig.create()
no_number = "no_number"
int(no_number) # This will raise an exception.
ifig.wait_for_interaction()
