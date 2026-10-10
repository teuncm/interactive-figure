"""Exercise the public API with real Agg figures and synthetic canvas events."""

from itertools import product
from unittest.mock import Mock

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest
from matplotlib.backend_bases import CloseEvent, KeyEvent, MouseButton, MouseEvent

import interactive_figure as figure

SPINES = ("top", "right", "bottom", "left")


@pytest.fixture
def canvas():
    figure.create()
    assert figure.state.fig is not None
    return figure.state.fig.canvas


def send_input(canvas, kind, position=(25, 75), key=None, button=MouseButton.LEFT):
    """Deliver an event through the callbacks registered by create()."""
    assert figure.state.ax is not None
    x, y = (-10, -10) if position is None else figure.state.ax.transData.transform(position)
    if kind == "key_press_event":
        event = KeyEvent(kind, canvas, key=key, x=x, y=y)
    else:
        event = MouseEvent(kind, canvas, x, y, button=button, key=key)
    canvas.callbacks.process(kind, event)


def assert_no_input():
    assert figure.get_last_key_press() is None
    assert figure.get_last_mouse_press() is None
    assert figure.get_last_mouse_pos() == (None, None)


def input_callbacks(canvas):
    """Snapshot callback IDs to detect leaked temporary listeners."""
    return {name: set(canvas.callbacks.callbacks.get(name, {})) for name in ("key_press_event", "button_press_event")}


def test_create_defaults(canvas):
    assert figure.state.fig.canvas is canvas
    assert figure.state.ax in figure.state.fig.axes
    assert figure.state.ax.get_xlim() == (0, 100)
    assert figure.state.ax.get_ylim() == (0, 100)
    assert all(figure.state.ax.spines[name].get_visible() for name in SPINES)
    assert len(figure.state.ax.get_xticks()) > 0
    assert len(figure.state.ax.get_yticks()) > 0
    assert_no_input()


def test_create_rejects_second_figure(canvas):
    original = figure.state.fig
    with pytest.raises(RuntimeError, match="multiple interactive figures"):
        figure.create(hide_toolbar=True)
    assert figure.state.fig is original
    assert original.canvas is canvas


@pytest.mark.parametrize("after_close", [False, True], ids=["before-create", "after-close"])
@pytest.mark.parametrize(
    ("function", "args"),
    [
        (figure.draw, ()),
        (figure.clear, ()),
        (figure.toggle_fullscreen, ()),
        (figure.close, ()),
        (figure.wait, (0.01,)),
        (figure.wait_for_interaction, (0.01,)),
        (figure.get_last_key_press, ()),
        (figure.get_last_mouse_press, ()),
        (figure.get_last_mouse_pos, ()),
    ],
    ids=lambda value: getattr(value, "__name__", None),
)
def test_functions_require_figure(function, args, after_close):
    if after_close:
        figure.create()
        figure.close()
    with pytest.raises(RuntimeError, match="interactive figure must be created first"):
        function(*args)


@pytest.mark.parametrize("hidden", list(product([False, True], repeat=4)))
def test_frame_options_survive_clear(hidden):
    figure.create(**{f"hide_{name}_frame": flag for name, flag in zip(SPINES, hidden, strict=True)})
    for _ in range(2):
        for name, flag in zip(SPINES, hidden, strict=True):
            assert figure.state.ax.spines[name].get_visible() is not flag
        figure.clear()


@pytest.mark.parametrize(("hide_x", "hide_y"), list(product([False, True], repeat=2)))
def test_label_options_survive_clear(hide_x, hide_y):
    figure.create(hide_x_labels=hide_x, hide_y_labels=hide_y)
    for _ in range(2):
        assert (len(figure.state.ax.get_xticks()) == 0) is hide_x
        assert (len(figure.state.ax.get_yticks()) == 0) is hide_y
        figure.clear()


def test_clear_removes_content_and_restores_limits_without_drawing(canvas, monkeypatch):
    ax = figure.state.ax
    ax.plot([10, 20], [30, 40])
    ax.text(50, 50, "hello")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-20, 20)
    draw = Mock()
    monkeypatch.setattr(canvas, "draw_idle", draw)
    figure.clear()
    assert len(ax.lines) == 0
    assert len(ax.texts) == 0
    assert ax.get_xlim() == (0, 100)
    assert ax.get_ylim() == (0, 100)
    draw.assert_not_called()


@pytest.mark.parametrize("button", [MouseButton.LEFT, MouseButton.MIDDLE, MouseButton.RIGHT])
def test_mouse_input(canvas, button):
    send_input(canvas, "button_press_event", key="shift", button=button)
    assert figure.get_last_key_press() == "shift"
    assert figure.get_last_mouse_press() == button.value
    assert figure.get_last_mouse_pos() == pytest.approx((25, 75))


def test_key_input_clears_previous_mouse_button(canvas):
    send_input(canvas, "button_press_event")
    send_input(canvas, "key_press_event", position=(60, 40), key="a")
    assert figure.get_last_key_press() == "a"
    assert figure.get_last_mouse_press() is None
    assert figure.get_last_mouse_pos() == pytest.approx((60, 40))


@pytest.mark.parametrize("kind", ["key_press_event", "button_press_event"])
def test_input_outside_axes(canvas, kind):
    send_input(canvas, kind, position=None, key="a")
    assert figure.get_last_mouse_pos() == (None, None)
    assert figure.get_last_key_press() == "a"
    assert figure.get_last_mouse_press() == (None if kind == "key_press_event" else MouseButton.LEFT.value)


