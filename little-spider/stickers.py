import os
import random
import time

import requests
from bs4 import BeautifulSoup
from common import headers


class App:
    base_url = 'https://www.mibimibi.com/sticker_sets/'
    base_dir = 'stickers'

    def __init__(self):
        self.req = requests
        self.bs = BeautifulSoup
        create_dir(self.base_dir)

    def download_page(self, set_id) -> str:
        res = self.req.get(self.base_url + set_id, headers={'user-agent': random.choice(headers)})
        res.encoding = 'utf-8'
        return res.text

    def get_pic(self, html):
        soup = self.bs(html, 'html.parser')
        set_name = soup.find('h1', class_='mt-3').text
        escaped_set_name = str(set_name.split('@')[0]).replace(' ', '')
        create_dir('stickers/{}'.format(escaped_set_name))
        img_items = soup.find_all('sticker-item')
        item_size = len(img_items)
        for i, item in enumerate(img_items):
            img_link = item.get('sticker-image-url')
            res = self.req.get(img_link, headers={'user-agent': random.choice(headers)})
            print('{}这个集合中共{}个文件, 正在下载第{}个。。。'.format(escaped_set_name, item_size, i + 1))
            with open('stickers/{}/{}'.format(escaped_set_name, img_link.split('/')[-1]), 'wb') as f:
                f.write(res.content)
                time.sleep(0.1)


def create_dir(dir_name) -> None:
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def main():
    app = App()
    # set_id = input('please input the set_id you want to download: ')
    set_ids = [360, 1001, 509]
    for id in set_ids:
        app.get_pic(app.download_page(str(id)))


if __name__ == '__main__':
    main()
