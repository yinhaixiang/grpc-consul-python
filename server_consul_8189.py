# -*- coding: utf-8 -*-
import consul
import grpc
import time
import json
from concurrent import futures
from proto import hello_pb2, hello_pb2_grpc

_HOST = '127.0.0.1'
_PORT = 8189

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GrpcActionServicerImpl(hello_pb2_grpc.GrpcActionServicer):

    def SayHello(self, request, context):
        print("called with " + request.name)
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)


def register():
    print("register started...")
    c = consul.Consul()  # 连接consul 服务器，默认是127.0.0.1，可用host参数指定host
    check = consul.Check.tcp(_HOST, _PORT, "30s")  # 健康检查的ip，端口，检查时间

    c.agent.service.register(
        "search-service",
        f"search-service-{_PORT}",
        address=_HOST,
        port=_PORT,
        check=check
    )  # 注册服务部分
    print("注册服务search-service成功")
    print("services: " + str(c.agent.services()))


def unregister():
    print("unregister started")
    c = consul.Consul()
    c.agent.service.deregister(f"search-service-{_PORT}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GrpcActionServicer_to_server(GrpcActionServicerImpl(), server)
    server.add_insecure_port('[::]:' + str(_PORT))
    register()
    server.start()
    print(f"{_PORT} server start success")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        unregister()
        server.stop(0)


if __name__ == '__main__':
    serve()
