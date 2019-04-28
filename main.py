from requests import get
from json import loads
from time import sleep
from os import mkdir
from urllib.parse import quote

'''
Todo1: 更新主页和搜索页 多页爬取
Todo2: 抓取gif图
'''


class Spider:
    def __init__(self, content, count=0):
        """
        :param content: contain the thing that you want to search
        :param count: don't need, just for count
        """
        self.content = content
        self.count = count

    def home(self):
        dir_name = self.content + 'pics_h'
        mkdir(dir_name)
        url = "https://m.weibo.cn/api/container/getIndex?uid=1831216671&luicode=10000011&lfid=100103" \
              "type%3D1%26q%3D" + quote(self.content) + "&type=uid&value=1831216671&containerid=1076031831216671"
        r = get(url).text
        data = loads(r)
        since_id = str(data["data"]["cardlistInfo"]["since_id"])
        print(since_id)

        # 每个json数据中有十个card
        for card_num in range(10):
            try:
                pic_num = 1
                for single_pic_url in data["data"]["cards"][card_num]["mblog"]["pics"]:
                    print(single_pic_url['large']['url'])
                    pic = get(single_pic_url['large']['url']).content
                    with open("./%s/%s%s.jpg" % (dir_name, card_num, pic_num), "wb") as f:
                        f.write(pic)
                    pic_num += 1
            except KeyError:
                continue

    def search(self):
        dir_name = self.content + 'pics_s'
        mkdir(dir_name)
        url = "https://m.weibo.cn/api/container/getIndex?containerid=100103" \
              "type%3D1%26q%3D" + quote(self.content) + "&page_type=searchall"
        r = get(url).text
        data = loads(r)

        # 每个json数据由五个card, 最后一项中存有所需数据。
        for card_num in range(9):
            try:
                pic_num = 0
                for single_pic_url in data["data"]["cards"][-1]['card_group'][card_num]["mblog"]["pics"]:
                    print(single_pic_url['large']['url'])
                    pic = get(single_pic_url['large']['url']).content
                    with open("./%s/%s%s.jpg" % (dir_name, card_num, pic_num), "wb") as f:
                        f.write(pic)
                    pic_num += 1
                    sleep(1)
            except KeyError:
                continue


if __name__ == '__main__':
    # 初始手机端主页xhr文件地址
    s = Spider()
    s.search()
