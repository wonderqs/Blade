#!/usr/bin/env python
# encoding: utf-8

class Payloader(object):
    """Payloads base class"""

    # Contructor
    # param: password
    # return: none
    def __init__(self, password):
        self.password = password

    # Override this method
    # param: osType, pwd, cmd, payload
    # return: none
    def parseCmd(self, osType, pwd, cmd, payload):
        pass

    # Override this method
    # param: remoteFilePath, payload
    # return: none
    def parseDownload(self, remoteFilePath, payload):
        pass

    # Override this method
    # param: remoteFilePath, fileContent, payload
    # return: none
    def parseUpload(self, remoteFilePath, fileContent, payload):
        pass

    # Override this method
    # param: dbms, dbHost, dbUserName, dbPassword, db, sql, payload
    # return: none
    def parseSql(self, dbms, dbHost, dbUserName, dbPassword, db, sql, payload):
        pass

    # Get a payload run command
    # param: osType, pwd, cmd, payload
    # return: payload
    def getCmdPayload(self, osType, pwd, cmd):
        payload = {}
        self.parseCmd(osType, pwd, cmd, payload)
        return payload

    # Get a payload download a file
    # param: remoteFilePath, payload
    # return: payload
    def getDownloadPayload(self, remoteFilePath):
        payload = {}
        self.parseDownload(remoteFilePath, payload)
        return payload

    # Get a payload upload a file
    # param: osType, pwd, cmd, payload
    # return: payload
    def getUploadPayload(self, remoteFilePath, fileContent):
        payload = {}
        self.parseUpload(remoteFilePath, fileContent, payload)
        return payload

    # Get a payload run a SQL statement
    # param: dbms, dbHost, dbUserName, dbPassword, db, sql
    # return: payload
    def getSqlPayload(self, dbms, dbHost, dbUserName, dbPassword, db, sql):
        payload = {}
        self.parseSql(dbms, dbHost, dbUserName, dbPassword, db, sql, payload)
        return payload