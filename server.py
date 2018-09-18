# -*- coding: utf-8 -*-
import grpc
import time
from concurrent import futures
from proto import hello_pb2, hello_pb2_grpc

_HOST = 'localhost'
_PORT = '8188'

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GrpcActionServicerImpl(hello_pb2_grpc.GrpcActionServicer):

    def SayHello(self, request, context):
        print("called with " + request.name)
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GrpcActionServicer_to_server(GrpcActionServicerImpl(), server)
    server.add_insecure_port('[::]:' + _PORT)
    server.start()
    print(f"{_PORT} server start success")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
