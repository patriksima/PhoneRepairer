#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

from model import Model
from view import View

from uimanager import UIManager

from addloan import AddLoanDlg
from editloan import EditLoanDlg

class MainWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        self.set_title("Phone Repairer Loans")
        
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)
        
        self.uimanager = UIManager()
        
        accelgroup = self.uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        
        self.uimanager.get_action('/MenuBar/File/Quit').connect("activate", self.destroy)
        self.uimanager.get_action('/MenuBar/Loans').connect("activate", self.addtype)
        self.uimanager.get_action('/MenuBar/Loans/Add').connect("activate", self.addloan)
        self.uimanager.get_action('/MenuBar/Loans/Edit').connect("activate", self.editloan)
        self.uimanager.get_action('/MenuBar/Loans/Del').connect("activate", self.delloan)
        self.uimanager.get_action('/MenuBar/Loans/Edit').set_sensitive(False)
        self.uimanager.get_action('/MenuBar/Loans/Del').set_sensitive(False)
                
        vbox = gtk.VBox()
        
        menubar = self.uimanager.get_widget('/MenuBar')
        toolbar = self.uimanager.get_widget('/ToolBar')
        print toolbar
        vbox.pack_start(menubar, False)
        vbox.pack_start(toolbar, False)
        
        scroll = gtk.ScrolledWindow()
        self.view = View()
        self.model = Model()
        self.view.set_model(self.model)
        
        #self.uimanager.addtype.connect("activate", self.addtype)
        self.view.connect("row-activated", self.active)
        self.view.connect("cursor-changed", self.changed)
        self.model.connect("row-changed", self.on_model_row_changed)
#        filter = model.filter_new()
#        filter.set_visible_func( self.visible_func )
#        view.set_model(filter)
        scroll.add(self.view)
        vbox.add(scroll)
        self.statusbar = gtk.Statusbar()
        self.contextid = self.statusbar.get_context_id("Phone Repairer")
        self.statusbar.push(self.contextid, "Ready")
        vbox.pack_start(self.statusbar, False)
        vbox.show()
        self.add(vbox)
        self.resize(800, 600)
        self.show_all()
    
    def addloan(self, *args):
        dlg = AddLoanDlg(self)
        res = dlg.run()
        self.view.set_model(None)
        self.model.update()
        self.view.set_model(self.model)
        self.uimanager.get_action('/MenuBar/Loans/Edit').set_sensitive(False)
        self.uimanager.get_action('/MenuBar/Loans/Del').set_sensitive(False)

    def on_model_row_changed(self, model, path, iter_):
        print model, path, iter_

    def editloan(self, *args):
        (path, col) = self.view.get_cursor()
        id = self.model[path][0]
        dlg = EditLoanDlg(self, id)
        dlg.run()

    def delloan(self, *args):
        dlg = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, \
                                      gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES|gtk.BUTTONS_NO, \
                                      msg)
        dlg.set_title("Chyba")
        if dlg.run == gtk.RESPONSE_YES:
            (path, col) = self.view.get_cursor()
            iter = self.model.get_iter(path)
            self.model.remove(iter)

    def changed(self, *args):
        print args
        (path, col) = self.view.get_cursor()
        data = self.model[path][0]
        print path, col
        print data
        self.uimanager.get_action('/MenuBar/Loans/Edit').set_sensitive(True)
        self.uimanager.get_action('/MenuBar/Loans/Del').set_sensitive(True)
        
    def active(self, widget, path, column):
        print widget, path, column

    def addtype(self, action):
        print action
        
    def visible_func(self, model, iter):
        return True

    def delete_event(self, widget, event, data=None):
        return False
    
    def destroy(self, widget, data=None):
        gtk.main_quit()
        
    def aboutdialog(self, widget, data=None):
        dlg = AboutDialog()
        dlg.run()
