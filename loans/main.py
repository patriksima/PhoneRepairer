#!/usr/bin/env python
# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

import math
import cairo
import pango

from model import Model
from view import View

from uimanager import UIManager

from about import AboutDlg
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
        self.uimanager.get_action('/MenuBar/File/Print').connect("activate", self.printing)
        self.uimanager.get_action('/MenuBar/Loans/Add').connect("activate", self.addloan)
        self.uimanager.get_action('/MenuBar/Loans/Edit').connect("activate", self.editloan)
        self.uimanager.get_action('/MenuBar/Loans/Del').connect("activate", self.delloan)
        self.uimanager.get_action('/MenuBar/Help/About').connect("activate", self.aboutdialog)
        self.uimanager.get_action('/MenuBar/Loans/Edit').set_sensitive(False)
        self.uimanager.get_action('/MenuBar/Loans/Del').set_sensitive(False)
                
        vbox = gtk.VBox()
        
        menubar = self.uimanager.get_widget('/MenuBar')
        toolbar = self.uimanager.get_widget('/ToolBar')
        
        vbox.pack_start(menubar, False)
        vbox.pack_start(toolbar, False)
        
        scroll = gtk.ScrolledWindow()
        self.view = View()
        self.model = Model()
        self.view.set_model(self.model)
        self.view.connect("row-activated", self.on_row_actived)
        self.view.connect("cursor-changed", self.on_cursor_changed)
        
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
        
    def draw_page (self, operation, context, page_number):
        cr = context.get_cairo_context()

        cr.set_line_width(0.1)
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0.0, 0.0, context.get_width(), context.get_height())
        cr.stroke()
        
        cr.set_line_width(0.5)
        cr.arc(context.get_width()/2, context.get_height()/2, 50, 0, 2*math.pi)
        cr.stroke()   
        cr.arc(context.get_width()/2, context.get_height()/2+10, 20, 15 * (math.pi/180), 165 * (math.pi/180))
        cr.stroke()   
        cr.arc(context.get_width()/2-18, context.get_height()/2-20, 5, 0, 2*math.pi)
        cr.stroke()   
        cr.arc(context.get_width()/2+18, context.get_height()/2-20, 5, 0, 2*math.pi)
        cr.stroke()  
        
        layout = context.create_pango_layout()
        layout.set_markup("by OVX")
        layout.set_font_description(pango.FontDescription("sans 10"))
        layout.set_alignment(pango.ALIGN_RIGHT)

        w, h = layout.get_pixel_size()

        cr.move_to(context.get_width()-w-5, context.get_height()-h-5)
        cr.layout_path(layout)
        cr.fill()
 
        """
        start_line = page_number * self.lines_per_page
        if page_number + 1 != operation.props.n_pages:
            end_line = start_line + self.lines_per_page
        else:
            end_line = self.layout.get_line_count()

        print start_line, end_line
        
        cr.move_to(0, 0)

        iter = self.layout.get_iter()
        i=0
        while 1:
            if i > start_line:
                line = iter.get_line()
                print line.get_extents()
                cr.rel_move_to(0, 6)
                cr.show_layout_line(line)
                print "i:",i
            i += 1
            if not (i < end_line and iter.next_line()):
                break
        """

    def begin_print(self, operation, context):
        """
        width = context.get_width()
        height = context.get_height()
        self.layout = context.create_pango_layout()
        print width, height

        self.layout.set_font_description(pango.FontDescription("Sans 12"))
        self.layout.set_width(int(width*pango.SCALE))
        self.layout.set_text("Phone Repairer a\nPhone Repairer Phone Repairer\nPhone Repairer\nPhone Repairer")

        num_lines = self.layout.get_line_count()
        print "num_lines: ", num_lines
        self.lines_per_page = math.floor(context.get_height() / 6)
        print "lines_per_page: ", self.lines_per_page
        #lines = self.layout.get_line_count()
        pages = ( int(math.ceil( float(num_lines) / float(self.lines_per_page) ) ) )
        """
        operation.set_n_pages(1)

    def printing(self, *args):
        print "printing"
        
        self.layout = None
        self.font_size=12
        self.lines_per_page=0
        
        setup = gtk.PageSetup()
        #setup.set_orientation(gtk.PAGE_ORIENTATION_LANDSCAPE)
        setup.set_paper_size(gtk.PaperSize(gtk.PAPER_NAME_A4))
        
        print_op = gtk.PrintOperation()
        print_op.set_default_page_setup(setup)
        print_op.set_unit(gtk.UNIT_MM)
        
        #print_op.set_n_pages(1)
        print_op.connect("draw_page", self.draw_page)
        print_op.connect("begin_print", self.begin_print)

        res = print_op.run(gtk.PRINT_OPERATION_ACTION_PREVIEW)
        
    def addloan(self, *args):
        dlg = AddLoanDlg(self, self.model)
        res = dlg.run()

    def editloan(self, *args):
        (path, col) = self.view.get_cursor()
        dlg = EditLoanDlg(self, self.model, self.model.get_iter(path))
        dlg.run()

    def delloan(self, *args):
        dlg = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, \
                                      gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, \
                                      "Fakt jo?")
        dlg.set_title("Chyba")
        res = dlg.run()
        if res == gtk.RESPONSE_YES:
            (path, col) = self.view.get_cursor()
            iter = self.model.get_iter(path)
            self.model.delete(iter)
            self.uimanager.get_action('/MenuBar/Loans/Edit').set_sensitive(False)
            self.uimanager.get_action('/MenuBar/Loans/Del').set_sensitive(False)
        dlg.hide()

    def on_row_actived(self, widget, path, column):
        dlg = EditLoanDlg(self, self.model, self.model.get_iter(path))
        dlg.run()

    def on_cursor_changed(self, *args):
        self.uimanager.get_action('/MenuBar/Loans/Edit').set_sensitive(True)
        self.uimanager.get_action('/MenuBar/Loans/Del').set_sensitive(True)

    def delete_event(self, widget, event, data=None):
        return False
    
    def destroy(self, widget, data=None):
        gtk.main_quit()
        
    def aboutdialog(self, widget, data=None):
        dlg = AboutDlg()
        dlg.run()
