#!/usr/bin/env python
# coding: utf-8

import re
import pygtk
pygtk.require('2.0')
import gtk

from db import DB

class AddLoanDlg(gtk.Dialog):
    def __init__(self, parent, model):
        gtk.Dialog.__init__(self, "Add loan")
        
        self.db = DB.getInstance()
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
        btn2 = gtk.Button("Přidat", gtk.STOCK_OK)
        btn1.connect("clicked", self.cancel)
        btn2.connect("clicked", self.check)
        hbox.add(btn1)
        hbox.add(btn2)
    
        # widgets for checking
        self.elements = []
        
        self.table = gtk.Table(10, 10, False)
        self.table.set_col_spacings(10)
        self.table.set_row_spacings(10)
        
        label = gtk.Label("Typ:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 1, 2)
        
        entry = gtk.Entry()
        compl = gtk.EntryCompletion()
        compl.set_model(self.create_types_store())
        entry.set_completion(compl)
        compl.set_text_column(0)

        self.elements.append(entry)
        self.table.attach(entry, 3, 10, 1, 2)
        
        label = gtk.Label("IMEI:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 2, 3)

        entry = gtk.Entry()
        self.elements.append(entry)
        self.table.attach(entry, 3, 10, 2, 3)
        
        label = gtk.Label("Cena:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 3, 4)

        entry = gtk.Entry()
        self.elements.append(entry)
        self.table.attach(entry, 3, 10, 3, 4)
        
        label = gtk.Label("Baterie:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 4, 5)

        check = gtk.CheckButton()
        self.elements.append(check)
        self.table.attach(check, 3, 10, 4, 5)
        
        label = gtk.Label("Nabíječka:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 5, 6)

        check = gtk.CheckButton()
        self.elements.append(check)
        self.table.attach(check, 3, 10, 5, 6)
        
        label = gtk.Label("Ostatní:")
        label.set_alignment(1.0,0.0)
        self.table.attach(label, 0, 3, 6, 7)

        scroll = gtk.ScrolledWindow()
        textview = gtk.TextView()
        textview.set_size_request(300,100)
        scroll.add(textview)
        self.elements.append(textview)
        self.table.attach(scroll, 3, 10, 6, 7)
        
        self.vbox.add(self.table)
        self.vbox.add(hbox)
        self.show_all()
    
    def create_types_store(self):
        lst = gtk.ListStore(str)
        res = self.db.execute("SELECT type FROM loans GROUP BY type ORDER BY type")
        for row in res:
            lst.append([row[0]])
        return lst
        
    def error_msg(self, msg):
        dlg = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, \
                                      gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, \
                                      msg)
        dlg.set_title("Chyba")
        dlg.run()
        dlg.hide()

    def cancel(self, widget):
        self.response(gtk.RESPONSE_CANCEL) 
        self.quit()
        
    def check(self, widget):
        if self.elements[0].get_text()=="":
            return self.error_msg("Vyberte typ telefonu.")
            
        if self.elements[1].get_text()=="":
            return self.error_msg("Zadejte IMEI.")
            
        if self.elements[2].get_text()=="":
            return self.error_msg("Zadejte cenu.")
            
        if not re.match(r"^[0-9]+(\.[0-9]+)?$",self.elements[2].get_text()):
            return self.error_msg("Formát ceny není korektní.")

        buff = self.elements[5].get_buffer()
        s, e = buff.get_bounds()
        
        self.model.add(self.elements[0].get_text(), \
                       self.elements[1].get_text(), \
                       int(self.elements[2].get_text()), \
                       self.elements[3].get_active(), \
                       self.elements[4].get_active(), \
                       buff.get_text(s, e))
        
        self.response(gtk.RESPONSE_OK)
        self.quit()

    def quit(self, *dummy):
        self.hide()
        self.destroy()
        
if __name__ == "__main__":
    def add(*dummy):
        print type(dummy), dummy
    model = gtk.ListStore(str)
    model.add = add
    
    main = gtk.Window()
    main.show()
    main.connect("destroy", lambda x:gtk.main_quit())
    
    dlg = AddLoanDlg(main, model)
    res = dlg.run()
    if res == gtk.RESPONSE_OK:
        print "good job sir"
    
    gtk.main()
