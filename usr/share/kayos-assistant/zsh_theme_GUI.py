import _functions

def GUI(self, Gtk, main, zsh_theme, base_dir, GdkPixbuf):
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("ZSH Themes")
    lbl1.set_name("title")
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hbox4.pack_start(hseparator, True, True, 0)
    hbox3.pack_start(lbl1, False, False, 0)
    

    label12 = Gtk.Label()
    label12.set_text("Zsh themes")
    hbox19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox19.pack_start(label12, False, False, 10)

    self.zsh_themes = Gtk.ComboBoxText()
    zsh_theme.get_themes(self.zsh_themes)
    hbox19.pack_start(self.zsh_themes, True, True, 10)

    label13 = Gtk.Label()
    label13.set_text("Chnage Zsh theme: Restart terminal\nSwitch shell: Re-login")
    label13.set_margin_top(30)
    hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox21.pack_start(label13, False, False, 10)

    tobash = Gtk.Button(label="Apply bash")
    tozsh = Gtk.Button(label="Apply zsh")

    tobash.connect("clicked", self.tobash_apply)
    tozsh.connect("clicked", self.tozsh_apply)

    termset = Gtk.Button(label="Apply Zsh theme")
    termreset = Gtk.Button(label="Reset ~/.zshrc")

    hbox20 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    hbox20.pack_end(termset, False, False, 0)
    hbox20.pack_end(termreset, False, False, 0)
    hbox20.pack_end(tozsh, False, False, 0)
    hbox20.pack_end(tobash, False, False, 0)

    termset.connect("clicked", self.on_zsh_apply)
    termreset.connect("clicked", self.on_zsh_reset)


    image_width = 600
    image_height = 480
    pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(base_dir + "/images/zsh-sample.png", image_width, image_height)
    if self.zsh_themes.get_active_text() is None:
        pass
    elif _functions.os.path.isfile(base_dir+"/images/zsh_previews/"+self.zsh_themes.get_active_text()+".jpg"):
        pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(base_dir + "/images/zsh_previews/"+self.zsh_themes.get_active_text()+".jpg", image_width, image_height)
    image = Gtk.Image().new_from_pixbuf(pixbuf)
    image.set_margin_top(30)

    self.zsh_themes.connect("changed", self.update_image, image, "zsh", base_dir, image_width, image_height)

    main.pack_start(hbox3, False, False, 0)  
    main.pack_start(hbox4, False, False, 0) 
    main.pack_start(hbox19, False, False, 0) 
    main.pack_start(image, False, False, 0)  
    main.pack_start(hbox21, False, False, 0) 
    main.pack_end(hbox20, False, False, 0) 

    if not zsh_theme.check_oh_my():
        termset.set_sensitive(False)
