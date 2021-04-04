# sqlite3 handler
# TODO: More on prevention of SQL injection
import sqlite3
from utils.logger import log_adapter


logger = log_adapter.getlogger(__name__)


class DbHandler:
    def __init__(self):
        self.active = True
        self.conn = sqlite3.connect('data.db')

    def cleanup(self):
        logger.debug("Running cleanup for DbHandler")
        self.conn.close()
        self.active = False

    def create_table( self, tablename, tablestr ):
        if not self.active:
            raise Exception("Try to operate on closed db handler")
        cur = self.conn.cursor()
        sta = 'CREATE TABLE IF NOT EXISTS %s (%s)' % ( tablename, tablestr )
        cur.execute( sta )
        self.conn.commit()

    def check_exist( self, table, key, value ):
        if not self.active:
            raise Exception("Try to operate on closed db handler")
        cur = self.conn.cursor()
        sta = "SELECT * FROM %s WHERE %s='%s'" % (table, key, value )
        cur.execute( sta )
        data = cur.fetchall()
        return len(data)

    def insert( self, table, values ):
        if not self.active:
            raise Exception("Try to operate on closed db handler")
        cur = self.conn.cursor()

        sta = 'INSERT INTO %s VALUES %s' % (table, values)
        cur.execute( sta )
        self.conn.commit()

    def delete(self, table, key, value):
        if not self.active:
            raise Exception("Try to operate on closed db handler")
        cur = self.conn.cursor()
        sta = "DELETE FROM %s WHERE %s='%s'" % (table, key, value )
        cur.execute( sta )
        self.conn.commit()


dbHandler = DbHandler()
