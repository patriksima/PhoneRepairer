#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from main import MainWindow

class App(object):
    @staticmethod
    def Run():
        main = MainWindow()
        main.show()
        gtk.main()
        
if __name__ == "__main__":
    App.Run()
