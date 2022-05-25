def GUI(self, Gtk, main, Functions):
    # header
    hlabel = Gtk.Label(xalign=0)
    hlabel.set_text("Pacman Editor")
    hlabel.set_name("title")
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

    header_frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    header_frame.pack_start(hlabel, False, False, 0)
    header_frame.pack_start(hseparator, True, True, 0)
    

    # footer
    apply_custom = Gtk.Button(label="Apply custom repo")
    apply_custom.connect('clicked', self.apply_custom_repo)
    reset_pacman = Gtk.Button(label="Reset pacman")
    reset_pacman.connect("clicked", self.reset_settings, Functions.pacman)
    blank_pacman = Gtk.Button(label="Blank pacman")
    blank_pacman.connect("clicked", self.blank_settings)

    footer_frame = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    footer_frame.pack_end(apply_custom, False, False, 0)
    footer_frame.pack_end(reset_pacman, False, False, 0)
    footer_frame.pack_end(blank_pacman, False, False, 0)
    

    # repo
    repo_frame = Gtk.Frame(label="")
    flabel = repo_frame.get_label_widget()
    flabel.set_markup("<b>Arch Linux repos</b>")

    self.checkbutton1 = Gtk.Switch()
    self.checkbutton1.connect("notify::active", self.on_pacman_toggle1)
    label1 = Gtk.Label(xalign=0)
    label1.set_markup("Enable Arch Linux testing repo")

    self.checkbutton2 = Gtk.Switch()
    self.checkbutton2.connect("notify::active", self.on_pacman_toggle2)
    label2 = Gtk.Label(xalign=0)
    label2.set_markup("Enable Arch Linux core repo") 

    self.checkbutton3 = Gtk.Switch()
    self.checkbutton3.connect("notify::active", self.on_pacman_toggle3)
    label3 = Gtk.Label(xalign=0)
    label3.set_markup("Enable Arch Linux extra repo")

    self.checkbutton4 = Gtk.Switch()
    self.checkbutton4.connect("notify::active", self.on_pacman_toggle4)
    label4 = Gtk.Label(xalign=0)
    label4.set_markup("Enable Arch Linux community testing repo")

    self.checkbutton5 = Gtk.Switch()
    self.checkbutton5.connect("notify::active", self.on_pacman_toggle5)
    label5 = Gtk.Label(xalign=0)
    label5.set_markup("Enable Arch Linux community repo")  

    self.checkbutton6 = Gtk.Switch()
    self.checkbutton6.connect("notify::active", self.on_pacman_toggle6)
    label6 = Gtk.Label(xalign=0)
    label6.set_markup("Enable Arch Linux multilib testing repo")

    self.checkbutton7 = Gtk.Switch()
    self.checkbutton7.connect("notify::active", self.on_pacman_toggle7)
    label7 = Gtk.Label(xalign=0)
    label7.set_markup("Enable Arch Linux multilib repo")

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)    
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

    hbox1.pack_start(label1, False, True, 10)
    hbox1.pack_end(self.checkbutton1, False, False, 10)
    hbox2.pack_start(label2, False, True, 10)
    hbox2.pack_end(self.checkbutton2, False, False, 10)
    hbox3.pack_start(label3, False, True, 10)
    hbox3.pack_end(self.checkbutton3, False, False, 10)
    hbox4.pack_start(label4, False, True, 10)
    hbox4.pack_end(self.checkbutton4, False, False, 10)
    hbox5.pack_start(label5, False, True, 10)
    hbox5.pack_end(self.checkbutton5, False, False, 10)
    hbox6.pack_start(label6, False, True, 10)
    hbox6.pack_end(self.checkbutton6, False, False, 10)
    hbox7.pack_start(label7, False, True, 10)
    hbox7.pack_end(self.checkbutton7, False, False, 10)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox.pack_start(hbox1, False, False, 0)
    vbox.pack_start(hbox2, False, False, 0)
    vbox.pack_start(hbox3, False, False, 0)
    vbox.pack_start(hbox4, False, False, 0)
    vbox.pack_start(hbox5, False, False, 0)
    vbox.pack_start(hbox6, False, False,0)
    vbox.pack_start(hbox7, False, False,0)
    repo_frame.add(vbox)


    # custom repo
    clabel = Gtk.Label(xalign=0)
    clabel.set_markup("<b>Add custom repo to pacman.conf</b>")

    self.ctextbook = Gtk.TextView()
    self.ctextbook.set_wrap_mode(Gtk.WrapMode.WORD)
    self.ctextbook.set_editable(True)
    self.ctextbook.set_cursor_visible(True)
    self.ctextbook.set_border_window_size(Gtk.TextWindowType.LEFT, 1)
    self.ctextbook.set_border_window_size(Gtk.TextWindowType.RIGHT, 1)
    self.ctextbook.set_border_window_size(Gtk.TextWindowType.TOP, 1)
    self.ctextbook.set_border_window_size(Gtk.TextWindowType.BOTTOM, 1)

    cscrollwindow = Gtk.ScrolledWindow()
    cscrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    cscrollwindow.add(self.ctextbook)

    custom_repo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    custom_repo.pack_start(clabel, False, False, 0)
    custom_repo.pack_start(cscrollwindow, True, True, 0)


    # pack to window
    main.pack_start(header_frame, False, False, 0)
    main.pack_start(repo_frame, False, False, 0)
    main.pack_start(custom_repo, True, True, 0)
    main.pack_end(footer_frame, False, False, 0)
