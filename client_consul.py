# -*- coding: utf-8 -*-

from __future__ import print_function

import grpc
from dns import resolver
from dns.exception import DNSException
from proto import hello_pb2, hello_pb2_grpc

# 连接consul服务，作为dns服务器
consul_resolver = resolver.Resolver()
consul_resolver.port = 8600
consul_resolver.nameservers = ["127.0.0.1"]


def get_ip_port():
    '''查询出可用的一个ip，和端口'''
    try:
        dnsanswer = consul_resolver.query("search-service.service.consul", "A")
        dnsanswer_srv = consul_resolver.query("search-service.service.consul", "SRV")
    except DNSException:
        return None, None
    return dnsanswer[0].address, dnsanswer_srv[0].port


_HOST, _PORT = get_ip_port()
print(_HOST, _PORT)


def run():
    channel = grpc.insecure_channel(_HOST + ':' + str(_PORT))
    client = hello_pb2_grpc.GrpcActionStub(channel=channel)

    name = '哈哈22sean哈哈'
    response = client.SayHello(hello_pb2.HelloRequest(name=name))
    print("received: " + response.message)


if __name__ == '__main__':
    run()
