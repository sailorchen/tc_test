from ApiTest.config import Conf
import os
from ApiTest.utils.yamlUtil import YamlReader
import pytest
from ApiTest.config.Conf import ConfigYaml
from ApiTest.utils.RequestsUtil import Request
from ApiTest.utils.AssertUtil import AssertUtil
import allure
from ApiTest.common.Base import allure_report

# 获取测试用例内容list
# 获取testlogin.yml文件路径
test_file = os.path.join(Conf.get_data_path(), "test_xiansuo_uat.yml")
# 使用工具类来读取多个文档内容
data_list = YamlReader(test_file).data_all()


# 参数化执行测试用例
@allure.feature("线索管理-线索用户名搜索")
class TestXianSuo:
    @pytest.mark.parametrize("search", data_list)
    def test_yml(self, search):
        # 初始化URL,data
        env = "uat"
        con = ConfigYaml()
        url = con.get_conf_url(env=env) + search["url"]
        headers = con.get_headers(env=env)
        data = search["data"]
        case_name = search["case_name"]
        print(case_name)
        allure.dynamic.title(case_name)
        allure.dynamic.description("请求body==>> %s" % str(data))
        request = Request()
        res = request.post(url=url, json=data,headers=headers)
        assert_res = AssertUtil()
        assert_res.assert_code(res["code"], search["except"]["code"])
        assert_res.assert_body(res["body"]["msg"], search["except"]["msg"])


if __name__ == '__main__':
    # report_path = Conf.get_report_path()+os.sep+"result"
    # report_html_path = Conf.get_report_path()+os.sep+"html"
    pytest.main(["-s", "test_login.py", "--alluredir", "./report/result"])
    # allure_report(report_path,report_html_path)
