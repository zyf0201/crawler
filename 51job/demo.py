#%%
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from docx import Document
import pandas as pd
import numpy as np
import time
import random
import os


# URL
URL = "https://jobs.51job.com/{region}/p{page}/"
# Header
HEADER = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
# chrom driver path
CHROMEDRIVERPATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"


def get_job(driver, url, region, page):

    try:
        correct_url = url.format(region = region, page = page)
        print(correct_url)
        driver = driver
        driver.get(correct_url)
        elem = driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("outerHTML")
        html = etree.HTML(source_code)
    except Exception as e:
        print(e)

    # 职位名称
    title_origin = html.xpath('//*//div[@class="e "]//p[@class="info"]//span[@class="title"]//a|\
                        //*//div[@class="e ebtm"]//*//span[@class="title"]//a')
    title = [i.text for i in title_origin]
    # 公司名称
    company_origin = html.xpath('//*//div[@class="e "]//p[@class="info"]//a[@class="name"]|\
                        //*//div[@class="e ebtm"]//p[@class="info"]//a[@class="name"]')
    company = [i.text for i in company_origin]
    # 工作地点
    address_origin = html.xpath('//*//div[@class="e "]//p[@class="info"]//span[@class="location name"]|\
                        //*//div[@class="e ebtm"]//p[@class="info"]//span[@class="location name"]')
    address = [i.text for i in address_origin]

    # 薪水
    salary_origin = html.xpath('//*//div[@class="e "]//p[@class="info"]//span[@class="location"]|\
                        //*//div[@class="e ebtm"]//p[@class="info"]//span[@class="location"]')

    salary = [i.text for i in salary_origin]
    # 发布时间
    release_time_origin = html.xpath('//*//div[@class="e "]//p[@class="info"]//span[@class="time"]|\
                            //*//div[@class="e ebtm"]//p[@class="info"]//span[@class="time"]')
    release_time = [i.text for i in release_time_origin]

    order = html.xpath('//*//div[@class="e "]//p[@class="order"]//text()|\
                            //*//div[@class="e ebtm"]//p[@class="order"]//text()')
    #order = [i.text for i in order_origin]
    # 需要分成20组，每组7个属性
    n = 7
    order_group = [order[i:i + n] for i in range(0, len(order), n)]

    # 获取各个公司信息
    education_background = [i[0] for i in order_group]
    work_experience = [i[2] for i in order_group]
    company_nature = [i[4] for i in order_group]
    company_size = [i[6] for i in order_group]

    # 获取岗位描述
    position_statment_origin =  html.xpath('//*//div[@class="e "]//p[@class="text"]//text()|\
                                        //*//div[@class="e ebtm"]//p[@class="text"]//text()')
    position_statment = [i.replace(u'\xa0', u' ').replace(u'\u3000', u' ').replace(u'\u30002', u' ')\
                    .replace(u'\u30003', u' ').replace(u'\u30004', u' ') for i in position_statment_origin]

    # 数据初始化为dataframe
    dict = {
        'title': title,
        'company': company,
        'company_nature': company_nature,
        "company_size": company_size,
        'address': address,
        'salary': salary,
        'educaion_background': education_background,
        'work_experience': work_experience,
        'release_time': release_time,
        'position_statment': position_statment
        }
    df = pd.DataFrame(dict)
    # 导出到csv文件，文件名为region+page
    df.to_csv("{region}_{page}.csv".format(region = region, page = page))


if __name__ == '__main__':
    n = 1
    limit = 5000
    print(os.getcwd())    #获取当前工作目录
    os.chdir("./beijing")   #修改当前工作目录
    print(os.getcwd())    #获取当前工作目录

    driver = webdriver.Chrome(executable_path=CHROMEDRIVERPATH)
    driver.implicitly_wait(3)

    while n <= limit:
        get_job(driver, URL, 'beijing', n)
        time.sleep(random.randint(2,3))
        n = n + 1

    driver.close()
    print("job over!!")