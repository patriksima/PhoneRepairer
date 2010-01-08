#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

import locale
locale.setlocale(locale.LC_ALL,'cs_CZ.utf8')

from db import DB

class Model(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, int, str, str, float, bool, bool, str)
        self.db = DB.getInstance()
        
        self.set_sort_func(0, lambda m,i1,i2:locale.strcoll(str(m.get_value(i1,1)),str(m.get_value(i2,1))))
        self.set_sort_func(1, lambda m,i1,i2:locale.strcoll(str(m.get_value(i1,2)),str(m.get_value(i2,2))))
        self.set_sort_func(2, lambda m,i1,i2:cmp(int(m.get_value(i1,3)),int(m.get_value(i2,3))))
        self.set_sort_func(3, lambda m,i1,i2:cmp(int(m.get_value(i1,4)),int(m.get_value(i2,4))))
        self.set_sort_func(4, lambda m,i1,i2:cmp(int(m.get_value(i1,5)),int(m.get_value(i2,5))))
        self.set_sort_column_id(0, gtk.SORT_ASCENDING)

        self.refresh()
    
    def add(self, *data):
        self.db.execute("INSERT INTO loans (type, imei, price, battery, charger, other) \
                         VALUES (?, ?, ?, ?, ?, ?)", data)
        self.db.commit()

        row = [i for i in data]
        row.insert(0, self.db.lastrowid)
        
        self.append(row)

    def update(self, iter, *data):
        for i, col in enumerate(data):
            self.set_value(iter, i, col)

    def delete(self, iter):
        self.db.execute("DELETE FROM loans WHERE id = ?", (self.get_value(iter, 0),))
        self.db.commit()
        self.remove(iter)

    def refresh(self):
        self.clear()
        res = self.db.execute("SELECT * FROM loans ORDER BY type ASC")
        for row in res:
            self.append([col for col in row])
        
if __name__ == "__main__":
    model = Model()      
