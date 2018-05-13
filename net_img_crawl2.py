#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网络图片下载
"""

from common import crawlcm
from common import loadcfgcm
import requests   #导入requests模块
from bs4 import BeautifulSoup #导入BeautifulSoup模块
from selenium import webdriver #导入selenium
import os #导入os模块
from selenium.webdriver.chrome.options import Options


# 缺省配置及说明
# 链接模式：SELECT 从选定页面开始，根据下一页按钮，循环抓取
# 链接模式：FORMAT 按照格式，根据格式生成下一页链接，循环抓取
default_config = """
{
    "page_url": "http://www.somesite.to.crawl/xxxx",
    "local_path": "./temp"
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_img_crawl2.json", default_config)

def get_headless_chrome():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('/opt/chrome/chromedriver', chrome_options=chrome_options)
    return driver

class MMPic():
    def __init__(self):  #类的初始化
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}  # 给请求指定一个请求头来模拟chrome浏览器
        self.web_url = cfg["page_url"]  #要爬虫的网址
        self.folder_path = cfg['local_path']  # 设置图片要存放的文件目录

    def request(self, url): #向url发送get请求，返回Response对象
        r = requests.get(url)
        return r

    def save_img(self, url, file_name):
        print('开始请求图片地址')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, '图片保存成功')
        f.close()

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names

    def mkdir(self, path):  #创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫', path, '的文件夹')
            os.makedirs(path)
            print('创建成功')
            return True
        else:
            print(path, '文件夹已经存在')
            return  False

    def spider_start(self):  #爬虫开始
        print('开始爬起来！！！！')
        #driver = webdriver.PhantomJS('/opt/phantomjs/phantomjs')
        driver = get_headless_chrome()

        driver.get(self.web_url)
        html = driver.page_source
        print(html)
        all_a = BeautifulSoup(html, 'lxml').find_all(class_='title')
        print(all_a)
        # self.mkdir(self.folder_path)
        # print('开始切换文件夹')
        # os.chdir(self.folder_path)
        for a in all_a:
            a_url = a.find('a')['href']
            print('爬虫网页', a_url)
            self.spider_page(a_url)

    def spider_page(self, page_url):
        # print('爬虫每一个网页')
        driver_page = get_headless_chrome()
        driver_page.get(page_url)
        html_page = driver_page.page_source
        html_parse = BeautifulSoup(html_page, 'lxml')
        page_title = html_parse.find(class_='article').h2.string
        page_path  = self.folder_path + '/' + page_title
        self.mkdir(page_path)
        os.chdir(page_path)
        file_names = self.get_files(page_path)  #获取文件夹中所有的文件名，类型为list
        page_total = int(html_parse.find(id='opic').previous_sibling.string)
        print(page_total)
        for i in range(page_total):
            driver_pic_index = get_headless_chrome()
            driver_pic_index.get(page_url + '/' + str(i+1))
            pic_index = driver_pic_index.page_source
            pic_src = BeautifulSoup(pic_index, 'lxml').find(id='content').img.attrs['src']
            print(pic_src)
            pic_name = pic_src[pic_src.rfind('/')+1:]  #根据pic_src获取图片的名称
            if pic_src in file_names:
                print('图片已经存在，不在重复下载')
            else:
                self.save_img(pic_src, pic_name)


mm_pic = MMPic()   #创建类的实例
mm_pic.spider_start() #执行类的方法