#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import urllib
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    headers = {'User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.__time_sleep = t

    def url_open(self, url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0')
        response = urllib.request.urlopen(req)
        html = response.read()
        return html

    def find_imgs(self, url):
        html = self.url_open(url).decode('utf-8')
        # 匹配img src字段，非贪婪方式图片链接
        reg = '<img src=".+?"'
        imgre = re.compile(reg)
        # 匹配html,输出list
        img_locals = re.findall(imgre, html)
        # 解析img地址
        word_cut = '".+?"'
        img_addrs = []
        index = 0
        for line in img_locals:
            line = re.findall(word_cut, line, flags=0)
            img_addrs.insert(index, line[0][1:-1])
            index += 1
        # print(img_addrs)
        return img_addrs

    def get_imgurlname(self, imaPath):
        match = ''
        if imaPath.__contains__('jpg'):
            match = '.*\.jpg'
        elif imaPath.__contains__('png'):
            match = '.*\.png'
        else:
            print("can not match any")
        res = re.findall(match, imaPath)
        a = re.split('/', res[0])
        newname = a[-1]
        # print(newname)
        return newname

    def save_imgs(self, folder, img_addrs):
        cnt = 0
        imageName = ''
        # print(img_addrs)
        for imaPath in img_addrs:
            try:
                time.sleep(self.__time_sleep)
                # 解析url中的imagename
                imageName = self.get_imgurlname(imaPath)
                # 下载image
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')
                ]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(imaPath, folder + '%s' % imageName)
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', imaPath)
                continue
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", imaPath)
                continue
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", imaPath)
                continue
            else:
                cnt += 1
                if cnt >= 100:
                    return
            finally:
                print("loading " + imageName + "... success!")
        print("load finish")

    def get_webimage(self, folder, url):
        # 存在项目resources内
        if not os.path.exists("./resources"):
            os.mkdir("./resources")

        img_addrs = self.find_imgs(url)
        self.save_imgs(folder, img_addrs)

    def grab_urlforfile(self):
        # 文件位置
        url = ''
        file = ''
        try:
            path = os.getcwd() + '\\AA\\a.md'
            file = open(path, encoding="utf-8")
            # 匹配url
            match = 'https:.*png'
            url = re.findall(match, file.read())
        except Exception as e:
            print(e)
        finally:
            file.close()
        return url

    def start(self):
        """
        爬虫入口
        """
        mode = input("Mode 1:md文件下载\nMode 2:网页下载\nMode 3:退出\n")
        folder = os.getcwd() + "\\resources\\"
        if mode == '1':
            urls = self.grab_urlforfile()
            # 在文件中找到图片位置
            self.save_imgs(folder, urls)
        elif mode == '2':
            #  直接从网页下载图片
            # weburl = 'https://draveness.me/etcd-introduction'
            weburl = input("请输入网页地址")
            self.get_webimage(folder, weburl)
        elif mode == '3':
            return

if __name__ == '__main__':
    crawler = Crawler(0.05)
    crawler.start()
