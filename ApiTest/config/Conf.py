import os
from ApiTest.utils.yamlUtil import YamlReader
import datetime
import os
current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# 1、获取项目基本目录
# 获取当前项目的绝对路径
current = os.path.abspath(__file__)
# print(current)
BASE_DIR = os.path.dirname(os.path.dirname(current))
# print(BASE_DIR)
# 定义config目录路径
_config_path = BASE_DIR + os.sep + "config"
# 定义data目录路径
_data_path = BASE_DIR + os.sep + "data"
# 定义conf.yml文件路径
_config_file = _config_path + os.sep + "conf.yml"
# 定义db_config.yml文件路径
_db_config_file = _config_path + os.sep + "db_conf.yml"
# 定义环境配置
_env_config_file = _config_path + os.sep + "env_conf.yml"
# 定义log文件路径
_log_path = BASE_DIR + os.sep + "logs" +os.sep+current_time
# 定义report目录路径
_report_path = BASE_DIR + os.sep + "report"+os.sep+current_time + os.sep+"result"

_report_html_path = BASE_DIR + os.sep + "report"+os.sep+current_time + os.sep+"html"


# print(_report_path)


def get_db_config_file():
    return _db_config_file

def get_env_config_file():
    return _env_config_file


def get_config_path():
    return _config_path


def get_config_file():
    return _config_file


def get_log_path():
    if not os.path.exists(_log_path):
        os.makedirs(_log_path)
    return _log_path


def get_data_path():
    return _data_path


def get_report_path():
    if not os.path.exists(_report_path):
        os.makedirs(_report_path)
    return _report_path

def get_report_html_path():
    if not os.path.exists(_report_html_path):
        os.makedirs(_report_html_path)
    return _report_html_path


# 2、读取配置文件
class ConfigYaml:
    # 初始yaml读取配置文件
    def __init__(self):
        # self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()
        self.env_config = YamlReader(get_env_config_file()).data()

    def get_conf_url(self,env):
        """
        获取测试的服务的配置信息
        :return:
        """
        return self.env_config[env]["host"]

    def get_conf_shop(self,env):
        return self.env_config[env]["shop_code"]

    #通过登录获取每个环境的token,返回headers
    def get_headers(self,env):
        host = self.get_conf_url(env)
        shop_code = self.get_conf_shop(env)
        login_url = host + "/login"
        headers = {
            "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50LXVzZXIiOiIwOjI2MDrpmYjomY4iLCJleHAiOjE2NDc4NDI4MjV9.DyMBBjrOQSHnxZlOoHf2B6JHj5KeQz6HxiGALYNZHuM",
            "x-shop-code": shop_code,
            "content-type": "application/json"
        }
        return headers

    def get_conf_log(self):
        # return self.config["BASE"]["log_level"]
        return self.env_config["log_level"]


    def get_conf_log_extension(self):
        # return self.config["BASE"]["log_extension"]
        return self.env_config["log_extension"]

    def get_db_config_info(self, db_alias):
        """
        根据db_alias获取该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.db_config[db_alias]

    def get_email_info(self):
        """
        获取email配置信息
        :return:
        """
        return self.config["email"]

    def get_env_config_info(self, env_alias):
        """
        根据db_alias获取该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.env_config[env_alias]


if __name__ == '__main__':
    conf_read = ConfigYaml()
    # print(conf_read.get_conf_url())
    # print(conf_read.get_conf_log())
    # print(conf_read.get_conf_log_extension())
    print(conf_read.get_env_config_info("uat"))
    # print(conf_read.get_db_config_info("stage"))
    # print(conf_read.get_email_info())
