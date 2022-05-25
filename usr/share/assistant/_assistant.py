#!/usr/bin/env python3
import os
import distro
import subprocess
from subprocess import PIPE, STDOUT
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib

import _functions
import _GUI
import _splash
import _settings
import pacman
import signal
import sddm
import desktopr
import autostart
import zsh_theme
import user


base_dir = os.path.dirname(os.path.realpath(__file__))
pmf = pacman


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="Assistant")
        self.set_border_width(10)
        self.connect("delete-event", self.on_close)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file(os.path.join(base_dir, 'images/kayos.png'))
        self.set_default_size(800, 700)

        self.opened = True
        self.firstrun = True
        self.desktop = ""
        self.timeout_id = None

        self.desktop_status = Gtk.Label()
        self.image_DE = Gtk.Image()

        self.grub_image_path = ""
        self.fb = Gtk.FlowBox()
        # _functions.test("/etc/skel/.config/bspwm")
        splScr = _splash.splashScreen()

        while Gtk.events_pending():
            Gtk.main_iteration()

        t = _functions.threading.Thread(target=_functions.get_desktop,
                                       args=(self,))
        t.daemon = True
        t.start()
        t.join()

        if not os.path.isdir(_functions.log_dir):
            try:
                os.mkdir(_functions.log_dir)
            except Exception as e:
                print(e)

        if not os.path.isdir(_functions.att_log_dir):
            try:
                os.mkdir(_functions.att_log_dir)
            except Exception as e:
                print(e)

        if os.path.exists("/usr/bin/sddm"):
            if not os.path.isdir(_functions.sddm_default_d2_dir):
                try:
                    os.mkdir(_functions.sddm_default_d2_dir)
                except Exception as e:
                    print(e)

            if not _functions.os.path.exists(_functions.sddm_conf):
                try:
                    _functions.shutil.copy(_functions.sddm_default_d_sddm_original_1,
                                          _functions.sddm_default_d1)
                    _functions.shutil.copy(_functions.sddm_default_d_sddm_original_2,
                                          _functions.sddm_default_d2)
                except OSError as e:
                    #This will ONLY execute if the sddm files and the underlying sddm files do not exist
                    if e.errno == 2:
                        command = '/usr/local/bin/arcolinux-fix-sddm-config'
                        _functions.subprocess.call(command,
                                        shell=True,
                                        stdout=_functions.subprocess.PIPE,
                                        stderr=_functions.subprocess.STDOUT)
                        print("The SDDM files in your installation either did not exist, or were corrupted.")
                        print("These files have now been restored. Please re-run the Tweak Tool if it did not load for you.")


            if  os.path.getsize(_functions.sddm_conf) == 0:
                _functions.shutil.copy(_functions.sddm_default_d_sddm_original_1,
                                      _functions.sddm_default_d1)
                _functions.shutil.copy(_functions.sddm_default_d_sddm_original_2,
                                      _functions.sddm_default_d2)
        if _functions.os.path.isfile(_functions.sddm_conf):
            session_exists = sddm.check_sddmk_session("Session=")
            if session_exists is False:
                sddm.insert_session("#Session=")

        if _functions.os.path.isfile(_functions.sddm_conf):
            user_exists = sddm.check_sddmk_user("User=")
            if user_exists is False:
                sddm.insert_user("#User=")

        if not _functions.os.path.exists(_functions.home + "/.config/autostart"):
            # _functions.MessageBox(self, "oops!",
            #                      "some directories are missing. run 'skel' in terminal and try starting again.")
            # Gtk.main_quit()
            _functions.os.makedirs(_functions.home + "/.config/autostart", 0o766)
            _functions.permissions(_functions.home + "/.config/autostart")

        #if not _functions.os.path.isdir(_functions.home + "/" +
        #                               _functions.bd):
            #_functions.os.makedirs(_functions.home + "/" +
            #                      _functions.bd, 0o766)
            #_functions.permissions(_functions.home + "/" +
            #                      _functions.bd)

        if not _functions.os.path.isdir(_functions.home +
                                       "/.config/arcolinux-tweak-tool"):

            _functions.os.makedirs(_functions.home +
                                  "/.config/arcolinux-tweak-tool", 0o766)
            _functions.permissions(_functions.home +
                                  "/.config/arcolinux-tweak-tool")
        # Force Permissions
        a1 = _functions.os.stat(_functions.home + "/.config/autostart")
        a2 = _functions.os.stat(_functions.home + "/.config/arcolinux-tweak-tool")
        #a3 = _functions.os.stat(_functions.home + "/" + _functions.bd)
        autostart = a1.st_uid
        att = a2.st_uid
        #backup = a3.st_uid

        #fixing root permissions if the folder exists
        #can be removed later - 02/11/2021 startdate
        if os.path.exists(_functions.home + "/.config-att"):
            _functions.permissions(_functions.home + "/.config-att")

        if autostart == 0:
            _functions.permissions(_functions.home + "/.config/autostart")
            print("Fix autostart permissions...")
        if att == 0:
            _functions.permissions(_functions.home + "/.config/arcolinux-tweak-tool")
            print("Fix arcolinux-tweak-tool permissions...")
        #if backup == 0:
        #    _functions.permissions(_functions.home + "/" + _functions.bd)
        #    print("Fix .att_backup permissions...")

        # if not _functions.path_check(_functions.config_dir + "images"):
        #     _functions.os.makedirs(_functions.config_dir + "images", 0o766)
        #     for x in _functions.os.listdir(base_dir + "/polybar_data/"):
        #         _functions.copy_func(base_dir + "/polybar_data/" + x, _functions.config_dir + "images", False)
        #     _functions.permissions(_functions.config_dir + "images")
        # else:
        #     for x in _functions.os.listdir(base_dir + "/polybar_data/"):
        #         _functions.copy_func(base_dir + "/polybar_data/" + x, _functions.config_dir + "images", False)
        #     _functions.permissions(_functions.config_dir + "images")

        if not _functions.os.path.isfile(_functions.config):
            key = {"theme": ""}
            _settings.make_file("TERMITE", key)
            _functions.permissions(_functions.config)

        _GUI.GUI(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango)

