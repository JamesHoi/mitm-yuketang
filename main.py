import signal
import sys
import os
import time

from multiprocessing import freeze_support
from common import edit_system_proxy,stop_thread
from mitm_thread import Mitm_Listener
from analysis_thread import Analysis_Thread
from receive_thread import Receive_Thread
from front_proxy import Front_Proxy
from options import *

analysis_thread = None
receive_thread = None
listener = None
front_proxy = None


def signal_handler(sig, frame):
    # 关闭程序时取消代理
    print("正在退出...")
    global analysis_thread, listener
    edit_system_proxy(False)
    stop_thread(analysis_thread)
    stop_thread(receive_thread)
    listener.terminate()
    if UPSTREAM: front_proxy.terminate()
    os._exit(0)


if __name__ == '__main__':
    freeze_support()
    
    print("（Ctrl+C退出程序）")
    print("正在初始化软件")
    signal.signal(signal.SIGINT, signal_handler)

    # 启动通信接受
    receive_thread = Receive_Thread()
    receive_thread.start()
    # 启动抓包分析并下载
    analysis_thread = Analysis_Thread()
    analysis_thread.start()
    # 启动抓包监听
    listener = Mitm_Listener()
    listener.start()
    # 内置代理服务器
    if UPSTREAM:
        front_proxy = Front_Proxy()
        front_proxy.start()

    # 设置代理服务器，设置退出函数
    edit_system_proxy(True,PROXY_HOST,PROXY_PORT)
    print("软件初始化完成")

    # 刷新主线程等待ctrl+c
    while True:
        time.sleep(0.1)