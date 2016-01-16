#!/usr/bin/env python
# encoding: utf-8

import re
from lib.core.connector import Connector

class DatabaseConnector(Connector):
    """Connctor for database connections"""

    # Constructor
    # param: url, password, server, dbms, dbHost, dbUserName, dbPassword, db
    # return: none
    def __init__(self, url, password, server, dbms, dbHost, dbUserName, dbPassword, db = ''):
        Connector.__init__(self, url, password, server)
        self.dbms = dbms
        self.dbHost = dbHost
        self.dbUserName = dbUserName
        self.dbPassword = dbPassword
        self.db = db

    # Select database
    # param: db
    # return: none
    def selectDb(self, db):
        self.db = db

    # Connect to database server
    # param: none
    # return: bool
    def connect(self):
        sql = ''
        payload = self.payloader.getSqlPayload(self.dbms, self.dbHost, self.dbUserName, self.dbPassword, self.db, sql)
        status, result = self.postToServer(payload)
        if result == '[S]FAIL[E]':
            return False
        else:
            return True

    # Request a SQL statement
    # param: sql
    # return: resultSet    
    def requestSql(self, sql):
        resultSet = []
        payload = self.payloader.getSqlPayload(self.dbms, self.dbHost, self.dbUserName, self.dbPassword, self.db, sql)
        status, result = self.postToServer(payload)
        if result == '[]':
            return resultSet
        else:
            print result
            return resultSet

    # Launch the connector
    # param: none
    # return: none
    def launch(self):
        if Connector.launch(self) != 'fail':
            print '------------------------------------------------------------'
            if self.connect():
                print '+ Connection Established'
                print ''
                if self.db == '':
                    sql = 'show schemas;'
                else:
                    sql = 'show tables;'
                while sql != 'exit':
                    pattern = re.search(r'use .*', sql)
                    if pattern:
                        self.selectDb(pattern.group()[4:].split(';')[0])
                        print 'Database changed'
                        sql = raw_input('> ')
                    else:
                        result = self.requestSql(sql)
                        for i in result:
                            print i
                        sql = raw_input('> ')
            else:
                print '- Error: Can not connect to DBMS'
                print ''

