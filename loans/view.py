#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
import locale

class View(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        crtext = gtk.CellRendererText()
        crtoggle = gtk.CellRendererToggle()
        
        self.column0 = gtk.TreeViewColumn("Typ", crtext, text=1)
        self.column1 = gtk.TreeViewColumn("IMEI", crtext, text=2)
        self.column2 = gtk.TreeViewColumn("Cena", crtext, text=3)
        self.column3 = gtk.TreeViewColumn("Bat", crtoggle, active=4)
        self.column4 = gtk.TreeViewColumn("Nab", crtoggle, active=5)
        self.column5 = gtk.TreeViewColumn("Jiné", crtext, text=6)
        self.append_column(self.column0)
        self.append_column(self.column1)
        self.append_column(self.column2)
        self.append_column(self.column3)
        self.append_column(self.column4)
        self.append_column(self.column5)
        
        self.column2.set_cell_data_func(crtext, self.ColRenderer2)
        self.column3.set_cell_data_func(crtoggle, self.ColRenderer3)
        self.column4.set_cell_data_func(crtoggle, self.ColRenderer4)
        
        self.column0.set_reorderable(True)
        self.column0.set_resizable(True)
        self.column0.set_sort_indicator(True)
        self.column0.set_sort_column_id(0)
        
        self.column1.set_reorderable(True)
        self.column1.set_resizable(True)
        self.column1.set_sort_indicator(True)
        self.column1.set_sort_column_id(1)
        
        self.column2.set_reorderable(True)
        self.column2.set_resizable(True)
        self.column2.set_sort_indicator(True)
        self.column2.set_sort_column_id(2)
        
        self.column3.set_reorderable(True)
        self.column3.set_resizable(True)
        self.column3.set_sort_indicator(True)
        self.column3.set_sort_column_id(3)
        
        self.column4.set_reorderable(True)
        self.column4.set_resizable(True)
        self.column4.set_sort_indicator(True)
        self.column4.set_sort_column_id(4)
        
        self.column5.set_reorderable(True)
        self.column5.set_resizable(True)
        #self.column5.set_sort_indicator(True)
        #self.column5.set_sort_column_id(5)
        
        self.set_search_column(1)

    def ColRenderer3(self, column, cell, model, iter):
        row = int(model.get_string_from_iter(iter))
        if row % 2 != 0:
            cell.set_property("cell-background", "#f4f8ff")
        else:
            cell.set_property("cell-background", "#ffffff")

    def ColRenderer4(self, column, cell, model, iter):
        row = int(model.get_string_from_iter(iter))
        if row % 2 != 0:
            cell.set_property("cell-background", "#f4f8ff")
        else:
            cell.set_property("cell-background", "#ffffff")

    def ColRenderer2(self, column, cell, model, iter):
        row = int(model.get_string_from_iter(iter))
        if row % 2 != 0:
            cell.set_property("cell-background", "#f4f8ff")
        else:
            cell.set_property("cell-background", "#ffffff")
        price = round(model.get_value(iter, 3), 2)
        price = locale.format("%.*f", (2, price), True)
        cell.set_property("text", price)
