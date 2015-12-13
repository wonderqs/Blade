#!/usr/bin/env python
# encoding: utf-8

from lib.core.fileConnector import FileConnector

class PullConnector(FileConnector):
    """Pull class"""

    # Constructor
    # param: url, password, server, fileList
    # return: none
    def __init__(self, url, password, server, fileList):
        FileConnector.__init__(self, url, password, server, fileList)
        self.remoteFilePath = self.fileList[0]
        if len(self.fileList) == 2:
            self.localFilePath = self.fileList[1]
        else:
            self.localFilePath = ''

    # Download file
    # param: none
    # return: bool
    def downloadFile(self):
        payload = self.payloader.getDownloadPayload(self.remoteFilePath)
        status, result = self.postToServer(payload)
        if result != '[S]NOFILE[E]':
            if self.localFilePath != '':
                f = file(self.localFilePath, 'w')
            else:
                f = file(self.remoteFilePath, 'w')
            f.write(result)
            f.close()
            return True
        else:
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
