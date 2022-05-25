import os
import distro
import sys
import shutil
import psutil
import datetime
import subprocess
import threading  # noqa
import gi
# import configparser
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk  # noqa

distr = distro.id()

sudo_username = os.getlogin()
home = "/home/" + str(sudo_username)

sddm_default = "/etc/sddm.conf"
sddm_default_original = "/usr/local/share/arcolinux/sddm/sddm.conf"

sddm_default_d1 = "/etc/sddm.conf"
sddm_default_d2 = "/etc/sddm.conf.d/kde_settings.conf"
sddm_default_d2_dir = "/etc/sddm.conf.d/"
sddm_default_d_sddm_original_1 = "/usr/local/share/arcolinux/sddm.conf.d/sddm.conf"
sddm_default_d_sddm_original_2 = "/usr/local/share/arcolinux/sddm.conf.d/kde_settings.conf"

if os.path.exists("/etc/sddm.conf.d/kde_settings.conf"):
    sddm_conf = "/etc/sddm.conf.d/kde_settings.conf"
else:
    sddm_conf = "/etc/sddm.conf"

arcolinux_mirrorlist = "/etc/pacman.d/arcolinux-mirrorlist"
arcolinux_mirrorlist_original = "/usr/local/share/arcolinux/arcolinux-mirrorlist"
pacman = "/etc/pacman.conf"
pacman_arco ="/usr/share/arcolinux-tweak-tool/data/arco/pacman.conf"
pacman_eos ="/usr/share/arcolinux-tweak-tool/data/eos/pacman.conf"
pacman_garuda ="/usr/share/arcolinux-tweak-tool/data/garuda/pacman.conf"
blank_pacman_arco ="/usr/share/arcolinux-tweak-tool/data/arco/blank/pacman.conf"
blank_pacman_eos ="/usr/share/arcolinux-tweak-tool/data/eos/blank/pacman.conf"
blank_pacman_garuda ="/usr/share/arcolinux-tweak-tool/data/garuda/blank/pacman.conf"
gtk3_settings = home + "/.config/gtk-3.0/settings.ini"
gtk2_settings = home + "/.gtkrc-2.0"
grub_theme_conf = "/boot/grub/themes/Vimix/theme.txt"
xfce_config = home + "/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml"
neofetch_config = home + "/.config/neofetch/config.conf"
lightdm_conf = "/etc/lightdm/lightdm.conf"
bd = ".att_backups"
config = home + "/.config/arcolinux-tweak-tool/settings.ini"
config_dir = home + "/.config/arcolinux-tweak-tool/"
polybar = home + "/.config/polybar/"
desktop = ""
autostart = home + "/.config/autostart/"
zsh_config = ""
fish_config = ""
if os.path.isfile(home + "/.config/fish/config.fish"):
    fish_config = home + "/.config/fish/config.fish"
if os.path.isfile(home + "/.zshrc"):
    zsh_config = home + "/.zshrc"
bash_config = ""
if os.path.isfile(home + "/.bashrc"):
    bash_config = home + "/.bashrc"
account_list = ["Standard","Administrator"]
i3wm_config = home + "/.config/i3/config"
awesome_config = home + "/.config/awesome/rc.lua"
qtile_config = home + "/.config/qtile/config.py"

seedhostmirror = "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
aarnetmirror = "Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"

atestrepo = "[arcolinux_repo_testing]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

arepo = "[arcolinux_repo]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

a3drepo = "[arcolinux_repo_3party]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

axlrepo = "[arcolinux_repo_xlarge]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

chaotics_repo = "[chaotic-aur]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/chaotic-mirrorlist"

endeavouros_repo = "[endeavouros]\n\
SigLevel = PackageRequired\n\
Include = /etc/pacman.d/endeavouros-mirrorlist"

nemesis_repo = "[nemesis_repo]\n\
SigLevel = Optional TrustedOnly\n\
Server = https://erikdubois.github.io/$repo/$arch"

arch_testing_repo = "[testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_core_repo = "[core]\n\
Include = /etc/pacman.d/mirrorlist"

arch_extra_repo = "[extra]\n\
Include = /etc/pacman.d/mirrorlist"

arch_community_testing_repo = "[community-testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_community_repo = "[community]\n\
Include = /etc/pacman.d/mirrorlist"

arch_multilib_testing_repo = "[multilib-testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_multilib_repo = "[multilib]\n\
Include = /etc/pacman.d/mirrorlist"


# Create log =====================================================

log_dir="/var/log/arcolinux/"
att_log_dir="/var/log/arcolinux/att/"

