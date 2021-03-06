# file name : dbModule.py
# pwd : /project_name/app/module/dbModule.py
 
from ast import excepthandler
import pymysql
 
class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='3102',
                                  db='testDB',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
 
    def execute(self, query, args={}):
        msg=None
        try:
            self.cursor.execute(query, args)  

        except pymysql.err.IntegrityError as e:
            code, msg = e.args
            print(code, msg)            
        
        return msg        
    
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()
        
    def rollback(self):
        self.db.rollback()
