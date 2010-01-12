#!/usr/bin/env python
# coding: utf-8

import os, sys

import pygtk
pygtk.require('2.0')
import gtk

class AboutDlg(gtk.AboutDialog):
    def __init__(self):
        gtk.AboutDialog.__init__(self)
        icon = gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.abspath(sys.path[0]), '..', 'resources','logo.svg'))
        self.set_name(u"Phone Repairer")
        self.set_version("1.0")
        self.set_copyright(u"Copyright (c) OVX.cz 2003 s.r.o.")
        self.set_comments(u"Phone Repairer")
        self.set_authors([u"Patrik Šíma", u"Michal Čížek"])
        self.set_website("http://www.ovx.cz/")
        self.set_website_label("www.ovx.cz")
        self.set_logo(icon)
        self.connect("response", lambda d, r: self.destroy())

if __name__ == "__main__":
    dlg = AboutDlg()
    dlg.run()
