

import requests
import time
import json
from hashlib import md5
import threading
from selenium import webdriver
from time import sleep

class test(object):

    def __init__(self):
        # self.env_domain = 'https://janus-stage.tenclass.com'
        self.env_domain = 'https://janus-uat.tenclass.com'

    # 获取用户token的headers
    def auto_headers(self):

        auto_test_time_stamp = int(round(time.time() * 1000))
        s = md5()
        s.update(("dGVuY2xhc3MtYXV0b3Rlc3Q=" + ":" + str(auto_test_time_stamp) + ":").encode("utf-8"))
        headers = {
            "x-autotest-sign": s.hexdigest(),
            "x-autotest-timestamp": str(auto_test_time_stamp)
        }
        return headers

    # 获取用户token
    def get_token(self, user_id):
        url = self.env_domain + "/ucenter/api/autotest/token"
        param = {
            "user_id": user_id
        }
        response = requests.get(url=url, params=param, headers=self.auto_headers())
        token = response.json().get("data")
        return token

    def into_video(self,user_id):
        token=self.get_token(user_id)
        # video_url = "https://study-stage.tenclass.com/shop/00001/video_content/course/3990/content/24330?__token={}".format(token)
        video_url = "https://study-uat.tenclass.com/shop/nwb540fd11e8063c/video_content/course/1708/content/9832?__token={}".format(token)
        print(video_url)
        browser = webdriver.Chrome(executable_path='D:\workspace\inter\ApiTest\src\chromedriver.exe')
        browser.get(video_url)
        sleep(10)
        browser.maximize_window()
        sleep(1)
        browser.find_element_by_xpath('//*[@id="video-player"]').click()
        sleep(40)
        browser.quit()

class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, uid):
        '''重写threading.Thread初始化内容'''
        threading.Thread.__init__(self)
        self.uid = uid

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        '''重写run方法'''
        # env = 'stage'
        env = 'uat'
        test().into_video(self.uid)

if __name__ == '__main__':
    # user_list=[949134146,949134149,949134145,949134144,949134147]
    # user_list=[949134121,949134125,949134115,949134117,949134120]
    # user_list=[949134096,949134095,949134099,949134068,949134092,949134094]
    user_list=[949134069,949134073,949134072,949134067]

    for uid in user_list:
        # test().into_video(user_id=949134146)
        t=myThread(uid)
        t.start()