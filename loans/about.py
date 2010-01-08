#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

class AboutDialog(gtk.AboutDialog):
    def __init__(self):
        gtk.AboutDialog.__init__(self)
        icon = gtk.gdk.pixbuf_new_from_file("res/logo.png")
        self.set_name(u"Pokus1")
        self.set_version("1.0")
        self.set_copyright(u"Copyright (c) OVX.cz 2003 s.r.o. 2009")
        self.set_comments(u"Pokus aplikace od OVX")
        self.set_authors([u"Patrik Šíma", u"Michal Čížek"])
        self.set_website("www.ovx.cz")
        self.set_logo(icon)
        self.connect("response", lambda d, r: self.destroy())

if __name__ == "__main__":
    dlg = AboutDialog()
    dlg.run()
