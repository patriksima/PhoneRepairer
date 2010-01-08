#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
import sqlite3

class Model(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, int, str, str, float, bool, bool, str)
        
        try:
            self.conn = sqlite3.connect("./data.db", detect_types=sqlite3.PARSE_DECLTYPES)
            self.curs = self.conn.cursor()
        except sqlite3.OperationalError, e:
            print "sqlite3: %s" % e
        
        sqlite3.register_adapter(str, lambda s:s.decode('utf-8'))
        sqlite3.register_adapter(bool, lambda x:int(x))
        sqlite3.register_converter('BOOLEAN', lambda x:bool(int(x)))
        
        self.curs.execute("CREATE TABLE IF NOT EXISTS loans \
        (id INTEGER PRIMARY KEY AUTOINCREMENT, \
        type, imei, price INTEGER, battery BOOLEAN, charger BOOLEAN, other)")
        self.conn.commit()
        
        self.update()
    
    def __del__(self):
        self.conn.close()

    def update(self):
        self.clear()
        self.curs.execute("SELECT * FROM loans ORDER BY id DESC")
        for row in self.curs:
            self.append([col for col in row])
        
if __name__ == "__main__":
    model = Model()      
