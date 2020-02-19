import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from lxml import etree
import threading


class DouyuBarrage():
    def __init__(self, url, roomId):
        self.option = Options()
        self.driver = self.set_headless()
        self.url = url
        self.roomId = roomId

    def set_headless(self):
        # 添加无界面参数
        self.option.add_argument('--headless')  # 浏览器不提供可视化页面.
        self.option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        self.option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        browser = webdriver.Chrome(options=self.option)
        return browser

    def getDanmu(self):
        self.driver.get(self.url + str(self.roomId))
        start = time.time()
        barrage_list = []
        while 1:
            time.sleep(1)
            try:
                for i in self.driver.find_elements_by_xpath('.//div[@class=" danmu-6e95c1"]/div/div'):
                    if i.text:
                        print(i.text)
                        barrage_list.append(i.text)
            except:
                continue
            stop = time.time()
            barrage_list = list(set(barrage_list))
            if len(barrage_list) >= 1000:
                for i in barrage_list:
                    if i:
                        self.save_barrage(i)
                barrage_list = []
            if stop - start >= 3600:
                if len(barrage_list) < 1000:
                    for i in barrage_list:
                        if i :
                            self.save_barrage(i)
                break
        self.driver_close()

    def driver_close(self):
        self.driver.close()

    def save_barrage(self, danmu):
        with open('danmu.txt', 'a+', encoding='utf-8')as f:
            f.write(danmu + '\n')


def get_roomid(url):
    response = requests.get(url)
    html = etree.HTML(response.text)
    roomid_list = html.xpath('//*[@id="listAll"]/div[2]/ul/li/div/a[1]/@href')
    return roomid_list


def main(type_url):
    url = 'https://www.douyu.com'
    roomid_list = get_roomid(url + type_url)
    for roomid in roomid_list[0:5]:
        bar = DouyuBarrage(url, roomid)
        t = threading.Thread(target=bar.getDanmu)
        t.start()


if __name__ == '__main__':
    type_url = '/g_LOL'
    main(type_url)
