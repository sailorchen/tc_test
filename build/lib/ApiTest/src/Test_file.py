import requests
import time
import json
from hashlib import md5
import threading
# from api.logger import logger_consle
import linecache
import random
from selenium import webdriver
from time import sleep
from faker import Faker

faker = Faker("zh-CN")


class test_file():

    def __init__(self, env):
        # config = open(file="config.json",mode="r")
        # config_read = config.read()
        # config_dict = json.loads(config_read)
        env_admin_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50LXVzZXIiOiIwOjExODrpmYjomY4iLCJleHAiOjE2NDQ4ODk2NTN9.iZQNvhnXBbzJBW_RhTSWgxtv0KifxzOwbDtLxN9dpdg'
        env_user_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50LXVzZXIiOiIwOjk4NDU6dGVzdCIsImV4cCI6MTYzNDYyODA1M30.FBSmFK_QSCElDZJWxWbL-uspIcP_is2ftgXl-heEa3M'
        # self.env_domain = config_dict[env]["domain"]
        # self.env_shop_id = config_dict[env]["shop_id"]
        # self.env_course_id = config_dict[env]["course_id"]
        # self.env_camp_id = config_dict[env]["camp_id"]
        # self.env_live_id = config_dict[env]["live_id"]
        # self.content_id = config_dict[env]["content_id"]

        # self.env_domain = 'https://janus-stage.tenclass.com'
        # self.env_shop_id = '00001'
        # self.env_course_id = 2832
        # self.env_camp_id = 3169
        # self.env_live_id = 11800
        # self.content_id = 23418
        # self.env = env

        self.env_domain = 'https://janus-uat.tenclass.com'
        self.env_shop_id = 'nwb540fd11e8063c'
        self.env_course_id = 624
        self.env_camp_id = 1233
        self.env_live_id = 4794
        self.content_id = 9132
        self.env = env

        self.admin_env_header = {
            "authorization": env_admin_token,
            "x-shop-code": self.env_shop_id
        }
        self.user_env_header = {
            "authorization": env_user_token,
            "x-shop-code": self.env_shop_id
        }
        # config.close()

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

    # 用户授权接口
    def user_grant(self, user_id):
        url = self.env_domain + "/study-center/admin/api/v1/user/course/grant"
        body = {
            "user_id": user_id,
            "course_id": self.env_course_id,
            "camp_id": self.env_camp_id
        }
        response = requests.post(url=url, headers=self.admin_env_header, json=body)
        print(response.json())
        # logger_consle.info(response.status_code)
        # logger_consle.info(response.content.decode())

    # 用户保持在线状态接口,需要在请求头加上断开连接"Connection": 'close'
    def user_online_ping(self, user_id, token):
        url = self.env_domain + "/nuoan-guard/api/v1/track/event"
        user_ping_header = {
            "authorization": token,
            "x-shop-code": self.env_shop_id,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.15 Safari/537.36",
            "Connection": 'close'
        }
        test_time = time.time()
        now_time = round(test_time, 3)

        body = {
            "type": "user_live_ping",
            "data": {"user_id": user_id,
                     "live_id": self.env_live_id,
                     "ping_time": now_time,
                     "content_id": self.content_id,
                     "live_stage": 1}}
        print(body)
        response = requests.post(url=url, headers=user_ping_header, json=body)
        print(response.json())
        # logger_consle.info(response.content.decode())

    # 获取用户token
    def get_token(self, user_id):
        url = self.env_domain + "/ucenter/api/autotest/token"
        param = {
            "user_id": user_id
        }
        response = requests.get(url=url, params=param, headers=self.auto_headers())
        # logger_consle.info(response.status_code)
        # logger_consle.info(response.content.decode())
        token = response.json().get("data")
        return token

    #分配销售
    def comminutity_assign(self,user_id):
        url = "http://10.0.30.40:30499/api/v2/took-order/group-session/community/get"
        param = {
            "course_id": 1599,
            "user_id": user_id,
            "source_from":"COURSE"
        }
        headers = {
                "Content-Type":"application/json",
                "shop-id":"10016",
                "current-user":"1:118:xxx"
        }
        response = requests.post(url=url, headers=headers, json=param)
        print(response.json())
        return response.json()

    # 用户进入直播间
    def user_clien(self, token):
        url = self.env_domain + "/study-center/api/v1/live/client_access?content_id=" + str(self.content_id)
        headers = {
            "authorization": token,
            "x-shop-code": self.env_shop_id
        }
        response = requests.get(url=url, headers=headers)
        print(response)
        # logger_consle.info(response.content.decode())

    # 上报用户设备
    def user_driver(self, user_id):
        auto_test_time_stamp = int(round(time.time() * 1000))
        token = self.get_token(user_id=user_id)
        url = self.env_domain + "/study-center/api/v1/practice_student_report.computer_info"
        # logger_consle.info(url)
        headers = {
            "authorization": token,
            "x-shop-code": self.env_shop_id
        }
        body = {
            "event_type": "live_practice",
            "event_id": self.content_id,
            "computer_info": "{\"speed\":2.3,\"system\":\"Windows\",\"browser\":\"chrome/93.0.4577 chrome/93\",\"screenH\":1080,\"screenW\":1920,\"gpu\":\"ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8682)\",\"ua\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.15 Safari/537.36\",\"loadAndDidMountTime\":439}",
            "pc_state": 0
        }
        # \"liveDidMountTime\":1631160340356
        body['liveDidMountTime'] = auto_test_time_stamp
        response = requests.post(url=url, headers=headers, json=body)
        # logger_consle.info(response.content.decode())

    # 用户ping事件1
    def user_re_onlline1(self, user_id):
        user_token = self.get_token(user_id)
        self.user_online_ping(user_id=user_id, token=user_token)

    # 用户ping事件
    def user_re_onlline(self, user_id, user_token):
        # user_token = self.get_token(user_id)
        self.user_online_ping(user_id=user_id, token=user_token)

    # 用户实际进入直播间
    def user_re_clien1(self, user_id):
        user_token = self.get_token(user_id)
        self.user_clien(token=user_token)

    # 用户实际进入直播间
    def user_re_clien(self, token):
        # user_token = self.get_token(user_id)
        self.user_clien(token=token)

    # 创建用户
    def create_user(self):
        # url = "http://janus-stage.tenclass.com/ucenter/api/autotest/users"
        url = "http://janus-uat.tenclass.com/ucenter/api/autotest/users"

        body = {
            "name": faker.name(),
            "sex": 0,
            "avatar_url": "https://thirdwx.qlogo.cn/mmopen/vi_32/HMkyblPicgl2qfUGwicdVnqMpzHyMx1kKLzLhqIHicKMJrrtuoJdF1lxMwjBg9HyQI6UCFHbFn8tCh3icAKa0AmnCQ/132",
            "mobile_phone": faker.phone_number(),
            # "mobile_phone": 13222222222,
            "city": faker.city(),
            "country": "中国",
            "province": faker.province()
        }
        response = requests.post(url=url, headers=self.auto_headers(), json=body)
        print(response.json().get("data").get("id"))

    def test(self):
        # user_id : 3564 8631
        # 进入直播间
        # self.user_grant(user_id=user_id)
        # self.user_re_clien(user_id=user_id)
        user_id, token = self.get_id_token().split(',')
        # print(user_id)
        token = token.replace('\n', '')
        print(user_id,token)
        # self.get_token(user_id=user_id)
        # # 保持在线
        # token = self.get_id_token()
        keep_min = 10
        # self.user_driver(user_id)
        for i in range(keep_min * 6):
            self.user_re_onlline(user_id=user_id,user_token=token)
            # time.sleep(5)
        self.user_driver(user_id=user_id)

    def test2(self):
        # user_id : 3564 8631
        # 进入直播间
        # self.user_grant(user_id=user_id)
        # self.user_re_clien(user_id=user_id)
        try:
            user_id, token = self.get_id_token().split(',')
            token = token.replace('\n', '')
            self.user_re_clien(token=token)
            # # 保持在线
            keep_min = 10
            self.user_driver(user_id)
            for i in range(keep_min * 6):
                self.user_re_onlline(user_id=user_id, user_token=token)
                time.sleep(10)
            # self.user_driver(user_id=user_id)
        except Exception as e:
            print(e)

    # 写token和用户id到txt文件
    def write_token(self, user_id):
        token = self.get_token(user_id=user_id)
        print(token)
        if token:
            # print(token)
            with open('token.txt', 'a+') as f:
                f.writelines(str(user_id) + ',' + token + '\n')

    # 获取id和token
    def get_id_token(self):
        max_line = len(self.get_ids_token())
        line_random = random.randint(1, max_line)
        return linecache.getline('token.txt', line_random)

    # get
    def get_ids_token(self):
        with open('token.txt') as f:
            return f.readlines()

    # 使用selenium进入直播间
    def into_live_room(self, token):
        user_id, token = self.get_id_token().split(',')
        # print(user_id)
        token = token.replace('\n', '')
        print(user_id)
        live_url = r"https://study-{}.tenclass.com/shop/{}/live/{}?is_pc=1&__token={}".format(self.env,
                                                                                              self.env_shop_id,
                                                                                              self.content_id, token)
        print(live_url)
        browser = webdriver.Chrome()
        browser.get(live_url)
        sleep(20)
        for x in range(2):
            words = faker.sentence()
            browser.find_element_by_xpath('//*[@id="textarea"]').click()
            browser.find_element_by_xpath('//*[@id="textarea"]').send_keys(words)
            sleep(1)
            browser.find_element_by_xpath('//*[@id="input-wrapper"]/div[3]/div[2]').click()
            sleep(1)
        browser.quit()


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, name, uid, token):
        '''重写threading.Thread初始化内容'''
        threading.Thread.__init__(self)
        self.threadName = name
        self.uid = uid
        self.token = token

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        '''重写run方法'''
        # env = 'stage'
        env = 'uat'
        # test_file(env=env).user_grant(user_id=self.uid)
        # test_file(env=env).write_token(user_id=self.uid)
        # test_file(env=env).comminutity_assign(user_id=self.uid)
        # test_file(env=env).test()
        test_file(env=env).into_live_room(self.token)
        # test_file(env=env).test2()


