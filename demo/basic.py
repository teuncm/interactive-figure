# Basic interactivity demo showing the internal state change after user input.

from interactive_figure import interactive_figure
import time

TIME_LIMIT = 10

interactive_figure.create()
print("State:", interactive_figure.get_state())

before = time.time()
interaction_type = interactive_figure.wait_for_interaction(TIME_LIMIT)
after = time.time()

reaction_time = round(after - before, 3)

if interaction_type is None:
    print("No input was registered within the time limit.")
else:
    print("User responded within", reaction_time, "seconds.")

print("State:", interactive_figure.get_state())
interactive_figure.close()
