# This demo confirms that the external close functionality works.

import interactive_figure as ifig

ifig.create()
string_var = "test"
# Will raise an exception and close the figure.
int(string_var)
ifig.wait_for_interaction()
