from dataclasses import dataclass


# https://github.com/catppuccin/catppuccin#-palette
# fmt: off
@dataclass(frozen=True)
class Catppuccin:
    crust     = "#11111b"
    mantle    = "#181825"
    base      = "#1e1e2e"
    surface0  = "#313244"
    surface1  = "#45475a"
    surface2  = "#585b70"
    overlay0  = "#6c7086"
    overlay1  = "#7f849c"
    overlay2  = "#9399b2"
    subtext0  = "#a6adc8"
    subtext1  = "#bac2de"
    text      = "#cdd6f4"
    lavender  = "#b4befe"
    blue      = "#89b4fa"
    sapphire  = "#74c7ec"
    sky       = "#89dceb"
    teal      = "#94e2d5"
    green     = "#a6e3a1"
    yellow    = "#f9e2af"
    peach     = "#fab387"
    red       = "#f38ba8"
    maroon    = "#eba0ac"
    flamingo  = "#f2cdcd"
    rosewater = "#f5e0dc"
    pink      = "#f5c2e7"
    mauve     = "#cba6f7"

palette = Catppuccin()
