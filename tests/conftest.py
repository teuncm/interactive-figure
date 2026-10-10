"""Keep tests independent and run Matplotlib without GUI windows."""

from unittest.mock import Mock

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import interactive_figure as figure

mpl.use("Agg")


@pytest.fixture(autouse=True)
def isolated_figure(monkeypatch):
    interactive = plt.isinteractive()
    figure.state.reset_fig()
    figure.state.reset_press()
    # Agg cannot show windows; creating and drawing real figures still works.
    monkeypatch.setattr(plt, "show", Mock())
    with mpl.rc_context():
        try:
            yield
        finally:
            figure.state.external_close = False
            plt.close("all")
            figure.state.reset_fig()
            figure.state.reset_press()
            plt.interactive(interactive)
