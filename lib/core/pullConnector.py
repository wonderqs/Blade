#!/usr/bin/env python
# encoding: utf-8

from lib.core.fileConnector import FileConnector
import os

class PullConnector(FileConnector):
    """Pull class"""

    # Constructor
    # param: url, password, server, fileList, timeout
    # return: none
    def __init__(self, url, password, server, fileList, timeout):
        FileConnector.__init__(self, url, password, server, fileList, timeout)
        self.remoteFilePath = self.fileList[0]
        if len(self.fileList) == 2:
            self.localFilePath = self.fileList[1]
        else:
            self.localFilePath = os.path.basename(self.remoteFilePath)

    # Handle fileExist usecase
    def handleIfFileExists(self, filePath):
        fname = filePath
        if os.path.exists(fname):
            print "Localfile: " +fname+ " exists!!"
            if 'no' in self.queryYesNo("Do you want to overwrite?","no"):
                print "Skipping " + fname
                return False
            else:
                print "Overwriteing " + fname
        return True

    # Download file
    # param: none
    # return: bool
    def downloadFile(self):
        payload = self.payloader.getDownloadPayload(self.remoteFilePath)
        status, result = self.postToServer(payload)
        if result != '[S]NOFILE[E]':
            if self.handleIfFileExists(self.localFilePath):
                fname = self.localFilePath
                f = file(fname, 'w')
                f.write(result)
                f.close()
                return True
        return False

    # The callable method to launch the connector
    # param: none
    # return: none
    def launch(self):
        if FileConnector.launch(self) != 'fail':
            if self.downloadFile():
                print '+ Downloading Successful'
                print ''
            else:
                print '+ Downloading Failed'
                print ''
        else:
            print 'Error: File opreation can not work'
            print ''