@pytest.mark.parametrize(("kind", "expected"), [("key_press_event", True), ("button_press_event", False)])
def test_wait_for_interaction_receives_input_and_cleans_up(canvas, monkeypatch, kind, expected):
    before = input_callbacks(canvas)
    stop = Mock()
    monkeypatch.setattr(canvas, "stop_event_loop", stop)
    loop = Mock(side_effect=lambda _timeout: send_input(canvas, kind, key="a"))
    monkeypatch.setattr(canvas, "start_event_loop", loop)
    for _ in range(3):
        assert figure.wait_for_interaction(timeout=0.25) is expected
        assert input_callbacks(canvas) == before
        assert figure.get_last_key_press() == "a"
        assert figure.get_last_mouse_pos() == pytest.approx((25, 75))
        assert figure.get_last_mouse_press() == (None if expected else MouseButton.LEFT.value)
    loop.assert_called_with(0.25)
    assert stop.call_count == 3


def test_interaction_timeout_resets_input_and_cleans_up(canvas, monkeypatch):
    send_input(canvas, "button_press_event", key="shift")
    before = input_callbacks(canvas)
    loop = Mock()
    monkeypatch.setattr(canvas, "start_event_loop", loop)
    assert figure.wait_for_interaction(timeout=0.25) is None
    loop.assert_called_once_with(0.25)
    assert input_callbacks(canvas) == before
    assert_no_input()


@pytest.mark.parametrize("error", [KeyboardInterrupt, RuntimeError])
def test_interaction_exception_disconnects_callbacks(canvas, monkeypatch, error):
    before = input_callbacks(canvas)
    monkeypatch.setattr(canvas, "start_event_loop", Mock(side_effect=error))
    with pytest.raises(error):
        figure.wait_for_interaction(timeout=0.25)
    assert input_callbacks(canvas) == before


def test_wait_resets_input(canvas, monkeypatch):
    send_input(canvas, "button_press_event", key="shift")
    loop = Mock()
    monkeypatch.setattr(canvas, "start_event_loop", loop)
    figure.wait(0.25)
    loop.assert_called_once_with(timeout=0.25)
    assert_no_input()


def test_programmatic_close_resets_state_and_allows_recreation(canvas, monkeypatch):
    original = figure.state.fig
    send_input(canvas, "button_press_event", key="shift")
    close = plt.close

    def close_with_event(fig):
        # Agg does not emit close_event; GUI backends do.
        canvas.callbacks.process("close_event", CloseEvent("close_event", canvas))
        close(fig)

    monkeypatch.setattr(plt, "close", close_with_event)
    figure.close()
    monkeypatch.setattr(plt, "close", close)
    assert not plt.fignum_exists(original.number)
    assert figure.state.fig is None
    assert figure.state.ax is None
    assert figure.state.external_close is True
    assert figure.state.closing is False
    assert figure.state.last_keypress is None
    assert figure.state.last_mousepress is None
    assert figure.state.last_mouse_x is None
    assert figure.state.last_mouse_y is None
    figure.create()
    assert figure.state.fig is not original
    assert_no_input()


def test_close_resets_display_options():
    figure.create(hide_x_labels=True, hide_y_labels=True, **{f"hide_{name}_frame": True for name in SPINES})
    figure.close()
    figure.create()
    assert all(figure.state.ax.spines[name].get_visible() for name in SPINES)
    assert len(figure.state.ax.get_xticks()) > 0
    assert len(figure.state.ax.get_yticks()) > 0


def test_external_close_exits_once(canvas):
    event = CloseEvent("close_event", canvas)
    with pytest.raises(SystemExit):
        canvas.callbacks.process("close_event", event)
    assert figure.state.closing is True
    canvas.callbacks.process("close_event", event)


@pytest.mark.parametrize("toolbar", ["toolbar2", "toolmanager", "None"])
@pytest.mark.filterwarnings("ignore:.*Tool classes.*:UserWarning")
def test_hidden_toolbar_restores_previous_setting(toolbar):
    mpl.rcParams["toolbar"] = toolbar
    figure.create(hide_toolbar=True)
    assert mpl.rcParams["toolbar"] == "None"
    with pytest.raises(RuntimeError, match="multiple interactive figures"):
        figure.create(hide_toolbar=True)
    figure.close()
    assert mpl.rcParams["toolbar"] == toolbar
    assert figure.state.previous_toolbar is None
    figure.create()
    assert mpl.rcParams["toolbar"] == toolbar
    figure.close()
    assert mpl.rcParams["toolbar"] == toolbar


@pytest.mark.usefixtures("canvas")
def test_default_create_does_not_override_later_toolbar_changes():
    mpl.rcParams["toolbar"] = "None"
    figure.close()
    assert mpl.rcParams["toolbar"] == "None"


def test_draw_updates_canvas_in_order(canvas, monkeypatch):
    calls = Mock()
    monkeypatch.setattr(canvas, "draw_idle", calls.draw)
    monkeypatch.setattr(canvas, "flush_events", calls.flush)
    figure.draw()
    assert [call[0] for call in calls.mock_calls] == ["draw", "flush"]
    calls.draw.assert_called_once_with()
    calls.flush.assert_called_once_with()


def test_toggle_fullscreen_uses_figure_manager(canvas, monkeypatch):
    toggle = Mock()
    monkeypatch.setattr(canvas.manager, "full_screen_toggle", toggle)
    figure.toggle_fullscreen()
    toggle.assert_called_once_with()
