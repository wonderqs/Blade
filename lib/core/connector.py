#!/usr/bin/env python
# encoding: utf-8

import pdb
import httplib2
from urllib import urlencode
from lib.generic import Interaction
from payloads.php import PhpPayloader
from payloads.asp import AspPayloader
from payloads.aspx import AspxPayloader

class Connector(object, Interaction):
    """The base class for all functions"""

    # Constructor
    # param: url, password, server, timeout
    # return: none
    def __init__(self, url, password, server, timeout):
        self.url = url
        self.timeout = timeout
        self.password = password
        self.server = server
        if server == 'php':
            self.payloader = PhpPayloader(password)
        elif server == 'asp':
            self.payloader = AspPayloader(password)
        elif server == 'aspx':
            self.payloader = AspxPayloader(password)
        elif server == 'jsp':
            self.payloader = JspPayloader(password)

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
            print '- HTTP Error'
            print '- Status Code: ' + resp['status']
            status = 'fail'
        return status, content

    # Request server with POST method
    # param: data
    # return: none
    def postToServer(self, data):
        status = 'success'
        if "aspx" == self.server:
            param = data[self.password]
        else:
            param = urlencode(data)
        header = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        h = httplib2.Http(timeout = self.timeout)
        resp, content = h.request(self.url, "POST", param, header)
        if resp['status'] != '200':
            print '- HTTP Error'
            print '- Status Code: ' + resp['status']
            status = 'fail'
        return status, content

    # Test whether the connection is functional or not
    # param: none
    # return: statu
    def launch(self):
        # Test the connection
        try:
            return self.getToServer({})[0]
        except httplib2.socket.error:
            print '- The host is unreachable'
            return 'fail'
