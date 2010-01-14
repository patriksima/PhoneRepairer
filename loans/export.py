#!/usr/bin/env python
# coding: utf-8

import re, os

import pygtk
pygtk.require('2.0')
import gtk

from db import DB

class ExportDlg(gtk.Dialog):
    def __init__(self, parent, model):
        gtk.Dialog.__init__(self, "Export do CSV")
        
        self.model = model
        
        self.connect("delete-event", self.quit)
        
        # cmon dialog settings
        self.set_default_response(gtk.RESPONSE_OK)
        self.set_has_separator(False)
        self.set_transient_for(parent)
        self.set_destroy_with_parent(True)
        self.set_border_width(6)
        self.set_modal(True)
        
        # action area
        hbox = gtk.HButtonBox()
        hbox.set_layout(gtk.BUTTONBOX_END)
        btn1 = gtk.Button("Zrušit", gtk.STOCK_CANCEL)
        btn2 = gtk.Button("Export", gtk.STOCK_OK)
        btn1.connect("clicked", self.quit)
        btn2.connect("clicked", self.export)
        hbox.add(btn1)
        hbox.add(btn2)
        
        # widgets for checking
        self.elements = []
        
        table = gtk.Table(10, 10, False)
        table.set_col_spacings(10)
        table.set_row_spacings(10)

        label = gtk.Label("Název souboru:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 3, 1, 2)
        entry = gtk.Entry()
        entry.set_text("export.csv")
        self.elements.append(entry)
        table.attach(entry, 3, 10, 1, 2)
        
        label = gtk.Label("Umístění:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 3, 2, 3)
        dialog = gtk.FileChooserDialog("Umístění pro export", None,
                 gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                 gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        chooser = gtk.FileChooserButton(dialog)
        self.elements.append(chooser)
        table.attach(chooser, 3, 10, 2, 3)
        
        label = gtk.Label("Kódování:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 3, 3, 4)
        combo = gtk.combo_box_new_text()
        combo.append_text("utf-8")
        combo.append_text("windows-1250")
        combo.append_text("iso-8859-2")
        combo.set_active(0)
        self.elements.append(combo)
        table.attach(combo, 3, 10, 3, 4)
        
        label = gtk.Label("Oddělovač pole:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 3, 4, 5)
        combo = gtk.combo_box_new_text()
        combo.append_text(";")
        combo.append_text(",")
        combo.append_text("|")
        combo.append_text("Mezera")
        combo.append_text("Tabulátor")
        combo.set_active(0)
        self.elements.append(combo)
        table.attach(combo, 3, 10, 4, 5)
        
        label = gtk.Label("Oddělovač textu:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 3, 5, 6)
        combo = gtk.combo_box_new_text()
        combo.append_text('"')
        combo.append_text("'")
        combo.set_active(0)
        self.elements.append(combo)
        table.attach(combo, 3, 10, 5, 6)
        
        self.vbox.add(table)
        self.vbox.add(hbox)
        self.show_all()
        
    def export(self, *args):
        params = (self.elements[0].get_text(),
                  self.elements[1].get_filename(),
                  self.elements[2].get_active_text(),
                  self.elements[3].get_active_text(),
                  self.elements[4].get_active_text())
        try:
            csvfile = open(os.path.join(params[1], params[0]), "w")
            for row in self.model:
                tmp = [params[4]+str(col)+params[4] for col in row]
                tmp = params[3].join(tmp)
                tmp+= "\n"
                tmp = tmp.encode(params[2])
                csvfile.write(tmp)
            csvfile.close()
            
            dlg = gtk.MessageDialog(parent=self, \
                                    type=gtk.MESSAGE_INFO, \
                                    buttons=gtk.BUTTONS_OK, \
                                    message_format="Uloženo")
            dlg.set_title("Export")
            dlg.run()
            dlg.destroy()
            
            self.response(gtk.RESPONSE_OK)
            self.quit()
        except IOError:
            dlg = gtk.MessageDialog(parent=self, \
                                    type=gtk.MESSAGE_ERROR, \
                                    buttons=gtk.BUTTONS_OK, \
                                    message_format="Nemohu otevřít soubor %s" % params[0])
            dlg.set_title("Chyba")
            dlg.run()
            dlg.destroy()

    def quit(self, *dummy):
        self.hide()
        self.destroy()
        
if __name__ == "__main__":
    dlg = ExportDlg(None, None)
    res = dlg.run()
    if res == gtk.RESPONSE_OK:
        print "good job sir"
