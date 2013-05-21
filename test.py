#!/usr/bin/python
#
# test cases for tfs restful in python 
#

import sys
import urllib2
import httplib
import random
sys.path.append('./')

from tfs_restful import TFS_Restful

def test_get_meta(client, tfsname):
    print 'test get meta'
    print client.get_tfs_meta(tfsname, type=1)

def test_get_data(client, tfsname):
    print 'test get data'
    rsp = client.get_tfs_data(tfsname)
    if rsp:
        print len(rsp)

def test_write(client):
    print 'test write'
    data = 'test tfs restful write, by zhiqi 2013-05-20 '
    rsp = client.write_tfs(data, suffix='.outimg', simple_name=0)
    print 'write rsp: ', rsp
    st = eval(rsp) 
    tfs = st['TFS_FILE_NAME']
    print 'meta: ', client.get_tfs_meta(tfs)
    print 'data: ', client.get_tfs_data(tfs)

def test_delete(client):
    print 'test delete'
    data = 'test tfs restful delete, by zhiqi 2013-05-20 '
    rsp = client.write_tfs(data, suffix='.outimg')
    st = eval(rsp)
    tfs = st['TFS_FILE_NAME']
    print tfs
    print client.del_tfs(tfs, 0)
    print client.get_tfs_meta(tfs, type=1, suffix='.outimg')

if __name__ == "__main__":
    # appkey, keep it secret 
    web_root_server = sys.argv[1] 
    appkey = sys.argv[2] 
    client = TFS_Restful(web_root_server,  appkey)
    print client.req_count, client.TfsProxyServer

    tfsname = "T4WhVyXcBXXXXXXXXX"
    test_get_meta(client, tfsname)

    #test_get_data(client, tfsname)

    #test_write(client)

    #test_delete(client)

