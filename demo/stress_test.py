# This is a timing-based stress test for the interactive figure.

import random
import interactive_figure as ifig
import matplotlib.pyplot as plt
import time
import math


def main():
    ifig.create()
    stress_test()
    ifig.close()


def stress_test():
    """
    Draw a scene with a bunch of randomly appearing objects and a rotating circle.
    """
    cur_angle = 0

    cx, cy = 50, 50
    radius = 40
    num_objects = 50

    while True:
        ifig.clear()

        x = cx + math.cos(cur_angle) * radius
        y = cy + math.sin(cur_angle) * radius
        plt.plot(x, y, marker="o", markersize=15, markerfacecolor="blue", linestyle='none', alpha=0.5)
        plt.plot([cx, x], [cy, y], marker=None, color="red", alpha=0.5, linewidth=3)

        for _ in range(num_objects):
            angle = random.random() * 2 * math.pi
            dist = random.random() * radius
            ox = cx + math.cos(angle) * dist
            oy = cy + math.sin(angle) * dist
            plt.plot(ox, oy, marker="o", markersize=10, markerfacecolor="green", linestyle='none', linewidth=10, alpha=0.3)

        ifig.draw()

        cur_angle += -(math.pi / 90)
        # Note that exiting while in the loop will cause a cleanup error.
        # To exit cleanly, press 'q' to close the figure.
        plt.pause(0.01)

        # Exit if q is pressed outside rectangle.
        if ifig.get_last_key_press() == "q":
            print("closing...")
            return


if __name__ == "__main__":
    main()
