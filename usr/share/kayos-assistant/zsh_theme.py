import os
import _functions


def check_oh_my():
    return os.path.isdir("/usr/share/oh-my-zsh/themes")


def get_themes(combo):
    if check_oh_my():
        try:
            lists = [x for x in os.listdir("/usr/share/oh-my-zsh/themes")]
            lists_sorted = sorted(lists)
            with open(_functions.zsh_config, "r") as f:
                theme_list = f.readlines()
                f.close()
            pos = _functions._get_position(theme_list, "ZSH_THEME=")
            #stripping whitespace, and quotation marks
            name = theme_list[pos].split("=")[1].strip().strip('"')
            active = 0
            combo.append_text("random")
            for x in range(len(lists_sorted)):
                if name in lists_sorted[x].replace(".zsh-theme", ""):
                    active = x+1 #remember; arrays start at ZERO
                combo.append_text(lists_sorted[x].split(".")[0].strip())
            combo.set_active(active)
        except OSError:
            print("ATT was unable to locate your .zshrc file, please either move your zshrc file to your base home directory (~/.zshrc), or run cz in zsh to restore the Arcolinux default.")
        except Exception as e:
            print(e)
    else:
        combo.append_text("oh-my-zsh not installed...")
        combo.set_active(0)


def set_config(self, theme):
    if not os.path.isfile(_functions.zsh_config + ".bak"):
        _functions.shutil.copy(_functions.zsh_config,
                              _functions.zsh_config + ".bak")

    try:
        with open(_functions.zsh_config, "r") as f:
            theme_list = f.readlines()
            f.close()

        pos = _functions._get_position(theme_list, "ZSH_THEME=")

        theme_list[pos] = "ZSH_THEME=\"" + theme + "\"\n"

        with open(_functions.zsh_config, "w") as f:
            f.writelines(theme_list)
            f.close()

        _functions.show_in_app_notification(self,
                                           "Settings Saved Successfully")

    except Exception as e:
        print(e)
        _functions.MessageBox(self,
                             "Error!!",
                             "Something went wrong setting this theme.")