def create_log(self):
    print('Making log in /var/log/arcolinux')
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d-%H-%M-%S" )
    destination = att_log_dir + 'att-log-' + time
    command = 'sudo pacman -Q > ' + destination
    subprocess.call(command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    #GLib.idle_add(show_in_app_notification, self, "Log file created")


# Notification ===========================================================

def show_in_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    self.notification_label.set_markup("<span foreground=\"white\">" +
                                       message + "</span>")
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None


def permissions(dst):
    try:
        # original_umask = os.umask(0)
        # calls = subprocess.run(["sh", "-c", "cat /etc/passwd | grep " +
        #                         sudo_username],
        #                        shell=False,
        #                        stdout=subprocess.PIPE,
        #                        stderr=subprocess.STDOUT)
        groups = subprocess.run(["sh", "-c", "id " +
                                 sudo_username],
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for x in groups.stdout.decode().split(" "):
            if "gid" in x:
                g = x.split("(")[1]
                group = g.replace(")", "").strip()
        # print(group)
        # name = calls.stdout.decode().split(":")[0].strip()
        # group = calls.stdout.decode().split(":")[4].strip()

        subprocess.call(["chown", "-R",
                         sudo_username + ":" + group, dst], shell=False)

    except Exception as e:
        print(e)


def copy_func(src, dst, isdir=False):
    if isdir:
        subprocess.run(["cp", "-Rp", src, dst], shell=False)
    else:
        subprocess.run(["cp", "-p", src, dst], shell=False)
    


def MessageBox(self, title, message):
    md2 = Gtk.MessageDialog(parent=self,
                            flags=0,
                            message_type=Gtk.MessageType.INFO,
                            buttons=Gtk.ButtonsType.OK,
                            text=title)
    md2.format_secondary_markup(message)
    md2.run()
    md2.destroy()


def _get_position(lists, value):
    data = [string for string in lists if value in string]
    position = lists.index(data[0])
    return position


def do_pulse(data, prog):
    prog.pulse()
    return True


def install_alacritty(self):
    install = 'pacman -S alacritty --needed --noconfirm'

    if os.path.exists("/usr/bin/alacritty"):
        pass
    else:
        subprocess.call(install.split(" "),
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)


def install_zsh(self):
    install = 'pacman -S zsh zsh-completions zsh-syntax-highlighting arcolinux-zsh-git oh-my-zsh-git --needed --noconfirm'

    if os.path.exists("/usr/bin/zsh") and os.path.exists("/etc/skel/.zshrc") :
        pass
    else:
        subprocess.call(install.split(" "),
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)


# Desktop trasher =====================================================

def install_adt(self):
    install = 'pacman -S arcolinux-desktop-trasher-git --noconfirm'

    if os.path.exists("/usr/local/bin/arcolinux-desktop-trasher"):
        pass
    else:
        subprocess.call(install.split(" "),
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)

# GRUB CONF =====================================================

def get_grub_wallpapers():
    if os.path.isdir("/boot/grub/themes/Vimix"):
        lists = os.listdir("/boot/grub/themes/Vimix")

        rems = ['select_e.png', 'terminal_box_se.png', 'select_c.png',
                'terminal_box_c.png', 'terminal_box_s.png',
                'select_w.png', 'terminal_box_nw.png',
                'terminal_box_w.png', 'terminal_box_ne.png',
                'terminal_box_sw.png', 'terminal_box_n.png',
                'terminal_box_e.png']

        ext = ['.png', '.jpeg', '.jpg']

        new_list = [x for x in lists if x not in rems for y in ext if y in x]

        new_list.sort()
        return new_list


def set_grub_wallpaper(self, image):
    if os.path.isfile(grub_theme_conf):
        if not os.path.isfile(grub_theme_conf + ".bak"):
            shutil.copy(grub_theme_conf, grub_theme_conf + ".bak")
        try:
            with open(grub_theme_conf, "r") as f:
                lists = f.readlines()
                f.close()

            val = _get_position(lists, "desktop-image: ")
            lists[val] = "desktop-image: \"" + os.path.basename(image) + "\"" + "\n"

            with open(grub_theme_conf, "w") as f:
                f.writelines(lists)
                f.close()

            show_in_app_notification(self, "Settings Saved Successfully")
        except:  
            pass


def get_desktop(self):
    base_dir = os.path.dirname(os.path.realpath(__file__))

    desktop = subprocess.run(["sh", base_dir + "/get_desktop.sh", "-n"],
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    dsk = desktop.stdout.decode().strip().split("\n")
    self.desktop = dsk[-1].strip()

def signal_handler(sig, frame):
    print('\nATT is Closing.')
    os.unlink("/tmp/att.lock")
    Gtk.main_quit(0)

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if processName == pinfo['pid']:
                return True
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