#       #========================ARCO REPO=============================

        arco_testing = pacman.check_repo("[arcolinux_repo_testing]")
        arco_base = pacman.check_repo("[arcolinux_repo]")
        arco_3p = pacman.check_repo("[arcolinux_repo_3party]")
        arco_xl = pacman.check_repo("[arcolinux_repo_xlarge]")

#       #========================ARCH REPO=============================
                
        arch_testing = pacman.check_repo("[testing]")
        arch_core = pacman.check_repo("[core]")
        arch_extra = pacman.check_repo("[extra]")
        arch_community_testing = pacman.check_repo("[community-testing]")
        arch_community = pacman.check_repo("[community]")
        arch_multilib_testing = pacman.check_repo("[multilib-testing]")
        arch_multilib = pacman.check_repo("[multilib]")

#       #========================OTHER REPO=============================
        
        chaotics_repo = pacman.check_repo("[chaotic-aur]")
        endeavouros_repo = pacman.check_repo("[endeavouros]")
        nemesis_repo = pacman.check_repo("[nemesis_repo]")
        
#       #========================ARCO MIRROR=============================
        if os.path.isfile(_functions.arcolinux_mirrorlist):
            arco_mirror_seed = pacman.check_mirror("Server = https://ant.seedhost.eu/arcolinux/$repo/$arch")
            arco_mirror_gitlab = pacman.check_mirror("Server = https://gitlab.com/arcolinux/$repo/-/raw/main/$arch")
            arco_mirror_belnet = pacman.check_mirror("Server = https://ftp.belnet.be/arcolinux/$repo/$arch")
            arco_mirror_codeberg = pacman.check_mirror("Server = https://codeberg.org/arcolinux/$repo/media/branch/main/$arch")
            arco_mirror_funami = pacman.check_mirror("Server = https://mirror.funami.tech/arcolinux/$repo/$arch")
            arco_mirror_jingk = pacman.check_mirror("Server = https://mirror.jingk.ai/arcolinux/$repo/$arch")
            arco_mirror_aarnet = pacman.check_mirror("Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch")
            arco_mirror_github = pacman.check_mirror("Server = https://arcolinux.github.io/$repo/$arch")



#       #========================ARCH LINUX REPO SET TOGGLE==================
        
        self.checkbutton1.set_active(arch_testing)
        self.checkbutton2.set_active(arch_core)
        self.checkbutton3.set_active(arch_extra)
        self.checkbutton4.set_active(arch_community_testing)
        self.checkbutton5.set_active(arch_community)
        self.checkbutton6.set_active(arch_multilib_testing)
        self.checkbutton7.set_active(arch_multilib)


        splScr.destroy()

# #---------------------------------------------------------------------------------------  
        # self.sessions = Gtk.ComboBoxText()
        # self.autologin = Gtk.Switch()
        # self.autologin.connect("notify::active", self.on_autologin_activated)


        # if _functions.os.path.isfile(_functions.lightdm_conf):          
        #     if _functions.os.path.isfile(_functions.lightdm_conf):
        #         with open(_functions.lightdm_conf, "r") as f:
        #             get_lines = f.readlines()
        #             f.close()

        #     pos = _functions._get_position(get_lines, "autologin-user=")
        #     check_lightdm = get_lines[pos].strip()
        

        #     if "#" in check_lightdm:
        #         self.autologin.set_active(False)
        #         self.sessions.set_sensitive(False)
        #     else:
        #         self.autologin.set_active(True)
        #         self.sessions.set_sensitive(True)

        if not "plasma" in self.desktop.lower():
            if _functions.os.path.isfile(_functions.sddm_conf):
                if "#" in sddm.check_sddm(sddm.get_sddm_lines(_functions.sddm_conf),"User="):
                    self.autologin_sddm.set_active(False)
                    self.sessions_sddm.set_sensitive(False)
                else:
                    self.autologin_sddm.set_active(True)
                    self.sessions_sddm.set_sensitive(True)
            if _functions.os.path.isfile(_functions.sddm_default):
                read_cursor_name=sddm.check_sddm(sddm.get_sddm_lines(_functions.sddm_default),"CursorTheme=").split("=")[1]
                self.entry_cursor_name.set_text(read_cursor_name)

        if not os.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w") as f:
                f.write("")


