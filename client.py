# -*- coding: utf-8 -*-

from __future__ import print_function

import grpc
from proto import hello_pb2, hello_pb2_grpc

_HOST = 'localhost'
_PORT = '8188'


def run():
    channel = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = hello_pb2_grpc.gRPCStub(channel=channel)

    name = '哈哈22sean哈哈'
    response = client.SayHello(hello_pb2.HelloRequest(name=name))
    print("received: " + response.message)


if __name__ == '__main__':
    run()
