#!/usr/bin/env python
# encoding: utf-8

from lib.core.connector import Connector

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
