from libqtile.config import Group, Key
from libqtile.lazy import lazy

from core.keys import keys, mod
from utils.match import wm_class

groups: list[Group] = []

for key, label, layout, matches in [
    ("1", "", None, wm_class("wezterm")),
    ("2", "", "max", wm_class("nvim")),
    ("3", "", "max", wm_class("nnn")),
    ("q", "", "max", wm_class("brave-browser", "firefox")),
    ("w", "", "max", wm_class("telegram-desktop", "element-desktop", "discord")),
    ("e", "", "max", wm_class("retroarch", "steam", "vlc")),
]:
    groups.append(Group(key, matches, label=label, layout=layout))

    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], key, lazy.group[key].toscreen(toggle=True)),

        # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], key, lazy.window.togroup(key)),
    ])  # fmt: skip
