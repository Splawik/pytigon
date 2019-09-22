## coding: utf-8

import pyodbc
import datetime
import platform

#Driver={ODBC Driver 13 for SQL Server};

if platform.system() == "Windows":
    CONNECTION_STRING=""" 
    Driver={SQL Server};
    Server=10.48.241.55;
    Database=POLBRUK_PROD;
    Uid=tech_qlikview;
    Pwd=P@55%W0rD2014;
    """
else:
    dsn = 'sqlserverdatasource'
    user = 'tech_qlikview'
    password = 'P@55%W0rD2014'
    database = 'POLBRUK_PROD'
    server = '10.48.241.55'
    driver= '{ODBC Driver 13 for SQL Server}'
    CONNECTION_STRING = 'DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+user+';PWD='+ password


class SoftlabConnection(object):
    def __init__(self):
        self.conn = None
        self.cur = None
        self.for_update = False

    def get_conn(self):
        if not self.conn:
            self.conn = pyodbc.connect(CONNECTION_STRING)
            #self.conn.setencoding('utf-8')
        return self.conn

    def get_cur(self):
        if not self.cur:
            self.cur = self.get_conn().cursor()
        return self.cur

    def execute(self, stament, for_update=False):
        try:
            self.get_cur().execute(stament)
        except:
            self.conn = None
            self.cur = None
            self.get_cur().execute(stament)
        if for_update:
            self.for_update = True

    def fetchall(self):
        return self.get_cur().fetchall()

    def iterall(self):
        def result_iter(cursor, arraysize=512):
            lp = 0
            while True:
                results = self.get_cur().fetchmany(arraysize)
                if not results:
                    break
                for result in results:
                    yield result
                    lp += 1
        return result_iter(self.get_cur())

    def commit(self):
        self.get_conn().commit()

    def close(self):
        if self.conn:
            if self.for_update:
                self.commit()
            if self.cur:
                self.cur.close()
                self.cur = None
            self.conn.close()
            self.conn = None
        self.for_update = False

    def __enter__(self):
        self.close()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type != None:
            self.for_update = False
        self.close()
