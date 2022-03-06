from threading import Thread
from mitmproxy.tools.main import mitmdump
import sys,os,asyncio,time

from common import stop_thread

class Mitm_Listener(Thread):
    def __init__(self):
        super().__init__()
        self.start()

    def run(self):
        print("正在生成证书")
        asyncio.set_event_loop(asyncio.new_event_loop())
        mitmdump(["-q"])
        # -q console will not show

listener = Mitm_Listener()
time.sleep(2)
stop_thread(listener)
filepath = os.path.expanduser('~')+"\\.mitmproxy\\mitmproxy-ca.p12"
os.system(f"xcopy {filepath} .")
