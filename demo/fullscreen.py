# This demo tests the fullscreen toggle functionality.

import matplotlib.pyplot as plt

import interactive_figure as ifig


def main():
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


if __name__ == "__main__":
    main()
