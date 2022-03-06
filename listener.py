import socket,json
import time

s = socket.socket()  # 创建 socket 对象
port = 5000  # 设置端口号
try:
    s.connect(("127.0.0.1", port))
except:
    print(f'通信端口{port}被占用，请退出软件重设')
    

def send_content(content):
    s.sendall(f"content-lengths:{len(content)}".encode())
    s.recv(1024)  # 阻塞，等待另一个线程处理数据完毕后再发送
    s.sendall(content)
    s.recv(1024)  # 阻塞，等待另一个线程处理数据完毕后再发送


def response(flow):
    if "bupt.yuketang.cn/mooc-api/v1/lms/exercise/get_exercise_list" in flow.request.url:
        send_content("exercise".encode())
        send_content(flow.response.content)
        send_content(json.dumps(list(flow.request.cookies.items())).encode())
    elif "bupt.yuketang.cn/mooc-api/v1/lms/learn/classroom_info" in flow.request.url:
        send_content("classroom".encode())
        send_content(flow.request.url.encode())
