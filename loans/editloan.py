#!/usr/bin/env python
# coding: utf-8

import re, sqlite3
import pygtk
pygtk.require('2.0')
import gtk

class EditLoanDlg(gtk.Dialog):
    def __init__(self, parent, idloan):
        gtk.Dialog.__init__(self, "Edit loan")
        
        self.idloan = idloan
        self.error = False
        
        # cmon dialog settings
        self.set_default_response(gtk.RESPONSE_OK)
        self.set_has_separator(False)
        self.set_transient_for(parent)
        self.set_destroy_with_parent(True)
        self.set_border_width(6)
        self.set_modal(True)
        
        #self.connect("destroy", self.quit)
        #self.connect("delete-event", self.quit)
                
        # action area
        hbox = gtk.HButtonBox()
        hbox.set_layout(gtk.BUTTONBOX_END)
        btn1 = gtk.Button("Zrušit", gtk.STOCK_CANCEL)
        btn2 = gtk.Button("Uložit", gtk.STOCK_OK)
        btn1.connect("clicked", self.cancel)
        btn2.connect("clicked", self.check)
        hbox.add(btn1)
        hbox.add(btn2)
    
        # init db
        try:
            self.conn = sqlite3.connect("./data.db", detect_types=sqlite3.PARSE_DECLTYPES)
            self.curs = self.conn.cursor()
        except sqlite3.OperationalError, e:
            print "sqlite3: %s" % e
        
        sqlite3.register_adapter(str, lambda s:s.decode('utf-8'))
        sqlite3.register_adapter(bool, lambda x:int(x))
        sqlite3.register_converter('BOOLEAN', lambda x:bool(int(x)))
        
        self.curs.execute("CREATE TABLE IF NOT EXISTS types \
        (id INTEGER PRIMARY KEY AUTOINCREMENT, type)")
        self.conn.commit()
   
        self.curs.execute("SELECT * FROM loans WHERE id = ?", (self.idloan,))
        self.data = self.curs.fetchone()
        
        # widgets for checking
        self.elements = []
        
        self.table = gtk.Table(10, 10, False)
        self.table.set_col_spacings(10)
        self.table.set_row_spacings(10)
        
        label = gtk.Label("Typ:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 1, 2)
        
        combo = gtk.combo_box_new_text()
        combo.append_text("--vyberte--")
        self.curs.execute("SELECT type FROM types ORDER BY type")
        for i,row in enumerate(self.curs):
            combo.append_text(row[0])
            if self.data[1]==row[0]:
                combo.set_active(i+1)
        self.elements.append(combo)
        self.table.attach(combo, 3, 10, 1, 2)
        
        label = gtk.Label("IMEI:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 2, 3)

        entry = gtk.Entry()
        entry.set_text(self.data[2])
        self.elements.append(entry)
        self.table.attach(entry, 3, 10, 2, 3)
        
        label = gtk.Label("Cena:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 3, 4)

        entry = gtk.Entry()
        entry.set_text(str(self.data[3]))
        self.elements.append(entry)
        self.table.attach(entry, 3, 10, 3, 4)
        
        label = gtk.Label("Baterie:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 4, 5)

        check = gtk.CheckButton()
        check.set_active(self.data[4])
        self.elements.append(check)
        self.table.attach(check, 3, 10, 4, 5)
        
        label = gtk.Label("Nabíječka:")
        label.set_alignment(1.0,0.5)
        self.table.attach(label, 0, 3, 5, 6)

        check = gtk.CheckButton()
        check.set_active(self.data[5])
        self.elements.append(check)
        self.table.attach(check, 3, 10, 5, 6)
        
        label = gtk.Label("Ostatní:")
        label.set_alignment(1.0,0.0)
        self.table.attach(label, 0, 3, 6, 7)

        scroll = gtk.ScrolledWindow()
        textview = gtk.TextView()
        textview.set_size_request(300,100)
        textview.get_buffer().set_text(self.data[6])
        scroll.add(textview)
        self.elements.append(textview)
        self.table.attach(scroll, 3, 10, 6, 7)
        
        self.vbox.add(self.table)
        self.vbox.add(hbox)
        self.show_all()
     
    def errormsg(self, msg):
        self.error = True
        dlg = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, \
                                      gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, \
                                      msg)
        dlg.set_title("Chyba")
        dlg.run()
        dlg.hide()

    def cancel(self, widget):
        self.response(gtk.RESPONSE_CANCEL) 
        self.quit()
        
    def check(self, widget):
        self.error = False
        
        if self.elements[0].get_active()==0:
            return self.errormsg("Vyberte typ telefonu.")
            
        if self.elements[1].get_text()=="":
            return self.errormsg("Zadejte IMEI.")
            
        if self.elements[2].get_text()=="":
            return self.errormsg("Zadejte cenu.")
            
        if not re.match(r"^[0-9]+(\.[0-9]+)?$",self.elements[2].get_text()):
            return self.errormsg("Formát ceny není korektní.")

        if not self.error:
            self.save()
            self.response(gtk.RESPONSE_OK) 
            self.quit() 

    def save(self):
        textbuff = self.elements[5].get_buffer()
        start, end = textbuff.get_bounds()
        c = ["type=?", "imei=?", "price=?", "battery=?", "charger=?", "other=?"]
        k = ",".join(c)
        query = "UPDATE loans SET %s WHERE id = ?" % k
        self.curs.execute(query, (self.elements[0].get_active_text(), \
                                  self.elements[1].get_text(), \
                                  self.elements[2].get_text(), \
                                  self.elements[3].get_active(), \
                                  self.elements[4].get_active(), \
                                  textbuff.get_text(start,end), \
                                  self.idloan))
        self.conn.commit()

    def quit(self, *dummy):
        print "quit"
        self.conn.close()
        self.destroy()
        
if __name__ == "__main__":
    dlg = EditLoanDlg(None, 1)
    print dlg.run()
