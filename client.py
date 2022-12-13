#!E:\python\venv\Scripts

# -*- coding:utf-8 -*-

import socket
import sys

def post_request():
    ip = get_ip()
    req = f"{ip}"
    return req

def start_request(master_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((master_ip, 3000))
    req = post_request()
    s.send(req.encode())
    buff = []
    while True:
        d = s.recv(1024).decode()
        if d:
            buff.append(d)
        else:
            break
    data = ''.join(buff)
    # 服务端返回响应
    print(data)
    s.close()



def get_ip() -> str:
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    # print(ip)
    return ip


if __name__ == '__main__':
    # start_request()
    # input("press any key to exit;")
    # a = get_map()
    master_ip = sys.argv[1]
    start_request(master_ip)
    # print(a)