#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------



    def on_close(self, widget, data):
        os.unlink("/tmp/att.lock")
        Gtk.main_quit()

    def create_autostart_columns(self, treeView):
        rendererText = Gtk.CellRendererText()
        renderer_checkbox = Gtk.CellRendererToggle()
        column_checkbox = Gtk.TreeViewColumn("", renderer_checkbox, active=0)
        renderer_checkbox.connect("toggled", self.renderer_checkbox, self.startups)
        renderer_checkbox.set_activatable(True)
        column_checkbox.set_sort_column_id(0)

        column = Gtk.TreeViewColumn("Name", rendererText, text=1)
        column.set_sort_column_id(1)

        column2 = Gtk.TreeViewColumn("Comment", rendererText, text=2)
        column2.set_sort_column_id(2)

        treeView.append_column(column_checkbox)
        treeView.append_column(column)
        treeView.append_column(column2)

    def create_columns(self, treeView):
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def renderer_checkbox(self, renderer, path, model):
        if path is not None:
            it = model.get_iter(path)
            model[it][0] = not model[it][0]

    def on_activated(self, treeview, path, column):
        failed = False
        treestore, selected_treepaths = treeview.get_selection().get_selected_rows()
        selected_treepath = selected_treepaths[0]
        selected_row = treestore[selected_treepath]
        bool = selected_row[0]
        text = selected_row[1]

        if bool:
            bools = False
        else:
            bools = True

        with open(_functions.home + "/.config/autostart/" + text + ".desktop", "r") as f:
            lines = f.readlines()
            f.close()
        try:
            pos = _functions._get_position(lines, "Hidden=")
        except:
            failed = True
            with open(_functions.home + "/.config/autostart/" + text + ".desktop", "a") as f:
                f.write("Hidden=" + str(bools))
                f.close()
        if not failed:
            val = lines[pos].split("=")[1].strip()
            lines[pos] = lines[pos].replace(val, str(bools).lower())
            with open(_functions.home + "/.config/autostart/" + text + ".desktop", "w") as f:
                f.writelines(lines)
                f.close()

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

# =====================================================
#               PACMAN FUNCTIONS
# =====================================================

    def on_pacman_toggle1(self, widget, active):
        if not pacman.repo_exist("[testing]"):
            pacman.append_repo(self, _functions.arch_testing_repo)
        else:
            if self.opened is False:
                pacman.toggle_test_repos(self, widget.get_active(),
                                      "testing")
            
    def on_pacman_toggle2(self, widget, active):
        if not pacman.repo_exist("[core]"):
            pacman.append_repo(self, _functions.arch_core_repo)
        else:
            if self.opened is False:
                pacman.toggle_test_repos(self, widget.get_active(),
                                      "core")

    def on_pacman_toggle3(self, widget, active):
        if not pacman.repo_exist("[extra]"):
            pacman.append_repo(self, _functions.arch_extra_repo)
        else:
            if self.opened is False:
                pacman.toggle_test_repos(self, widget.get_active(),
                                      "extra")

    def on_pacman_toggle4(self, widget, active):
        if not pacman.repo_exist("[community-testing]"):
            pacman.append_repo(self, _functions.arch_community_testing_repo)
        else:
            if self.opened is False:
                pacman.toggle_test_repos(self, widget.get_active(),
                                      "community-testing")

    def on_pacman_toggle5(self, widget, active):
        if not pacman.repo_exist("[community]"):
            pacman.append_repo(self, _functions.arch_community_repo)
        else:        
            if self.opened is False:
                pacman.toggle_test_repos(self, widget.get_active(),
                                      "community")

    def on_pacman_toggle6(self, widget, active):
        if not pacman.repo_exist("[multilib-testing]"):
            pacman.append_repo(self, _functions.arch_multilib_testing_repo)
        else:        
            if self.opened is False:
                pacman.toggle_test_repos(self, widget.get_active(), "multilib-testing")
            

    def on_pacman_toggle7(self, widget, active):
        if not pacman.repo_exist("[multilib]"):
            pacman.append_repo(self, _functions.arch_multilib_repo)
        else:        
            if self.opened is False:
                pacman.toggle_test_repos(self, widget.get_active(), "multilib")

      
    def apply_custom_repo(self, widget):
        self.text = self.ctextbox.get_buffer()
        startiter, enditer = self.text.get_bounds()

        if not len(self.text.get_text(startiter, enditer, True)) < 5:
            print(self.text.get_text(startiter, enditer, True))
            pacman.append_repo(
                self, self.text.get_text(startiter, enditer, True))


    def blank_settings(source,target):
        _functions.shutil.copy(_functions.pacman, _functions.pacman + ".bak")
        if distro.id() == "arcolinux":
            _functions.shutil.copy(_functions.blank_pacman_arco, _functions.pacman)
        if distro.id() == "endeavouros":
            _functions.shutil.copy(_functions.blank_pacman_eos, _functions.pacman)
        if distro.id() == "garuda":
            _functions.shutil.copy(_functions.blank_pacman_garuda, _functions.pacman)


    def reset_settings(self, widget, filez):  # noqa
        if os.path.isfile(filez + ".bak"):
            _functions.shutil.copy(filez + ".bak", filez)
            _functions.show_in_app_notification(self, "Default Settings Applied")

        if filez == _functions.pacman:
            if distro.id() == "arcolinux":
                _functions.shutil.copy(_functions.pacman_arco, _functions.pacman)
            if distro.id() == "endeavouros":
                _functions.shutil.copy(_functions.pacman_eos, _functions.pacman)
            if distro.id() == "garuda":
                _functions.shutil.copy(_functions.pacman_garuda, _functions.pacman)
             
            _functions.show_in_app_notification(self, "Default Settings Applied")
        

