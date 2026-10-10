# Draw, clear, wait, draw.

import interactive_figure as ifig
import matplotlib.pyplot as plt

ifig.create()

plt.plot(50, 50, "ro", markersize=10)
plt.draw()
ifig.wait(0.5)

ifig.clear()
ifig.draw()
ifig.wait(0.5)

ifig.close()
