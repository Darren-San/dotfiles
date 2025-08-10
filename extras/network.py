from libqtile.widget import base
import psutil

class NetworkIcon(base.ThreadPoolText):
    def __init__(self, **config):
        super().__init__(text="󰤫", **config)
        self.add_defaults(NetworkIcon.defaults)
    def poll(self):
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for interface, addrs in interfaces.items():
            if interface in stats and stats[interface].isup:
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        return "󰈁"
                    elif addr.family == psutil.AF_INET:
                        if "wl" in interface:
                            return "󰤨"
                        elif "en" in interface:
                            return "󰈁"
        return "󰤫"
