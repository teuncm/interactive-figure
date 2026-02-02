# This demo tests the fullscreen toggle functionality.

import interactive_figure as ifig
import matplotlib.pyplot as plt

ifig.create()
plt.title("Windowed mode")
ifig.draw()
ifig.wait_for_interaction()
ifig.toggle_fullscreen()
plt.title("Fullscreen mode")
ifig.draw()
ifig.wait_for_interaction()
ifig.toggle_fullscreen()
plt.title("Windowed mode")
ifig.draw()
ifig.wait_for_interaction()
ifig.close()
