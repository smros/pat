#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Steve"
__date__ ="$Dec 20, 2011 9:26:33 PM$"

import sqlite3

class sqlliteDB:
    def __init__(self, dbFilename):
        try:
            self.conn=sqlite3.connect(dbFilename)
            self.conn.text_factory=str
        except:
            print 'DB Error.  Does the file exist?'

    def getCursor(self):
        try:
            c=self.conn.cursor()
        except:
            print 'Error in getCursor'
        return(c)

#    def executeTransaction(self, statement):
#        c=self.getCursor()
#        try:
#            c.execute(statement)
#            self.conn.commit()
#        except:
#            print '--------------------------------'
#            print 'Error in executeTransaction'
#            print 'The transaction I tried was: ' + statement
#            print '--------------------------------'
#        finally:
#            c.close()

    def executeTransaction2(self, prefix, values):
        c=self.getCursor()
#        try:
        c.execute(prefix, values)
        self.conn.commit()
#        except:
#            print '--------------------------------'
#            print 'Error in executeTransaction2'
        print 'The transaction I tried was: ' + prefix
        print values
        print '--------------------------------'
#            temp=raw_input('Waiting...')
#        finally:
        c.close()

    def executeQueryFetchOne(self,query):
        c=self.getCursor()
        try:
            c.execute(query)
            data=c.fetchone()[0]
        except:
            print 'Error in executeQueryFetchOne'
        finally:
            c.close()

        return(data)

    def executeQueryFetchAll2(self,prefix, query):
        c=self.getCursor()
        #try:
        print prefix
        print query
        c.execute(prefix, query)
        data=c.fetchall()
#        except:
#            print 'Error in executeQueryFetchAll'
#
#        finally:
        c.close()

        return(data)

#    def executeQueryFetchAll(self,query):
#        c=self.getCursor()
#        try:
#            c.execute(query)
#            data=c.fetchall()
#        except:
#            print 'Error in executeQueryFetchAll'
#        finally:
#            c.close()
#
#        return(data)

    def executeScript(self, myScript):
        # Executes a series of sql statements given as a script. Expected to
        # be used for table creation

        c=self.getCursor()
        try:
            c.executescript(myScript)
        except:
            print 'Error in executeScript'
        finally:
            c.close()

    def closeDB(self):
        self.conn.close()


#    d=sqlliteDB('test.db')
#
#    tableInit="""
#
#    drop table if exists quotes;
#
#    create table quotes(
#        title TEXT,
#        author TEXT,
#        locBegin INTEGER,
#        locEnd INTEGER,
#        page INTEGER,
#        dateString DATETIME,
#        content TEXT,
#        primary key (title, author, locBegin, locEnd)
#        );
#
#    create index idx1 on quotes(
#        title,
#        author,
#        locBegin,
#        locEnd
#        );
#
#    create index titles on quotes(
#        title
#        );
#
#    """
#
#    d.executeScript(tableInit)
#
#    d.closeDB()
    
