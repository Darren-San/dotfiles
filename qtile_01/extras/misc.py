from libqtile.core.manager import Qtile
import subprocess

def float_to_front(qtile: Qtile) -> None:
    for window in qtile.current_group.windows:
        if window.floating:
            window.bring_to_front()

def toggle_keyboard_layout():
    result = subprocess.run(["setxkbmap", "-query"], capture_output=True, text=True)
    current_layout = ""
    for line in result.stdout.splitlines():
        if "layout:" in line:
            current_layout = line.split(":")[1].strip()
            break
    new_layout = "es" if current_layout == "us" else "us"
    subprocess.run(["setxkbmap", new_layout])
