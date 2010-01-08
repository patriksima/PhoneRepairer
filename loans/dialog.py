#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

class AboutDialog(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self)
        self.table = gtk.Table(10, 10, True)
        self.table.set_col_spacings(5)
        self.table.set_row_spacings(5)
        s = ['name', 'surname', 'lol', 'kokot']
        for i, item in enumerate(s):
            print i, item
            self.table.attach(gtk.Label(item),0,3,i,i+1)
            self.table.attach(gtk.Entry(),3,10,i,i+1)
        self.table.attach(gtk.Button('ok'),1,9,i+1,i+2)
        self.vbox.add(self.table)
        self.show_all()

if __name__ == "__main__":
    dlg = AboutDialog()
    dlg.run()
