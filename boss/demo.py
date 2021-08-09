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


"""
crawl information form zhipin.com

url: https://www.zhipin.com/c101210100/?page=10&ka=page-10

region HangZhou: c101210100

Job description url: https://www.zhipin.com/job_detail/4829579ae9d2953d1nR42tu1EFtQ.html
Get from: xpath tag[job-name]
Example:
<span class="job-name">
<a href="/job_detail/4829579ae9d2953d1nR42tu1EFtQ.html" title="项目经理" 
target="_blank" ka="search_list_jname_271" 
data-securityid="f95dlJnCqBEnV-m1okqXjfLfPk3Znz5H0MUrk8EsywFftVQSexqqV
g_qOX5fTfgmiqaE0FjLw_a7Js2_x3Zmuxk2Q49snsh8EYArTKgakpVxlw~~" 
data-jid="4829579ae9d2953d1nR42tu1EFtQ" data-itemid="271" 
data-lid="9Ctkkill6T2.search.271" data-jobid="102168090" 
data-index="0">项目经理</a>
</span>

"""

REGION = {
    "hangzhou": "c101210100",
}

URL = "https://www.zhipin.com/{region}/?page={page}&ka=page-{page}"
#URL = "https://www.zhipin.com/{region}"

HEADER = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
CHROMEDRIVERPATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

# %%
correct_url = URL.format(region = REGION["hangzhou"], page = 1)
print(correct_url+"...")

driver = webdriver.Chrome(executable_path=CHROMEDRIVERPATH)
driver.implicitly_wait(5)
driver.get(correct_url)
time.sleep(5)
driver.find_element_by_xpath('//div[@class="primary-wrapper"]')
try:
    elem = WebDriverWait(driver, timeout=3).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="primary-wrapper"]'))
    )
    print("page is ready")
except Exception as e:
    print(e)

#elem = driver.find_element_by_xpath("//*")
#source_code = elem.get_attribute("outerHTML")
print(driver.page_source)
html = etree.HTML(driver.page_source)

title = html.xpath('//*//div[@class="company-list"]//span[@class="job-name"]//text()')
job_detail = html.xpath('//*//div[@class="company-list"]//span[@class="job-name"]//a//@href')
address = html.xpath('//*//div[@class="company-list"]//span[@class="job-area"]//text()')
comapny = html.xpath('//*//div[@class="company-list"]//div[@class="company-text"]//h3//text()')
comapny_info = html.xpath('//*//div[@class="company-list"]//div[@class="company-text"]//p//text()')
salary = html.xpath('//*//div[@class="company-list"]//div[@class="job-limit clearfix"]//sapn//text()')
work_experience = html.xpath('//*//div[@class="company-list"]//div[@class="job-limit clearfix"]//p//text()')

# %%
driver.close()