#   #====================================================================
#   #                       GRUB
#   #====================================================================

    def on_grub_item_clicked(self, widget, data):
        for x in data:
            self.grub_image_path = x.get_name()

    def on_set_grub_wallpaper(self, widget):
        # _functions.set_grub_wallpaper(self,
        #                              self.grub_theme_combo.get_active_text())
        _functions.set_grub_wallpaper(self,
                                     self.grub_image_path)

    def on_reset_grub_wallpaper(self, widget):
        if os.path.isfile(_functions.grub_theme_conf + ".bak"):
            _functions.shutil.copy(_functions.grub_theme_conf + ".bak",
                                  _functions.grub_theme_conf)
        self.pop_themes_grub(self.grub_theme_combo,
                             _functions.get_grub_wallpapers(), True)
        _functions.show_in_app_notification(self, "Default Settings Applied")

    def pop_themes_grub(self, combo, lists, start):
        if os.path.isfile(_functions.grub_theme_conf):
            combo.get_model().clear()
            with open(_functions.grub_theme_conf, "r") as f:
                listss = f.readlines()
                f.close()

            val = _functions._get_position(listss, "desktop-image: ")
            bg_image = listss[val].split(" ")[1].replace("\"", "").strip()

            for x in self.fb.get_children():
                self.fb.remove(x)

            for x in lists:
                pb = GdkPixbuf.Pixbuf().new_from_file_at_size("/boot/grub/themes/Vimix/" + x, 128, 128) # noqa
                pimage = Gtk.Image()
                pimage.set_name("/boot/grub/themes/Vimix/" + x)
                pimage.set_from_pixbuf(pb)
                self.fb.add(pimage)
                pimage.show_all()
            # for i in range(len(lists)):
            #     combo.append_text(lists[i])
            #     if start is True:
            #         if(lists[i] == bg_image):
            #             combo.set_active(i)
            #     else:
            #         if(lists[i] == os.path.basename(self.tbimage.get_text())):
            #             combo.set_active(i)

    def on_grub_theme_change(self, widget):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf().new_from_file_at_size('/boot/grub/themes/Vimix/' +  # noqa
                                                               widget.get_active_text(),  # noqa
                                                               645, 645)
            print(widget.get_active_text())
            self.image_grub.set_from_pixbuf(pixbuf3)
        except Exception as e:
            print(e)

    def on_import_wallpaper(self, widget):
        text = self.tbimage.get_text()
        if len(text) > 1:
            print(os.path.basename(text))
            _functions.shutil.copy(text, '/boot/grub/themes/Vimix/' +
                                  os.path.basename(text))
            self.pop_themes_grub(self.grub_theme_combo,
                                 _functions.get_grub_wallpapers(), False)

    def on_remove_wallpaper(self, widget):
        widget.set_sensitive(False)
        if os.path.isfile(self.grub_image_path):

        # if os.path.isfile('/boot/grub/themes/Vimix/' +
        #                   self.grub_theme_combo.get_active_text()):
            excludes = ["archlinux03.jpg", "archlinux04.jpg",
                        "archlinux06.jpg", "archlinux07.jpg",
                        "arcolinux01.jpg", "arcolinux02.jpg",
                        "arcolinux03.jpg", "arcolinux04.jpg",
                        "arcolinux05.jpg", "arcolinux06.jpg",
                        "arcolinux07.jpg", "arcolinux08.jpg",
                        "background-slaze.jpg", "background-stylish.jpg",
                        "background-tela.jpg", "background-vimix.jpg",
                        "archlinux01.png",
                        "archlinux02.png", "archlinux05.png",
                        "arcolinux09.png",
                        "arcolinux10.png", "arcolinux11.png", "arcolinux.png",
                        "background.png"]

            # if not self.grub_theme_combo.get_active_text() in excludes:
            if not _functions.os.path.basename(self.grub_image_path) in excludes:
                # os.unlink('/boot/grub/themes/Vimix/' +
                #           self.grub_theme_combo.get_active_text())
                os.unlink(self.grub_image_path)
                self.pop_themes_grub(self.grub_theme_combo,
                                     _functions.get_grub_wallpapers(),
                                     True)
                _functions.show_in_app_notification(self,
                                                   "Wallpaper removed successfully")  # noqa
            else:
                _functions.show_in_app_notification(self,
                                                   "You can not remove that wallpaper")  # noqa
        widget.set_sensitive(True)

    def on_choose_wallpaper(self, widget):
        dialog = Gtk.FileChooserDialog(
                                       title="Please choose a file",
                                       action=Gtk.FileChooserAction.OPEN,)
        filter = Gtk.FileFilter()
        filter.set_name("IMAGE Files")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpg")
        filter.add_mime_type("image/jpeg")
        dialog.set_filter(filter)
        dialog.set_current_folder(_functions.home)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open",
                           Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_cb)

        dialog.show()

    def open_response_cb(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.tbimage.set_text(dialog.get_filename())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def on_click_install_arco_vimix_clicked(self, desktop):
        command = 'pacman -S arcolinux-grub-theme-vimix-git --noconfirm'
        _functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)

        GLib.idle_add(_functions.show_in_app_notification, self, "Vimix has been installed - restart ATT")


