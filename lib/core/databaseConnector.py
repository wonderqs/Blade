#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import json
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
            resultSet = json.loads(result)
            return resultSet

    # Print the result of SQL query
    # param: resultSet
    # return: none
    def printResult(self, resultSet):
        matrix = [[]]
        temp = []
        length = []
        for key, value in resultSet[0].items():
            matrix[0].append(str(key)) 
        for i in resultSet:
            for key, value in i.items():
                temp.append(str(value))
            matrix.append(temp)
            temp = []
        maxLen = 0
        for i in range(0, len(matrix[0])):
            for j in range(0, len(matrix)):
                currLen = len(str(matrix[j][i]))
                if currLen > maxLen:
                    maxLen = currLen
            length.append(maxLen)
            maxLen = 0
        matrix.insert(0, length)
        
        for i in range(0, len(matrix[0])):
            sys.stdout.write('+')
            for j in range(0, matrix[0][i]):
                sys.stdout.write('-')
        sys.stdout.write('+')
        sys.stdout.write('\n')
        
        for k in range(0, len(matrix[1])):
            sys.stdout.write('|')
            sys.stdout.write(matrix[1][k])
            for l in range(0, matrix[0][k] - len(matrix[1][k])):
                sys.stdout.write(' ')
        sys.stdout.write('|')
        sys.stdout.write('\n')

        for i in range(0, len(matrix[0])):
            sys.stdout.write('+')
            for j in range(0, matrix[0][i]):
                sys.stdout.write('-')
        sys.stdout.write('+')
        sys.stdout.write('\n')
        
        for i in range(0, len(matrix) - 2):
            for k in range(0, len(matrix[i + 2])):
                sys.stdout.write('|')
                sys.stdout.write(matrix[i + 2][k])
                for l in range(0, matrix[0][k] - len(matrix[i + 2][k])):
                    sys.stdout.write(' ')
            sys.stdout.write('|')
            sys.stdout.write('\n')
        
        for i in range(0, len(matrix[0])):
            sys.stdout.write('+')
            for j in range(0, matrix[0][i]):
                sys.stdout.write('-')
        sys.stdout.write('+')
        sys.stdout.write('\n')

    # Launch the connector
    # param: none
    # return: none
    def launch(self):
        try:
            if Connector.launch(self) != 'fail':
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
                            try:
                                self.printResult(result)
                            except IndexError:
                                print 'Empty Set'
                            sql = raw_input('> ')
                else:
                    print '- Error: Can not connect to DBMS'
                    print ''
            else:
                print '- Error: Can not connect to DBMS'
                print ''
        except KeyboardInterrupt:
            pass
