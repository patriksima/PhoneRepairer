#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

class UIManager(gtk.UIManager):
    ui = '''<ui>
    <menubar name="MenuBar">
      <menu action="File">
        <menuitem action="Quit"/>
      </menu>
      <menu action="Loans">
        <menuitem action="Add"/>
        <menuitem action="Edit"/>
        <menuitem action="Del"/>
      </menu>
    </menubar>
    <toolbar name="ToolBar">
      <toolitem action="Quit"/>
      <separator/>
      <placeholder name="LoansHolder">
        <toolitem action="Add"/>
        <toolitem action="Edit"/>
        <toolitem action="Del"/>
      </placeholder>
    </toolbar>
    </ui>'''
    
    def __init__(self):
        gtk.UIManager.__init__(self)
        self.actiongroup = gtk.ActionGroup('UIBase')
        self.actions = (('File', None, '_File'),
                            ('Quit', gtk.STOCK_QUIT, '_Quit', None, 'Quit', None),
                        ('Loans', None, '_Loans'),
                            ('Add', None, '_Add', '<CTRL>A', 'Add loan', None),
                            ('Edit', None, '_Edit', '<CTRL>E', 'Edit loan', None),
                            ('Del', None, '_Del', '<CTRL>D', 'Delete loan', None))
        self.actiongroup.add_actions(self.actions)
        self.insert_action_group(self.actiongroup, 0)
        self.add_ui_from_string(self.ui)
        
        self.get_widget('/ToolBar').set_style(gtk.TOOLBAR_BOTH)
