import _functions, os
from gi.repository import GLib

def check_sddmk_session(value):
    with open(_functions.sddm_conf, "r") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:          
            return True
    return False

def insert_session(text):
    with open(_functions.sddm_conf, "r") as f:
        lines = f.readlines()
        f.close()
    pos = _functions._get_position(lines, "[Autologin]")
    num = pos+2

    lines.insert(num, text + "\n")

    with open(_functions.sddm_conf, "w") as f:
        f.writelines(lines)
        f.close() 


def check_sddmk_user(value):
    with open(_functions.sddm_conf, "r") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:          
            return True
    return False

def insert_user(text):
    with open(_functions.sddm_conf, "r") as f:
        lines = f.readlines()
        f.close()
    pos = _functions._get_position(lines, "[Autologin]")
    num = pos+3

    lines.insert(num, text + "\n")

    with open(_functions.sddm_conf, "w") as f:
        f.writelines(lines)
        f.close() 


def check_sddm(lists, value):
    pos = _functions._get_position(lists, value)
    val = lists[pos].strip()
    return val

def set_sddm_value(self, lists, value, session, state, theme):
    try:
        com = _functions.subprocess.run(["sh", "-c", "su - " + _functions.sudo_username + " -c groups"], shell=False, stdout=_functions.subprocess.PIPE)
        groups = com.stdout.decode().strip().split(" ")
        # print(groups)
        if "autologin" not in groups:
            _functions.subprocess.run(["gpasswd", "-a", _functions.sudo_username, "autologin"], shell=False)            
       
        pos = _functions._get_position(lists, "Session=")
        pos_session = _functions._get_position(lists, "User=")

        if state:
            lists[pos_session] = "User=" + value + "\n"
            lists[pos] = "Session=" + session + "\n"
        else:
            if "#" not in lists[pos]:
                lists[pos] = "#" + lists[pos]
                lists[pos_session] = "#" + lists[pos_session]
        
        pos_theme = _functions._get_position(lists, "Current=")
        lists[pos_theme] = "Current=" + theme + "\n" 

        with open(_functions.sddm_conf, "w") as f:
            f.writelines(lists)
            f.close()

#        GLib.idle_add(_functions.show_in_app_notification, self, "Settings Saved Successfully")

    except Exception as e:
        print(e)
        _functions.MessageBox(self, "Failed!!", "There seems to have been a problem in \"set_sddm_value\"")
 
def set_sddm_cursor(self, lists, cursor):    
    try:                    

        pos_theme = _functions._get_position(lists, "CursorTheme=")
        lists[pos_theme] = "CursorTheme=" + cursor + "\n" 

        with open(_functions.sddm_default, "w") as f:
            f.writelines(lists)
            f.close()

        GLib.idle_add(_functions.show_in_app_notification, self, "Settings Saved Successfully")

    except Exception as e:
            print(e)
            _functions.MessageBox(self, "Failed!!", "There seems to have been a problem in \"set_sddm_value\"")


def get_sddm_lines(files):
    if _functions.os.path.isfile(files):
        with open(files, "r") as f:
            lines = f.readlines()
            f.close()
        return lines


def pop_box(self, combos):
    comss = []
    combos.get_model().clear()

    for items in _functions.os.listdir("/usr/share/xsessions/"):
        comss.append(items.split(".")[0].lower())
    lines = get_sddm_lines(_functions.sddm_conf)

    name = check_sddm(lines, "Session=").split("=")[1]

    
    comss.sort()
    if 'i3-with-shmlog' in comss:
        comss.remove('i3-with-shmlog')
    if 'openbox-kde' in comss:
        comss.remove('openbox-kde')
    if 'cinnamon2d' in comss:
        comss.remove('cinnamon2d')
    if 'icewm-session' in comss:
        comss.remove('icewm-session')

    for i in range(len(comss)):
        combos.append_text(comss[i])
        if name.lower() == comss[i].lower():
           combos.set_active(i)

def pop_theme_box(self, combo):
    coms = []
    combo.get_model().clear()

    if os.path.exists("/usr/share/sddm"):
        for items in _functions.os.listdir("/usr/share/sddm/themes/"):
            coms.append(items.split(".")[0].lower())
        lines = get_sddm_lines(_functions.sddm_conf)

        name = check_sddm(lines, "Current=").split("=")[1]

        coms.sort()
        for i in range(len(coms)):
            #excludes = ['maya', 'maldives', 'elarun', '']
            #if not coms[i] in excludes:
            combo.append_text(coms[i])
            if name.lower() == coms[i].lower():
                combo.set_active(i)
