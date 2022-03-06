from threading import Thread
from multiprocessing import Process
from mitmproxy.tools.main import mitmdump
import sys,os,asyncio
from options import *


def program_dir():
    return sys._MEIPASS + "\\" if hasattr(sys, 'frozen') else os.getcwd() + "\\"


class Mitm_Listener(Process):
    def __init__(self):
        super().__init__()

    def replace_file(self, filename, src, dest):
        with open(filename, "r", encoding="UTF-8") as f1: content = f1.read()
        with open(filename, "w", encoding="UTF-8") as f2: f2.write(content.replace(src, dest))

    def run(self):
        self.replace_file(program_dir() + "listener.py", "555555", str(COMM_PORT))
        asyncio.set_event_loop(asyncio.new_event_loop())
        mitmdump(["-p", str(PROXY_PORT),
                    "-s",program_dir() + "listener.py"]
                    +(["--set", "stream_large_bodies=1"] if STREAMING else [])
                    +([] if DEBUG else ["-q"])
                    +(["--mode", f"upstream:http://{FRONT_PROXY_HOST}:{FRONT_PROXY_PORT}"] if UPSTREAM else []))
        # -q console will not show