if __name__ == '__main__':
    """
    1.课程授权=》test_file(env='uat').user_grant(user_id=a)  
    =>stage(4203,7364)
    =>uat(507443,508202)(600000,601999)
    2.保存user_id和token =》  test_file(env='uat').write_token(user_id=a)
    3.分配销售 
    4.到播  test_file(env='uat').into_live_room()
    5.时长上报和设备上报  test_file(env='uat').test2()
    """
    # test_file(env='uat').test()
    # t = myThread("xiaoming", 6000, 6075)
    # t.start()
    # 课程授权
    # for i in range(507825,508202):
    #     print(i)
    #     # test_file(env='uat').user_grant(user_id=i)
    #     # test_file(env='stage').write_token(user_id=i)
    #     test_file(env='uat').write_token(user_id=i)
    # 写token
    # for a in [949134134,949134135,949134137,949134138,949134140,949134136,949134139,949134141,949134142,949134143,949134125,949134127,949134128,949134130,949134124,949134126,949134129,949134131,949134132,949134133]:
    for a in range(4203,4207):
        x = myThread(a, a, a)
        x.start()
    # 到播
    # for a in test_file(env='stage').get_ids_token():
    #     uid,token = a.split(',')
    #     token= token.replace("\n","")
    #     print(uid)
    #     test_file(env='stage').into_live_room(token)
    # 时长和设备上报
    # number = len(test_file(env='uat').get_ids_token())
    # print(number)
    # for a in range(number):
    #     x = myThread(a, a, a)
    #     x.start()
    # for a in test_file(env='uat').get_ids_token():
    #     uid,token = a.split(',')
    #     token= token.replace("\n","")
    #     x = myThread(a, uid, token)
    #     x.start()
