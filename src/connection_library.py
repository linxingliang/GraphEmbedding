# -*-coding:utf-8-*-
import pymysql
from pystalkd.Beanstalkd import Connection
import redis
import requests
import hashlib
import sys
sys.path.append(r'../pb')
from disk_file_system_pb2 import RealTimeRecOp, RealTimeRequest, RealTimeResponse, dataSource
from sshtunnel import SSHTunnelForwarder


def get_db(host='172.31.61.41', username='hwdata', password='Pass4dat@2018!0',
           port=3306, database='report_db', mode='remote'):
    """
    连接数据库
    :param mode: Remote为远程连接， Server为服务器连接
    :return:
    """
    if mode == 'server':
        con = pymysql.connect(host=host,
                              user=username,
                              password=password,
                              port=port,
                              db=database,
                              charset='utf8mb4')
    elif mode == 'remote':
        server = SSHTunnelForwarder(
            # 指定ssh登录的跳转机的address
            ssh_address_or_host=('localhost', 6001),
            ssh_username='duser',
            ssh_pkey='../data/id_rsa',
            # 设置数据库服务地址及端口
            remote_bind_address=(host, port))
        server.start()
        con = pymysql.connect(host='127.0.0.1',
                              user=username,
                              password=password,
                              port=server.local_bind_port,
                              db=database, charset='utf8mb4')
    else:
        raise Exception('Select server or remote mode')
    return con


def get_beanstalk_conn(host, port, mode='server'):
    if mode == 'remote':
        server = SSHTunnelForwarder(
            # 指定ssh登录的跳转机的address
            ssh_address_or_host=('localhost', 6001),
            ssh_username='duser',
            ssh_pkey='../data/id_rsa',
            # 设置数据库服务地址及端口
            remote_bind_address=(host, port))
        server.start()
        con = Connection('127.0.0.1', server.local_bind_port)
    elif mode == 'server':
        con = Connection(host=host, port=port)
    else:
        raise Exception('Select server or remote mode')
    return con


def get_redis_con(host, passwd, port, mode='server'):
    if mode == 'remote':
        server = SSHTunnelForwarder(
            # 指定ssh登录的跳转机的address
            ssh_address_or_host=('localhost', 6001),
            ssh_username='duser',
            ssh_pkey='../data/id_rsa',
            # 设置数据库服务地址及端口
            remote_bind_address=(host, port))
        server.start()
        con = redis.Redis(host='127.0.0.1', port=server.local_bind_port, password=passwd)
    elif mode == 'server':
        con = redis.Redis(host=host, port=port, password=passwd)
    else:
        raise Exception('Select server or remote mode')
    return con


class DiskFileSystem(object):
    def __init__(self, disk_host, disk_port=4102, mode='server'):
        self.disk_host = disk_host
        self.disk_port = disk_port
        self.mode = mode

    def set_data_to_disk(self, key, value, data_source):
        if self.mode == 'remote':
            server = SSHTunnelForwarder(
                # 指定ssh登录的跳转机的address
                ssh_address_or_host=('localhost', 6001),
                ssh_username='duser',
                ssh_pkey='../data/id_rsa',
                # 设置数据库服务地址及端口
                remote_bind_address=(self.disk_host, self.disk_port))
            server.start()
            url = r'http://127.0.0.1:{}/real_time_rec_io'.format(server.local_bind_port)
        elif self.mode == 'server':
            url = r'http://{}:{}/real_time_rec_io'.format(self.disk_host, self.disk_port)
        else:
            raise Exception('Select server or remote mode')
        data_request = RealTimeRequest()
        data_request.key = key
        data_request.value = value
        data_request.source_type = data_source
        data_request.operate = RealTimeRecOp.RealTimeRecSetData
        request = data_request.SerializeToString()
        response = requests.post(url, data=request)
        return response.content

    def get_data_from_disk(self, key, data_source):
        if self.mode == 'remote':
            server = SSHTunnelForwarder(
                # 指定ssh登录的跳转机的address
                ssh_address_or_host=('localhost', 6001),
                ssh_username='duser',
                ssh_pkey='../data/id_rsa',
                # 设置数据库服务地址及端口
                remote_bind_address=(self.disk_host, self.disk_port))
            server.start()
            url = 'http://127.0.0.1:{}/real_time_rec_io'.format(server.local_bind_port)
        elif self.mode == 'server':
            url = r'http://{}:{}/real_time_rec_io'.format(self.disk_host, self.disk_port)
        else:
            raise Exception('Select server or remote mode')
        data_request = RealTimeRequest()
        data_request.key = key
        data_request.value = b""
        data_request.source_type = data_source
        data_request.operate = RealTimeRecOp.RealTimeRecGetData
        request = data_request.SerializeToString()
        response = requests.post(url, data=request)
        pb_response = RealTimeResponse()
        pb_response.ParseFromString(response.content)
        received_data = pb_response.value
        return received_data


if __name__ == '__main__':
    # get_db(mode='remote')
    print('test')
    DG = DiskFileSystem("172.31.61.42")
    data = DG.get_data_from_disk('4313281170', dataSource.Abroad_UserBehavior)
    print(data)
