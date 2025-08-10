from libqtile.bar import CALCULATED
from libqtile.lazy import lazy

from core.bar.base import base, powerline, rectangle, symbol
from extras import Clock, GroupBox, TextBox, modify, widget
from extras.network import NetworkIcon
from utils.config import cfg
from utils.palette import palette

bar = {
    "background": palette.base,
    "border_color": palette.base,
    "border_width": 4,
    "margin": [10, 10, 0, 10],
    "opacity": 1,
    "size": 50,
}

def sep(fg, offset=0, padding=10):
    return TextBox(
        **base(None, fg),
        **symbol(),
        offset=offset,
        padding=padding,
        text="󰇙",
    )

logo = lambda bg, fg: TextBox(
    **base(bg, fg),
    **symbol(),
    **rectangle(),
    mouse_callbacks={"Button1": lazy.restart()},
    padding=20,
    text="",
)

groups = lambda bg: GroupBox(
    **symbol(),
    background=bg,
    borderwidth=1,
    colors=[
        palette.blue,
        palette.teal,
        palette.lavender,
        palette.red,
        palette.sapphire,
        palette.flamingo,
    ],
    highlight_color=palette.base,
    highlight_method="line",
    inactive=palette.surface2,
    invert=True,
    padding=6,
    rainbow=True,
)

# network = lambda bg, fg: [
#     modify(
#         TextBox,
#         **base(bg, fg),
#         **symbol(),
#         **rectangle("left"),
#         offset=-13,
#         padding=15,
#         text=" ",
#     ),
#     NetworkIcon(
#         **base(bg, fg),
#         **powerline("arrow_right"),
#         update_interval=5,
#         fontsize=50,
#     ),
# ]

updates = lambda bg, fg: [
    TextBox(
        **base(bg, fg),
        **symbol(28),
        offset=-1,
        text="",
        x=-2,
    ),
    widget.CheckUpdates(
        **base(bg, fg),
        **rectangle("right"),
        colour_have_updates=fg,
        colour_no_updates=fg,
        custom_command=" " if cfg.is_xephyr else "checkupdates",
        display_format="{updates}",
        initial_text="...",
        no_update_string="0",
        padding=15,
        update_interval=3600,
    ),
]

window_name = lambda fg: widget.WindowName(
    **base(None, fg),
    fontsize=30,
    format="{name}",
    max_chars=56,
    width=CALCULATED,
)

# cpu = lambda bg, fg: [
#     modify(
#         TextBox,
#         **base(bg, fg),
#         **symbol(),
#         **rectangle("left"),
#         offset=-13,
#         padding=15,
#         text="󰍛",
#     ),
#     widget.CPU(
#         **base(bg, fg),
#         **powerline("arrow_right"),
#         format="{load_percent:.0f}%",
#     ),
# ]

# ram = lambda bg, fg: [
#     TextBox(
#         **base(bg, fg),
#         **symbol(),
#         offset=-1,
#         padding=15,
#         text="󰘚",
#     ),
#     widget.Memory(
#         **base(bg, fg),
#         **powerline("arrow_right"),
#         format="{MemUsed:,.0f}m ",
#         padding=-3,
#     ),
# ]

# keyboard = lambda bg, fg: [
#     TextBox(
#         **base(bg, fg),
#         **symbol(),
#         offset=-1,
#         text="",
#         x=-2,
#     ),
#     widget.KeyboardLayout(
#         **base(bg, fg),
#         **powerline("arrow_right"),
#         configured_keyboards=["us", "es"],
#         update_interval=1,
#         display_map={"us": "US ", "es": "ES "},
#         padding=0,
#     ),
# ]

# volume = lambda bg, fg: [
#     modify(
#         TextBox,
#         **base(bg, fg),
#         **symbol(),
#         **powerline("arrow_left"),
#         offset=-17,
#         padding=1,
#         text="",
#         x=-2,
#     ),
#     widget.Volume(
#         **base(bg, fg),
#         **powerline("arrow_right"),
#         check_mute_command="pamixer --get-mute",
#         check_mute_string="true",
#         get_volume_command="pamixer --get-volume-human",
#         mute_command="pamixer --toggle-mute",
#         update_interval=0.1,
#         volume_down_command="pamixer --decrease 5",
#         volume_up_command="pamixer --increase 5",
#     ),
# ]

battery = lambda bg, fg: [
    TextBox(
        **base(bg, fg),
        **symbol(),
        offset=-1,
        text="",
    ),
    widget.Battery(
        **base(bg, fg),
        **rectangle("right"),
        update_interval=10,
        low_percentage=0.2,
        low_foreground=fg,
        format="{char} {percent:2.0%}",
        charging_icon="",
        full_icon="",
        empty_icon="",
    )
]

clock = lambda bg, fg: [
    modify(
        TextBox,
        **base(bg, fg),
        **symbol(),
        **rectangle(),
        offset=-14,
        padding=16,
        text="",
    ),
    modify(
        Clock,
        **base(bg, fg),
        **rectangle(),
        format="%A %d %H:%M|%V",
        long_format="%d-%m-%Y",
        padding=7,
    ),
]


widgets = lambda: [
    widget.Spacer(length=1),
    logo(palette.blue, palette.base),
    sep(palette.surface2, offset=-14),
    groups(None),
    sep(palette.surface2, offset=8, padding=2),
    # *network(palette.maroon, palette.base),
    *updates(palette.peach, palette.base),
    window_name(palette.text),
    widget.Spacer(),
    # *cpu(palette.peach, palette.base),
    # *ram(palette.yellow, palette.base),
    # *keyboard(palette.teal, palette.base),
    # *volume(palette.teal, palette.base),
    *battery(palette.sapphire, palette.base),
    sep(palette.surface2),
    *clock(palette.lavender, palette.base),
    widget.Spacer(length=1),
]
