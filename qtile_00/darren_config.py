# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
import psutil
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

# Assign default group for both screens
@hook.subscribe.startup
def _():
    # Set initial groups
    if len(qtile.screens) > 1:
        qtile.groups_map["CHAT"].cmd_toscreen(0, toggle=False)
        qtile.groups_map["EXTRA"].cmd_toscreen(1, toggle=False)

mod = "mod4"            # Sets mod key to SUPER/WINDOWS
terminal = "alacritty"  # Terminal of choice
Browser = "brave"       # Browser of choice

keys = [
    ### The essentials
    Key([mod], "Return", lazy.spawn(terminal), desc='Launches My Terminal'),
    Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
    Key([mod], "w", lazy.window.kill(), desc='Kill active window'),
    Key([mod], "r", lazy.restart(), desc='Restart Qtile' ),
    Key([mod], "z", lazy.window.toggle_floating(), desc='Toggle Floating State' ),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    ### Some programs
    Key([mod], "v", lazy.spawn(Browser), desc='Default browser'),
    Key([mod], "b", lazy.spawn("firefox"), desc='Firefox browser'),
    Key([mod], "d", lazy.spawn("discord"), desc='Discord'),
    Key([mod], "t", lazy.spawn("telegram-desktop"), desc='Telegram'),
    Key([mod], "e", lazy.spawn("element-desktop"), desc='Element'),

    ### Move between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
]

groups = [Group("CHAT", layout='Columns'),
          Group("DEV", layout='Columns'),
          Group("DOC", layout='Columns'),
          Group("MEDIA", layout='Columns'),
          Group("EXTRA", layout='Columns')
]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 3,
                "margin": 5,
                "border_normal":"#00416a",
                "border_normal_stack":"#00416a",
                "border_focus":"#5ea8d6",
                "border_focus_stack":"#a9a1e1"
                }

layouts = [
    layout.Columns(**layout_theme),
    #layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
]

colors = [["#282c34", "#282c34"], # Very dark grayish blue
          ["#1c1f24", "#1c1f24"], # Very dark (mostly black) blue
          ["#dfdfdf", "#dfdfdf"], # Very light gray
          ["#ff6c6b", "#ff6c6b"], # Very light red
          ["#9dda48", "#9dda48"], # Soft green
          ["#eb5b00", "#da8548"], # Soft orange
          ["#489dda", "#489dda"], # Soft blue
          ["#eb0090", "#c678dd"], # Soft magenta
          ["#0090eb", "#0090eb"], # Pure Blue
          ["#a9a1e1", "#a9a1e1"]] # Very soft blue

font_sizes = {
    "small": 12,
    "medium": 14,
    "big": 26,
    "xl": 32
}

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Roboto",
    fontsize = font_sizes["xl"],
    padding = 5,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              # widget.Image(
              #         padding = 6,
              #         filename = "~/.config/qtile/icons/python.png",
              #         scale = "False",
              #         mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}
              #         ),
              widget.GroupBox(
                       fontsize = font_sizes["big"],
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[9],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = font_sizes["big"]
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2],
                       background = colors[0],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[0],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = font_sizes["big"]
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.Systray(
                       background = colors[0],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
             widget.Net(
                       interface = "enp6s0",
                       format = 'Net: {down} ↓↑ {up}',
                       foreground = colors[3],
                       background = colors[0],
                       decorations=[
                           BorderDecoration(
                               colour = colors[3],
                               border_width = [0, 0, 2, 0],
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.ThermalSensor(
                       foreground = colors[5],
                       background = colors[0],
                       foreground_alert = colors[3],
                       tag_sensor = 'Composite',
                       show_tag = True,
                       threshold = 80,
                       fmt = '{}',
                       decorations=[
                           BorderDecoration(
                               colour = colors[5],
                               border_width = [0, 0, 2, 0],
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.Memory(
                       foreground = colors[5],
                       background = colors[0],
                       fmt = '{}',
                       measure_mem='G',
                       decorations=[
                           BorderDecoration(
                               colour = colors[5],
                               border_width = [0, 0, 2, 0],
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "{updates} U",
                       foreground = colors[4],
                       colour_have_updates = colors[4],
                       colour_no_updates = colors[4],
                       background = colors[0],
                       decorations=[
                           BorderDecoration(
                               colour = colors[4],
                               border_width = [0, 0, 2, 0],
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.Volume(
                       foreground = colors[7],
                       background = colors[0],
                       fmt = '{}',
                       decorations=[
                           BorderDecoration(
                               colour = colors[7],
                               border_width = [0, 0, 2, 0],
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.GenPollText(
                       func=lambda: subprocess.check_output("~/scripts/days_left.sh").decode("utf-8").strip(),
                       foreground = colors[6],
                       background = colors[0],
                       decorations=[
                           BorderDecoration(
                               colour = colors[6],
                               border_width = [0, 0, 2, 0],
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.KeyboardLayout(
                       foreground = colors[6],
                       background = colors[0],
                       fmt = '{}',
                       decorations=[
                           BorderDecoration(
                               colour = colors[6],
                               border_width = [0, 0, 2, 0],
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.AnalogueClock(
                       background = colors[0],
                       face_shape = "circle",
                       face_background = colors[6],
                       face_border_colour = colors[6],
                       face_border_width = 4,
                       ),
              widget.Clock(
                       foreground = colors[2],
                       background = colors[0],
                       format = " %H:%M %a %d-%m-%Y (%V) ",
                       decorations=[
                           BorderDecoration(
                               colour = colors[6],
                               border_width = [0, 0, 2, 0],
                               padding_x = 5,
                               padding_y = None,
                           )
                       ],
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              ]
    return widgets_list

screens = [
    Screen(top=bar.Bar(widgets=init_widgets_list(), opacity=1.0, size=20)),
    Screen(top=bar.Bar(widgets=init_widgets_list()[:6], opacity=1.0, size=16))
]

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        # default_float_rules include: utility, notification, toolbar, splash, dialog,
        # file_progress, confirm, download and error.
        *layout.Floating.default_float_rules,
        Match(title="Confirmation"),  # tastyworks exit box
        Match(title="Qalculate!"),  # qalculate-gtk
        Match(wm_class="kdenlive"),  # kdenlive
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
    ],
    border_focus="#00416a",
    border_normal="#001421",
    border_width=3
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
