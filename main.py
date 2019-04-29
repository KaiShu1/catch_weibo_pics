from requests import get, post
from json import loads
from time import sleep
from os import mkdir
from urllib.parse import quote

'''
Todo1: 更新主页和搜索页 多页爬取
Todo2: 抓取gif图

Done: Todo1、Todo2，可以通过设置page_count来选择多页爬取主页，对于搜索页面需要多设置一个参数 page=page_count 即可，
      且可以抓取gif图,新增获取搜索页面视频资源

Todo3: 自动获取用户的 containerid
'''


class Spider:
    def __init__(self, content, page_count=1):
        """
        :param content: contain the thing that you want to search
        :param count: catch home page numbers
        """
        self.content = content
        self.page_count = page_count
        original_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103" \
                       "type%3D3%26q%3D" + quote(self.content) + "&page_type=searchall"
        self.home_page_url = self.get_home_page_url(original_url)
        self.since_id = ''

    def hm_catch_pics(self):
        """
        catch number of home page pics by setting self.page_count
        :return: 1
        """

        dir_name = self.content + 'pics_h'
        try:
            mkdir(dir_name)
        except FileExistsError:
            print('file existed')
        for page_count in range(self.page_count):
            print("page:" + str(page_count) + "-" * 40)
            base_url = "https://m.weibo.cn/api/container/getIndex"
            r = get(base_url, params={'is_hot[]': '1',
                                      'jumpfrom': "weibocom",
                                      'type': 'uid',
                                      'value': self.home_page_url[21:31],
                                      'containerid': 1076035404464551,
                                      'since_id': self.since_id,
                                      })
            data = loads(r.text)
            self.since_id = str(data["data"]["cardlistInfo"]["since_id"])
            # 每个json数据中有十个card
            for card_num in range(10):
                try:
                    pic_num = 1
                    for single_pic_url in data["data"]["cards"][card_num]["mblog"]["pics"]:
                        print(single_pic_url['large']['url'])
                        publish_time = data['data']['cards'][card_num]['mblog']['created_at'
                                       ].replace(':', '').replace(' ', '')[:6]
                        print(publish_time)
                        pic = get(single_pic_url['large']['url']).content
                        if single_pic_url['large']['url'][-1:-4] == 'gif':
                            with open("./%s/%s%s%sat %s.gif" % (
                                    dir_name, page_count, card_num, pic_num, publish_time), "wb") as f:
                                f.write(pic)
                        else:
                            with open("./%s/%s%s%sat %s.jpg" % (
                                    dir_name, page_count, card_num, pic_num, publish_time), "wb") as f:
                                f.write(pic)
                        pic_num += 1
                except KeyError:
                    continue
                sleep(1)
        return 1

    def sp_catch_pics(self):
        dir_name = self.content + 'pics_s'
        try:
            mkdir(dir_name)
        except FileExistsError:
            print('file existed')

        for page_count in range(1, self.page_count + 1):
            url = "https://m.weibo.cn/api/container/getIndex?containerid=100103" \
                  "type%3D1%26q%3D" + quote(self.content) + "&page_type=searchall"
            if page_count:
                url += "&page=%s" % page_count
            print(url)
            r = get(url)
            data = loads(r.text)

            # 每个json数据中最后一个cards存有所需数据。
            for card_num in range(len(data['data']['cards'][-1]['card_group'])):
                try:
                    pic_num = 0
                    for single_pic_url in data["data"]["cards"][-1]['card_group'][card_num]["mblog"]["pics"]:
                        print(single_pic_url['large']['url'])
                        pic = get(single_pic_url['large']['url']).content
                        if single_pic_url['large']['url'][-3:] == 'gif':
                            with open("./%s/%s%s%s.gif" % (dir_name, page_count, card_num, pic_num), "wb") as f:
                                f.write(pic)
                        else:
                            with open("./%s/%s%s%s.jpg" % (dir_name, page_count, card_num, pic_num), "wb") as f:
                                f.write(pic)
                        pic_num += 1
                        sleep(0.5)
                except KeyError:
                    continue

    def sp_catch_media(self):
        dir_name = self.content + '_video_s'
        try:
            mkdir(dir_name)
        except FileExistsError:
            print('file existed')
        for page_count in range(1, self.page_count + 1):
            url = "https://m.weibo.cn/api/container/getIndex?containerid=100103" \
                  "type%3D1%26q%3D" + quote(self.content) + "&page_type=searchall"
            if page_count:
                url += "&page=%s" % page_count
            r = get(url)
            data = loads(r.text)
            for card_num in range(len(data['data']['cards'][-1]['card_group'])):
                try:
                    media_info = data["data"]["cards"][-1]['card_group'][card_num]["mblog"]["page_info"]["media_info"]
                except KeyError:
                    continue
                if media_info['mp4_720p_mp4']:
                    media_url = media_info['mp4_720p_mp4']
                elif media_info['mp4_hd_url']:
                    media_url = media_info['mp4_hd_url']
                else:
                    media_url = media_info['mp4_sd_url']
                with open("./%s/%s%s.mp4" % (dir_name, page_count, card_num), "wb") as f:
                    f.write(get(media_url).content)

    def get_home_page_url(self, api_url):
        data = loads(get(api_url).text)
        self.home_page_url = data['data']['cards'][1]['card_group'][0]['user']['profile_url']
        return self.home_page_url


if __name__ == '__main__':
    # 初始手机端主页xhr文件地址
    s = Spider("韩国BJ", 2)
