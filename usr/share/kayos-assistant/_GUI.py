import os

import _functions
import autostart
import desktopr
import distro
import sddm
import user
import zsh_theme

import autostart_GUI
import desktopr_GUI
import fixes_GUI
import grub_GUI
import pacman_GUI
import sddm_GUI
import zsh_theme_GUI
import user_GUI


def GUI(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango):  # noqa
    process = _functions.subprocess.run(["sh", "-c", "echo \"$SHELL\""],
                             stdout=_functions.subprocess.PIPE)

    output = process.stdout.decode().strip()

    # =======================================================
    #                       App Notifications
    # =======================================================

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.notification_revealer = Gtk.Revealer()
    self.notification_revealer.set_reveal_child(False)

    self.notification_label = Gtk.Label()

    pb_panel = GdkPixbuf.Pixbuf().new_from_file(base_dir + '/images/panel.png')
    panel = Gtk.Image().new_from_pixbuf(pb_panel)

    overlayFrame = Gtk.Overlay()
    overlayFrame.add(panel)
    overlayFrame.add_overlay(self.notification_label)

    self.notification_revealer.add(overlayFrame)

    hbox0.pack_start(self.notification_revealer, True, False, 0)

    # ==========================================================
    #                       CONTAINER
    # ==========================================================

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

    vbox.pack_start(hbox, True, True, 0)
    self.add(vbox)

    # ==========================================================
    #                    INITIALIZE STACK
    # ==========================================================
    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.NONE)

    vboxStack1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    #vboxStack5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    #vboxStack6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack7 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack8 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    #vboxStack9 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack10 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack11 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack12 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack13 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    #vboxStack14 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack15 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack16 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack17 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack18 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack19 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxStack20 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)



    # ==========================================================
    #                AUTOSTART
    # ==========================================================

    autostart_GUI.GUI(self, Gtk, GdkPixbuf, vboxStack13, autostart,
                      _functions, base_dir)

    # ==========================================================
    #                DESKTOP
    # ==========================================================

    desktopr_GUI.GUI(self, Gtk, GdkPixbuf, vboxStack12, desktopr,
                     _functions, base_dir, Pango)

    # # ==========================================================
    # #               FIXES
    # # ==========================================================

    fixes_GUI.GUI(self, Gtk, GdkPixbuf, vboxStack19, user, _functions)

    # ==========================================================
    #                 GRUB
    # ==========================================================

    if os.path.isfile("/boot/grub/themes/Vimix/theme.txt"):
        grub_GUI.GUI(self, Gtk, GdkPixbuf, vboxStack4, _functions)
    else:
        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl1 = Gtk.Label(xalign=0)
        lbl1.set_text("Grub")
        lbl1.set_name("title")
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox41.pack_start(hseparator, True, True, 0)
        hbox31.pack_start(lbl1, False, False, 0)
        vboxStack4.pack_start(hbox31, False, False, 0)
        vboxStack4.pack_start(hbox41, False, False, 0)
        ls = Gtk.Label()
        ls.set_markup("We did not find a <b>/boot/grub/themes/Vimix/themes.txt</b> file\nMake sure the ArcoLinux repos are activated in the Pacman tab")

        install_arco_vimix = Gtk.Button(label="Install Vimix theme")
        install_arco_vimix.connect("clicked", self.on_click_install_arco_vimix_clicked)

        vboxStack4.pack_start(install_arco_vimix, False, False, 0)
        vboxStack4.pack_start(ls, True, False, 0)

    
    # ==========================================================
    #                 PACMAN
    # ==========================================================
    if os.path.isfile(_functions.pacman):
        pacman_GUI.GUI(self, Gtk, vboxStack1, _functions)

    
    # # ==========================================================
    # #               SDDM
    # # ==========================================================

    if "plasma" in self.desktop.lower():
        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl1 = Gtk.Label(xalign=0)
        lbl1.set_text("Sddm Autologin")
        lbl1.set_name("title")
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox41.pack_start(hseparator, True, True, 0)
        hbox31.pack_start(lbl1, False, False, 0)
        vboxStack17.pack_start(hbox31, False, False, 0)
        vboxStack17.pack_start(hbox41, False, False, 0)
        ls = Gtk.Label()
        ls.set_markup("Use the Plasma settings manager to set Sddm")
        reset_sddm_original = Gtk.Button(label="Apply the sddm.conf from ArcoLinux")
        reset_sddm_original.connect("clicked", self.on_click_fix_sddm_conf)

        vboxStack17.pack_end(reset_sddm_original, False, False, 0)
        vboxStack17.pack_start(ls, True, False, 0)

    else:

        if os.path.isfile(_functions.sddm_conf):
            sddm_GUI.GUI(self, Gtk, GdkPixbuf, vboxStack17, sddm, _functions)
        else:
            hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl1 = Gtk.Label(xalign=0)
            lbl1.set_text("Sddm Autologin")
            lbl1.set_name("title")
            hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            hbox41.pack_start(hseparator, True, True, 0)
            hbox31.pack_start(lbl1, False, False, 0)
            vboxStack17.pack_start(hbox31, False, False, 0)
            vboxStack17.pack_start(hbox41, False, False, 0)
            ls = Gtk.Label()
            ls.set_markup("No /etc/sddm.conf configuration file found. \nInstall <b>Sddm</b> and the configuration file to use this tab.")
            reset_sddm_original = Gtk.Button(label="Apply the sddm.conf from ArcoLinux")
            reset_sddm_original.connect("clicked", self.on_click_no_sddm_reset_original)
            install_sddm = Gtk.Button(label="Install Sddm and enable it")
            install_sddm.connect("clicked", self.on_click_att_sddm_clicked)
            reset_sddm_original_restart = Gtk.Button(label="Restart ArchLinux Tweak Tool")
            reset_sddm_original_restart.connect("clicked", self.on_refresh_att_clicked)

            vboxStack17.pack_start(ls, False, False, 0)
            vboxStack17.pack_end(reset_sddm_original_restart, False, False, 0)
            vboxStack17.pack_end(reset_sddm_original, False, False, 0)
            vboxStack17.pack_end(install_sddm, False, False, 0)


    # # ==========================================================
    # #                USER
    # # ==========================================================

    user_GUI.GUI(self, Gtk, GdkPixbuf, vboxStack18, user, _functions)
    ls = Gtk.Label()
    ls.set_markup("Fill in the fields and create your account")
    vboxStack18.pack_start(ls, True, False, 0)

     # ==========================================================
    #                   ZSH
    # ==========================================================

    zsh_theme_GUI.GUI(self, Gtk, vboxStack15, zsh_theme, base_dir, GdkPixbuf)

    # ==========================================================
    #                   ADD TO WINDOW
    # ==========================================================

    stack.add_titled(vboxStack1, "stack6", "Pacman")
    stack.add_titled(vboxStack18, "stack18", "User")
    stack.add_titled(vboxStack13, "stack13", "Autostart")   
    stack.add_titled(vboxStack17, "stack17", "Sddm")
    stack.add_titled(vboxStack4, "stack1", "Grub") 
    stack.add_titled(vboxStack15, "stack15", "Zsh") 
    stack.add_titled(vboxStack12, "stack12", "Desktop") 
    stack.add_titled(vboxStack19, "stack19", "Fixes") 

    stack_switcher = Gtk.StackSidebar()
    stack_switcher.set_name("sidebar")
    stack_switcher.set_stack(stack)


    # =====================================================
    #               RESTART BUTTON
    # =====================================================
    
    btnReStartAtt = Gtk.Button(label="Restart")
    btnReStartAtt.connect('clicked', self.on_refresh_att_clicked)

    # =====================================================
    #                      PACKS
    # =====================================================

    ivbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

    hbox3.pack_start(btnReStartAtt, False, False, 0)

    #ivbox.pack_start(image, False, False, 0)
    ivbox.pack_start(stack_switcher, True, True, 0)

    ivbox.pack_start(hbox2, False, False, 0)
    ivbox.pack_start(hbox3, False, False, 0)

    vbox1.pack_start(hbox0, False, False, 0)
    vbox1.pack_start(stack, True, True, 0)

    hbox.pack_start(ivbox, False, True, 0)
    hbox.pack_start(vbox1, True, True, 0)

    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)
