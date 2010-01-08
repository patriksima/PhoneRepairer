#!/usr/bin/env python
# coding: utf-8

import sqlite3

from singleton import Singleton

class DB(Singleton):
    def __init__(self):
        try:
            self.conn = sqlite3.connect("./data.db", detect_types=sqlite3.PARSE_DECLTYPES)
            self.curs = self.conn.cursor()
        except sqlite3.OperationalError, e:
            print "sqlite3: %s" % e
        
        sqlite3.register_adapter(str, lambda s:s.decode('utf-8'))
        sqlite3.register_adapter(bool, lambda x:int(x))
        sqlite3.register_converter('BOOLEAN', lambda x:bool(int(x)))
        
        self.commit  = self.conn.commit
        self.execute = self.curs.execute
        
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return getattr(self.curs, name)

if __name__ == "__main__":
    db = DB.getInstance()
    for row in db.execute("Select * from loans"):
        print row