#    #====================================================================
#    #                       ZSH THEMES
#    #====================================================================

    def on_zsh_apply(self, widget):
        if self.zsh_themes.get_active_text() is not None:
            widget.set_sensitive(False)
            zsh_theme.set_config(self, self.zsh_themes.get_active_text())
            widget.set_sensitive(True)

    def on_zsh_reset(self, widget):
        if os.path.isfile(_functions.zsh_config + ".bak"):
            _functions.shutil.copy(_functions.zsh_config + ".bak",
                                  _functions.zsh_config)
            _functions.show_in_app_notification(self,
                                               "Default Settings Applied")
    def tozsh_apply(self,widget):
        # install missing applications for ArcoLinuxD
        _functions.install_zsh(self)
        # first make backup if there is a file
        if not _functions.os.path.isfile(_functions.home + "/.zshrc" + ".bak") and _functions.os.path.isfile(_functions.home + "/.zshrc"):
            _functions.shutil.copy(_functions.home + "/.zshrc",
                              _functions.home + "/.zshrc" + ".bak")
            _functions.permissions(_functions.home + "/.zshrc.bak")
        if not _functions.os.path.isfile(_functions.home + "/.zshrc"):
            _functions.shutil.copy("/etc/skel/.zshrc",
                              _functions.home + "/.zshrc")
            _functions.permissions(_functions.home + "/.zshrc")

        command = 'sudo chsh ' + _functions.sudo_username + ' -s /bin/zsh'
        _functions.subprocess.call(command,
                        shell=True,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Shell changed for user - logout")

    def tobash_apply(self,widget):
        command = 'sudo chsh ' + _functions.sudo_username + ' -s /bin/bash'
        _functions.subprocess.call(command,
                        shell=True,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Shell changed for user - logout")

    #The intent behind this function is to be a centralised image changer for all portions of ATT that need it
    #Currently utilising an if tree - this is not best practice: it should be a match: case tree.
    #But I have not yet got that working.
    def update_image(self, widget, image, theme_type, att_base, image_width, image_height):
        sample_path = ""
        preview_path = ""
        random_option = False
        if theme_type == "zsh":
            sample_path = att_base+"/images/zsh-sample.png"
            preview_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
            if widget.get_active_text() == "random":
                random_option = True
        elif theme_type == "qtile":
            sample_path = att_base+"/images/qtile-sample.jpg"
            preview_path = att_base+"/themer_data/qtile/"+widget.get_active_text() + ".jpg"
        elif theme_type == "i3":
            sample_path = att_base+"/images/i3-sample.jpg"
            preview_path = att_base+"/themer_data/i3/"+widget.get_active_text() + ".jpg"
        elif theme_type == "awesome":
        #Awesome section doesn't use a ComboBoxText, but a ComboBox - which has different properties.
            tree_iter = self.awesome_combo.get_active_iter()
            if tree_iter is not None:
                model = self.awesome_combo.get_model()
                row_id, name = model[tree_iter][:2]

            sample_path = att_base+"/images/i3-sample.jpg"
            preview_path = att_base+"/themer_data/awesomewm/"+name+".jpg"
        elif theme_type == "neofetch":
            sample_path = att_base + widget.get_active_text()
            preview_path = att_base + widget.get_active_text()
        else:
            print("Function update_image passed an incorrect value for theme_type. Value passed was: " + theme_type)
            print("Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height.")

        source_pixbuf = image.get_pixbuf()
        if os.path.isfile(preview_path) and not random_option:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(preview_path, image_width, image_height)
        else:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(sample_path, image_width, image_height)
        image.set_from_pixbuf(pixbuf)


#    #====================================================================
#    #                       ARCOLINUX MIRRORLIST
#    #===================================================================

    def on_click_reset_arcolinux_mirrorlist(self, widget):
        if not _functions.os.path.isfile(_functions.arcolinux_mirrorlist + ".bak"):
            _functions.shutil.copy(_functions.arcolinux_mirrorlist,
                                  _functions.arcolinux_mirrorlist + ".bak")

        if _functions.os.path.isfile(_functions.arcolinux_mirrorlist_original):
            _functions.shutil.copy(_functions.arcolinux_mirrorlist_original,
                                  _functions.arcolinux_mirrorlist)
            _functions.show_in_app_notification(self, "Original ArcoLinux mirrorlist is applied")



    # ====================================================================
    #                       SDDM
    # ====================================================================

    def on_click_sddm_apply(self, widget):
        #if not _functions.os.path.isfile(_functions.sddm_conf + ".bak"):
        #    _functions.shutil.copy(_functions.sddm_conf,
        #                          _functions.sddm_conf + ".bak")


        if (self.sessions_sddm.get_active_text() is not None and self.theme_sddm.get_active_text() is not None and self.autologin_sddm.get_active() is True) or (self.autologin_sddm.get_active() is False and self.theme_sddm.get_active_text() is not None) :
            t1 = _functions.threading.Thread(target=sddm.set_sddm_value,
                                            args=(self,
                                                sddm.get_sddm_lines(_functions.sddm_conf),  # noqa
                                                _functions.sudo_username,
                                                self.sessions_sddm.get_active_text(),
                                                self.autologin_sddm.get_active(),
                                                self.theme_sddm.get_active_text()))
            t1.daemon = True
            t1.start()

            t1 = _functions.threading.Thread(target=sddm.set_sddm_cursor,
                                            args=(self,
                                            sddm.get_sddm_lines(_functions.sddm_default),  # noqa
                                            self.entry_cursor_name.get_text()))
            t1.daemon = True
            t1.start()

            GLib.idle_add(_functions.show_in_app_notification, self, "Settings Saved Successfully")

        else:
            _functions.show_in_app_notification(self, "You need to select desktop and/or theme first")

    def on_click_sddm_reset(self, widget):
        #if _functions.os.path.isfile(_functions.sddm_conf + ".bak"):
        #    _functions.shutil.copy(_functions.sddm_conf + ".bak",
        #                          _functions.sddm_conf)
        if _functions.os.path.isfile(_functions.sddm_conf):
            if "#" in sddm.check_sddm(sddm.get_sddm_lines(_functions.sddm_conf), "User="):  # noqa
                self.autologin_sddm.set_active(False)
            else:
                self.autologin_sddm.set_active(True)
            _functions.show_in_app_notification(self, "Your sddm.conf backup is now applied")
        else:
            _functions.show_in_app_notification(self, "We did not find a backup file for sddm.conf")

    def on_click_sddm_reset_original(self, widget):
        if _functions.sddm_conf == "/etc/sddm.conf.d/kde_settings.conf":
            _functions.shutil.copy(_functions.sddm_default_d_sddm_original_1,
                                  _functions.sddm_default_d1)
            _functions.shutil.copy(_functions.sddm_default_d_sddm_original_2,
                                  _functions.sddm_default_d2)
        else:
            _functions.shutil.copy(_functions.sddm_default_original,
                                  _functions.sddm_default)

        if "#" in sddm.check_sddm(sddm.get_sddm_lines(_functions.sddm_conf), "User="):  # noqa
            self.autologin_sddm.set_active(False)
        else:
            self.autologin_sddm.set_active(True)

        _functions.show_in_app_notification(self, "The ArcoLinux sddm.conf is now applied")

    def on_click_no_sddm_reset_original(self, widget):
        if _functions.os.path.isfile(_functions.sddm_default_d_sddm_original_1):
            _functions.shutil.copyfile(_functions.sddm_default_d_sddm_original_1,
                                  _functions.sddm_default_d1)
            _functions.shutil.copyfile(_functions.sddm_default_d_sddm_original_2,
                                  _functions.sddm_default_d2)

        _functions.show_in_app_notification(self, "The ArcoLinux sddm.conf is now applied")

    def on_autologin_sddm_activated(self, widget, gparam):
        if widget.get_active():
            self.sessions_sddm.set_sensitive(True)
        else:
            self.sessions_sddm.set_sensitive(False)

    def on_click_install_sddm_themes(self,widget):
        command = 'pacman -S arcolinux-meta-sddm-themes --needed --noconfirm'
        _functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "ArcoLinux Sddm Themes Installed")

    def on_click_remove_sddm_themes(self,widget):
        command = 'pacman -Rss arcolinux-meta-sddm-themes --noconfirm'
        _functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "ArcoLinux Sddm themes were removed")

        if self.keep_default_theme.get_active() is True:
            command = 'pacman -S arcolinux-sddm-sugar-candy-git --needed --noconfirm'
            _functions.subprocess.call(command.split(" "),
                            shell=False,
                            stdout=_functions.subprocess.PIPE,
                            stderr=_functions.subprocess.STDOUT)
            GLib.idle_add(_functions.show_in_app_notification, self, "ArcoLinux Sddm themes were removed except default")

    def on_click_att_sddm_clicked(self, desktop):
        command = 'pacman -S sddm --noconfirm --needed'
        _functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)

        command = 'systemctl enable sddm.service -f'
        _functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)

        GLib.idle_add(_functions.show_in_app_notification, self, "Sddm has been installed and enabled - reboot")

    def on_click_sddm_enable(self, desktop):
        command = 'systemctl enable sddm.service -f'
        _functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Sddm has been enabled - reboot")

    def on_launch_adt_clicked(self, desktop):
        _functions.install_adt(self)
        subprocess.Popen("/usr/local/bin/arcolinux-desktop-trasher")
        GLib.idle_add(_functions.show_in_app_notification, self, "ArcoLinux Desktop Trasher launched")

    def on_refresh_att_clicked(self, desktop):
        os.unlink("/tmp/att.lock")
        _functions.restart_program()

    # ====================================================================
    #                       USER
    # ====================================================================

    def on_click_user_apply(self, widget):
        user.create_user(self)

    # ====================================================================
    #                       FIXES
    # ====================================================================

    def on_click_fix_pacman_keys(self,widget):
        _functions.install_alacritty(self)
        _functions.subprocess.call("alacritty -e /usr/local/bin/arcolinux-fix-pacman-databases-and-keys",
                        shell=True,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Pacman keys fixed")

    def on_click_fix_osbeck(self,widget):
        command = '/usr/local/bin/arcolinux-osbeck-as-mirror'
        _functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Osbeck set as Arch Linux")

    def on_click_fix_mirrors(self,widget):
        _functions.install_alacritty(self)
        _functions.subprocess.call("alacritty -e /usr/local/bin/arcolinux-get-mirrors",
                        shell=True,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Fastest Arch Linux servers saved")

    def on_click_fix_sddm_conf(self,widget):
        command = '/usr/local/bin/arcolinux-fix-sddm-config'
        _functions.subprocess.call(command,
                        shell=True,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Saved the original /etc/sddm.conf")

    def on_click_fix_pacman_conf(self,widget):
        command = '/usr/local/bin/arcolinux-fix-pacman-conf'
        _functions.subprocess.call(command,
                        shell=True,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Saved the original /etc/pacman.conf")

    def on_click_fix_pacman_gpg_conf(self,widget):
        command = '/usr/local/bin/arcolinux-fix-pacman-gpg-conf'
        _functions.subprocess.call(command,
                        shell=True,
                        stdout=_functions.subprocess.PIPE,
                        stderr=_functions.subprocess.STDOUT)
        GLib.idle_add(_functions.show_in_app_notification, self, "Saved the original /etc/pacman.d/gnupg/gpg.conf")


# Desktop ====================================================================

    def on_d_combo_changed(self, widget):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf().new_from_file_at_size(base_dir +
                                                            "/desktop_data/" +
                                                            self.d_combo.get_active_text() + ".jpg",  # noqa
                                                            345,
                                                            345)
            self.image_DE.set_from_pixbuf(pixbuf3)
        except:  # noqa
            self.image_DE.set_from_pixbuf(None)
        if desktopr.check_desktop(self.d_combo.get_active_text()):
            self.desktop_status.set_text("This desktop is installed")
        else:
            self.desktop_status.set_text("This desktop is NOT installed")

    def on_uninstall_clicked(self, widget):
        secs = _settings.read_section()
        if "DESKTOP" in secs:
            desktopr.uninstall_desktop_check(self,
                                             self.d_combo.get_active_text())
        else:
            _functions.show_in_app_notification(self,
                                               "You Must Set Default First")

    def on_install_clicked(self, widget, state):
        _functions.create_log(self)
        # if desktopr.check_desktop(self.d_combo.get_active_text()) is not True:
        print("installing {}".format(self.d_combo.get_active_text()))
        desktopr.check_lock(self,self.d_combo.get_active_text(),state)

        # desktopr.install_desktop(self, self.d_combo.get_active_text())

    def on_default_clicked(self, widget):
        _functions.create_log(self)
        if desktopr.check_desktop(self.d_combo.get_active_text()) is True:
            secs = _settings.read_section()
            if "DESKTOP" in secs:
                _settings.write_settings("DESKTOP",
                                        "default",
                                        self.d_combo.get_active_text())
            else:
                _settings.new_settings("DESKTOP",
                                      {"default": self.d_combo.get_active_text()})
        else:
            _functions.show_in_app_notification(self,
                                               "That desktop is not installed")

# Autostart ====================================================================

    def on_comment_changed(self, widget):
        if len(self.txtbox1.get_text()) >= 3 and len(self.txtbox2.get_text()) >= 3:
            self.abutton.set_sensitive(True)

    def on_auto_toggle(self, widget, data, lbl):
        failed = False
        try:
            with open(_functions.autostart + lbl + ".desktop", "r") as f:
                lines = f.readlines()
                f.close()
            try:
                pos = _functions._get_position(lines, "Hidden=")
            except:
                failed = True
                with open(_functions.autostart + lbl + ".desktop", "a") as f:
                    f.write("Hidden=" + str(not widget.get_active()).lower())
                    f.close()
        except:
            pass
        if not failed:
            val = lines[pos].split("=")[1].strip()
            lines[pos] = lines[pos].replace(val, str(not widget.get_active()).lower())
            with open(_functions.autostart + lbl + ".desktop", "w") as f:
                f.writelines(lines)
                f.close()

    def on_auto_remove_clicked(self, widget, data, listbox, lbl):
        os.unlink(_functions.autostart + lbl + ".desktop")
        self.vvbox.remove(listbox)

    def clear_autostart(self):
        for x in self.vvbox.get_children():
            self.vvbox.remove(x)

    def load_autostart(self, files):
        self.clear_autostart()

        for x in files:
            self.add_row(x)

    def add_row(self, x):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        lbl = Gtk.Label(xalign=0)
        lbl.set_text(x)

        swtch = Gtk.Switch()
        swtch.connect("notify::active", self.on_auto_toggle, lbl.get_text())
        swtch.set_active(autostart.get_startups(self, lbl.get_text()))

        listbox = Gtk.ListBox()

        fbE = Gtk.EventBox()

        pbfb = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(base_dir, 'images/remove.png'), 28, 28)
        fbimage = Gtk.Image().new_from_pixbuf(pbfb)

        fbE.add(fbimage)

        fbE.connect("button_press_event",
                    self.on_auto_remove_clicked,
                    listbox,
                    lbl.get_text())

        fbE.set_property("has-tooltip", True)

        fbE.connect("query-tooltip", self.tooltip_callback, "Remove")

        hbox.pack_start(lbl, False, False, 0)
        hbox.pack_end(fbE, False, False, 0)
        vbox2.pack_start(swtch, False, False, 10)
        hbox.pack_end(vbox2, False, False, 0)

        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox1.pack_start(hbox, False, False, 5)

        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        listboxrow = Gtk.ListBoxRow()
        listboxrow.add(vbox1)
        listbox.add(listboxrow)

        self.vvbox.pack_start(listbox, False, False, 0)
        self.vvbox.show_all()

    def on_remove_auto(self, widget):
        selection = self.treeView4.get_selection()
        model, paths = selection.get_selected_rows()

        # Get the TreeIter instance for each path
        for path in paths:
            iter = model.get_iter(path)
            # Remove the ListStore row referenced by iter
            value = model.get_value(iter, 1)
            model.remove(iter)
            _functions.os.unlink(_functions.home + "/.config/autostart/" + value + ".desktop")  #  noqa

    def on_add_autostart(self, widget):
        if len(self.txtbox1.get_text()) > 1 and len(self.txtbox2.get_text()) > 1:  # noqa
            autostart.add_autostart(self, self.txtbox1.get_text(),
                                    self.txtbox2.get_text(),
                                    self.txtbox3.get_text())

    def on_exec_browse(self, widget):

        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            action=Gtk.FileChooserAction.OPEN)

        dialog.set_select_multiple(False)
        dialog.set_show_hidden(False)
        dialog.set_current_folder(_functions.home)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open",
                           Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_auto)

        dialog.show()

    def open_response_auto(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            print(dialog.get_filenames())
            foldername = dialog.get_filenames()
            # for item in foldername:
            self.txtbox2.set_text(foldername[0])
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()



if __name__ == "__main__":
    signal.signal(signal.SIGINT, _functions.signal_handler)
    #These lines offer protection and grace when a kernel has obfuscated or removed basic OS functionality.
    os_function_support = True
    try:
        os.getlogin()
    except:
        os_function_support = False
    if not os.path.isfile("/tmp/att.lock") and os_function_support:
        with open("/tmp/att.pid", "w") as f:
            f.write(str(os.getpid()))
            f.close()
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(base_dir + "/_att.css")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        w = Main()
        w.show_all()
        Gtk.main()
    else:
        md = ""

        if os_function_support:
            md = Gtk.MessageDialog(parent=Main(),
                                   flags=0,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.YES_NO,
                                   text="Lock File Found")
            md.format_secondary_markup(
                "The lock file has been found. This indicates there is already an instance of <b>ArchLinux Tweak Tool</b> running.\n\
    click yes to remove the lock file and try running again")  # noqa
        else:
            md = Gtk.MessageDialog(parent=Main(),
                                   flags=0,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.CLOSE,
                                   text="Kernel Not Supported")
            md.format_secondary_markup(
                "Your current kernel does not support basic os function calls. <b>ArchLinux Tweak Tool</b> requires these to work.")  # noqa

        result = md.run()
        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            pid = ""
            with open("/tmp/att.pid", "r") as f:
                line = f.read()
                pid = line.rstrip().lstrip()
                f.close()

            if _functions.checkIfProcessRunning(int(pid)):
                _functions.MessageBox("Application Running!",
                                     "You first need to close the existing application")  # noqa
            else:
                os.unlink("/tmp/att.lock")
