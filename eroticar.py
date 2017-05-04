#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-5-4 下午6:04
# @Author  : Sylor
# @File    : eroticar.py
# @Software: PyCharm
import os
import requests
from pyquery import PyQuery as pq
import re
from multiprocessing import Pool

def index_html(url):  #获取图片首页的地址
    try:
        doc = pq(url)
        items = doc('.thumbs').items()  #需要items（）才能进行循环。
        for links in items:            #获取每个thumbs里的a标签
            for img in links('a').items():  #获取每个a里的href内容
                all_imgs = img.attr.href
                all_urls = re.sub('.*?url=','',str(all_imgs))  #替换掉href的跳转字符串
                img_urls = re.sub('&p=87','',all_urls)
                parse_html(img_urls)
    except:
        return None

def parse_html(img_urls):  #获取图片详情页的地址
    try:
        doc = pq(img_urls)
        img_name = doc('.crumbles').find('span').text()
        print('创建文件夹',img_name)
        mkdir(img_name)
        thumb_box = doc('.thumb_box').items()
        for img_links in thumb_box:
            for allimgs in img_links('a').items():
                allimg = img_urls + allimgs.attr.href
                img_jpg(allimg,img_urls,img_name)
    except:
        return None

def img_jpg(allimg,img_urls,img_name): #获取图片地址，并存取图片
    doc = pq(allimg)
    img_path = img_urls + doc('.modelbox-thumbs').find('img').attr.src
    path_name =requests.get(img_path)
    img_path_name = img_path[-7:-4].replace("/",'_')
    print('开始保存文件')
    with open(img_path_name + '.jpg','wb') as f:
        f.write(path_name.content)
        f.close()
        print('保存完毕')

def mkdir(img_name):
    os.makedirs(os.path.join('/opt/erot',img_name))
    os.chdir(os.path.join('/opt/erot/'+img_name))


def main(url):
    index_html(url)



if __name__ == '__main__':
    url = 'http://www.eroticartbeauty.com/'
    main(url)
    pool = Pool(10)
    pool.apply_async(main,index_html,parse_html,img_jpg)
    pool.close()
    pool.join()
