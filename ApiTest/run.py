import os
import pytest
from config import Conf
from common.Base import allure_report
from common.Base import send_mail
import json
import pandas as pd
from PIL import ImageGrab
import xlwt

from PIL import Image,ImageFont,ImageDraw
import random

def get_case_info(folder):
    #定义总的case信息
    testcase_info = {}
    f = 'test.xls'
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('sheet1')
    for root,dirs,files in os.walk(folder):
        list = []
        for file in files:
            if '-result.json' in file:
                file_name = root+os.sep+file
                with open(file_name,encoding='utf-8') as f:
                    case = []
                    load_dict = json.load(f)
                    suite_name = load_dict['name']
                    suite_result = load_dict['status']
                    case.append(suite_name)
                    case.append(suite_result)
                    list.append(case)
        df = pd.DataFrame(list,columns=['用例名称','运行结果'])
        df.to_excel('test.xlsx',sheet_name='haha',index=False)

# def send():
#     name='测试用例      结果'
#     # result='结果'
#     # 图片颜色
#     color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
#     # 生成背景图片
#     image = Image.new('RGB', (1080, 1920), (color[0], color[1], color[2]))
#     # 在图片上留白 x开始位置 y开始位置 x结束位置  y结束位置
#     image.paste((255, 255, 255), (0, 1290, 1080, 1410))
#     # 保存原始版本
#     image.save("test.png")
#     im02=Image.open('test.png')
#     ft= ImageFont.truetype("C:\\windows\\Fonts\\SIMYOU.TTF",20)
#     draw= ImageDraw.Draw(im02)
#     draw.text((30,30),name,font=ft,fill='green')
#     im02.show()

if __name__ == '__main__':
    pass
    # report_path = Conf.get_report_path()
    # report_html_path = Conf.get_report_html_path()
    # pytest.main(["-s","--alluredir",report_path])
    # allure_report(report_path,report_html_path)
    a=r'D:\workspace\inter\ApiTest\report\2022_03_26_11_05_02\result'
    b=get_case_info(a)
    # get_case_info(report_path)
    # send_mail(report_html_path,"接口测试结果如下，如有附件请查看附件。","接口测试demo")
