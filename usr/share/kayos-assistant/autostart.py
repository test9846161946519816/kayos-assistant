import _functions

def get_startups(self, n):

    try:
        with open(_functions.autostart + n + ".desktop") as f:
            lines = f.readlines()
            f.close()
        state = True
    except Exception as e:
        return True

    try:
        pos = _functions._get_position(lines, "Hidden=")
        state = lines[pos].split("=")[1].strip()

        state = state.capitalize()
        state = not eval(state)
        return state
    except Exception as e:
        print(e)
        return True


def add_autostart(self, name, com, comnt):
    lists = [x for x in _functions.os.listdir(_functions.home + "/.config/autostart/")]
    if not (name + ".desktop") in lists:
        content = "[Desktop Entry]\n\
Encoding=UTF-8\n\
Version=1.0\n\
Type=Application\n\
Name=" + name + "\n\
Comment=" + comnt + "\n\
Exec=" + com + "\n\
TryExec=" + com + "\n\
StartupNotify=false\n\
X-GNOME-Autostart-enabled=true\n\
Terminal=false\n\
Hidden=false\n"

        with open(_functions.home + "/.config/autostart/" + name + ".desktop", "w") as f:
            f.write(content)
            f.close()
        self.add_row(name)
        # self.startups.append([True, name, comnt])
