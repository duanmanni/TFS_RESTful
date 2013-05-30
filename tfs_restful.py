#!/usr/bin/python

# TFS Restful in python
# test passed python2.4, python2.6

import sys
import urllib2
import httplib
import random

class TFS_Restful:
    def __init__(self, web_root_server, appkey):
        self.appkey = appkey
        self.web_root_server = web_root_server 
        self.req_count = 0
        self.TfsProxyServer = []
        self.set_TfsProxyServer()

    def do_webroot_request(self):
        url = "http://%s/v1/tfs.list" % (self.web_root_server)
        conn = httplib.HTTPConnection(self.web_root_server)
        conn.request("GET", url)
        rs = conn.getresponse()
        data = rs.read()
        conn.close()
        return  data


    def do_tfs_request(self, method, url, data=None, headers={}):
        try :
            proxy = self.TfsProxyServer[random.randint(0, len(self.TfsProxyServer))]
            conn = httplib.HTTPConnection(proxy)
            conn.request(method, url, data, headers)
            rs = conn.getresponse()
            if rs.status != 200:
                conn.close()
                return rs.status, None
            data  = rs.read()
            conn.close()
            self.req_count -= 1
            if self.req_count <= 0 :
                self.set_TfsProxyServer()
            return rs.status, data 
        except httplib.HTTPException:
            return 503, None
        except :
            return 500, None 

    def parse_server(self, data):
        if not data:
            return None, None
        if data == '':
            return None, None
        lines = data.split('\n')
        try :
            req_count = int(lines[0])
        except ValueError:
            print >>sys.stderr, 'Error: tfs proxy server parse failed!'
            return None, None
        if req_count <= 0 :
            print >>sys.stderr, 'Error: request count <=0 !'
            return None, None

        proxy_list = []
        for i in lines[1:]:
            if i != '' : 
                proxy_list.append(i)
        return req_count, proxy_list 

    def set_TfsProxyServer(self):
        rsp = self.do_webroot_request()
        req_count, proxy_list = self.parse_server(rsp)
        self.req_count = req_count 
        self.TfsProxyServer = proxy_list
        return req_count, proxy_list 

    # GET /v1/appkey/metadata/TfsFileName HTTP/1.1
    # type=1, force to read tfs meta in hide or deleted status
    def get_tfs_meta(self, tfsname, suffix=None, type=0):
        if suffix:
            tfsname = tfsname + suffix
        url = "/v1/%s/metadata/%s" %  (self.appkey, tfsname)
        if type == 1:
            url = "%s?type=1" % (url)
        rsp = self.do_tfs_request('GET', url)
        return rsp

    # GET /v1/appkey/TfsFileName HTTP/1.1 
    def get_tfs_data(self, tfsname):
        url = "/v1/%s/%s" %  (self.appkey, tfsname)
        rsp = self.do_tfs_request('GET', url)
        return rsp
        pass
   
    # suffix=, tfs will set the suffix
    # simple_name=1, make reading require suffix
    def write_tfs(self, data, suffix=None, simple_name=0):
        query = []
        if suffix:
            param = "suffix=%s" % suffix
            query.append(param)
        if simple_name == 1:
            param = "simple_name=1"
            query.append(param)

        if query :
            url = "/v1/%s?%s" %  (self.appkey, '&'.join(query))
        else :
            url = "/v1/%s" %  (self.appkey)

        rsp = self.do_tfs_request('POST', url, data)
        return rsp
    
    # hide=1, set tfs status to be hidden beside deleted
    def del_tfs(self, tfsname, hide=0):
        url = "/v1/%s/%s" %  (self.appkey, tfsname)
        if hide == 0:
            url = "%s?hide=1" % (url)
        rsp = self.do_tfs_request('DELETE', url)
        return rsp


