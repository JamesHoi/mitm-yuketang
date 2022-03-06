from queue import Queue
from threading import Thread
import socket, math, sys, time
from options import *

q = Queue(maxsize=0)

class Receive_Thread(Thread):
    def __init__(self):
        super().__init__()
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.bind((COMM_HOST, COMM_PORT))
        except:
            print("接收线程无法通信")
            input(); sys.exit(0)
        self.s.listen(1)
        self.buffer_size = 1024

    def recv_content(self,c):
        data = c.recv(self.buffer_size).decode()
        c.send(data.encode())  # 让对方知道已接收到长度大小
        content_len = int(data[data.find(":") + 1:])
        buffer = bytes(); times = math.ceil(content_len / self.buffer_size)
        for i in range(times):
            buffer += c.recv(self.buffer_size)
        c.send("done".encode())  # 传输消息已完成
        return buffer

    def run(self):
        c, addr = self.s.accept()  # 建立客户端连接
        print("通信通道初始化完成")
        while True:
            q.put_nowait(self.recv_content(c))
            time.sleep(0.1)