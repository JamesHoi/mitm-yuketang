from threading import Thread
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import urlparse, parse_qs
import json, os, time, sys
import requests
import itertools
import random

from options import *
from receive_thread import q

def printf(data,end="\n"):
    print(data,end=end)
    sys.stdout.flush()


class Analysis_Thread(Thread):
    def __init__(self):
        super().__init__()
        self.classroom_id = 0

    def recv_content(self):
        while True:
            try: return q.get_nowait()
            except: time.sleep(0.1)

    def get_time_str(self):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def printf_all_answer_by_index(self,problems):
        for problem in problems:
            if problem['user']['is_show_answer']: continue
            content = problem['content']; i = problem['index']
            if not hasattr(content,'answerIndex'):
                self.printf_all_answer_by_trying([problem])
                continue
            if content['TypeText'] != '单选题': continue
            problem_id = problem['problem_id']
            answer = chr(ord("A")+content['answerIndex'])
            if AUTO_MODE:
                success = self.try_get_answer(problem_id,[answer])
                assert success
                time.sleep(random.uniform(2,3))
                printf(f"{i}.",end="")
            printf(answer,end=" " if i%10 else "\n")

    def try_get_answer(self,problem_id,answer_list):
        url = "https://bupt.yuketang.cn/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=2841"
        payload = json.dumps({
        "classroom_id": self.classroom_id,
        "problem_id": problem_id,
        "answer": answer_list
        })
        headers = {
        'Cookie': '; '.join([f'{c[0]}={c[1]}' for c in self.cookies]),
        'X-CSRFToken': self.cookies[0][1],
        'xtbz': 'cloud',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload,verify=False)
        try:
            return json.loads(response.content.decode())['data']['is_show_answer']
        except Exception:
            try: txt = json.loads(response.content.decode())
            except: return self.try_get_answer(problem_id,answer_list)
            if "detail" in txt: tmp = ['detail'][45:]
            else: 
                printf("未知错误，请重新刷新网页")
                time.sleep(0.5)
                return self.try_get_answer(problem_id,answer_list)
            printf("被服务器发现请求太快，需等待"+tmp)
            printf("程序正在等待")
            time.sleep(float(tmp[:-8])+0.1)
            return self.try_get_answer(problem_id,answer_list)


    def get_all_choice(self,op_num,is_single=False):
        # op_num: 题目选项个数
        assert op_num >= 1
        choice = []
        gen_list = list('ABCDEFGH'[:op_num])
        choice_num = 1 if is_single else len(gen_list) # 最大可选数
        for i in range(1,choice_num+1):
            iter = itertools.combinations(gen_list,i)
            choice.extend([list(c) for c in list(iter)])
        if is_single == False: choice = [list("ABCD"),list("ABC")] + choice # 这两个选项可能性较大
        return choice

    def printf_all_answer_by_trying(self,problems):
        for problem in problems:
            if problem['user']['is_show_answer']: continue
            problem_id = problem['problem_id']
            content = problem['content']; i = problem['index']
            typetext = content['TypeText']
            if typetext != '单选题' and typetext != '多选题' and typetext != '判断题': continue
            op_num = len(content['Options'])
            if typetext != '判断题':
                choice = self.get_all_choice(op_num,is_single=typetext=='单选题')
            else: choice = [["true"],["false"]]
            for answer in choice:
                success = self.try_get_answer(problem_id,answer)
                time.sleep(random.uniform(2,3))
                if success: break
            printf(f"{i}."+"".join(answer),end=" " if i%10 else "\n")
            time.sleep(random.uniform(2,2.5))

    def run(self):
        while True:
            mode = self.recv_content().decode()
            if mode == "classroom":
                url = self.recv_content().decode()
                self.classroom_id = int(parse_qs(urlparse(url).query)['classroom_id'][0])
            else:
                tmp = self.recv_content()
                if DEBUG: printf(tmp)
                data = json.loads(tmp.decode())
                self.cookies = json.loads(self.recv_content().decode())
                if not ('data' in data and 'problems' in data['data']): 
                    printf("程序解析有误")
                    continue
                if not DEBUG: os.system("cls")
                printf("成功获取到题目信息 "+self.get_time_str())
                printf(data['data']['name'])
                printf("")
                printf("（请按Ctrl+C键退出）")
                printf("（请不要多开此软件，没有作用）")
                printf("（注：只支持单选题、多选题和部分判断题，做完的题目不显示答案）")
                problems = data['data']['problems']
                if 'answerIndex' in problems[0]['content']:
                    if AUTO_MODE: printf("成功获取到全部答案，正在自动提交答案")
                    else: printf("成功获取到全部答案，请手动填入答案防止服务器发现")
                    self.printf_all_answer_by_index(problems)
                else:
                    printf("无法获取到答案，正在自动尝试做题，请耐心等待\n题目结果显示完全后刷新浏览器界面即可看到已完成")
                    self.printf_all_answer_by_trying(problems)
                printf("\n已完成")
