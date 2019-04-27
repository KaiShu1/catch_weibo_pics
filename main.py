import requests
import json


class Spider:
    def __init__(self, origin_url):
        self.url = origin_url
        self.r = requests.get(self.url).text
        self.data = json.loads(self.r)

    def catch_since_id(self):
        since_id = self.data["data"]["cardlistInfo"]["since_id"]
        return since_id

    def catch_pic(self):
        for i in range(10):
            try:
                single_pic_url = self.data["data"]["cards"][i]["mblog"]["original_pic"]
            except KeyError:
                continue
            pic = requests.get(single_pic_url).content
            with open("./imgs/%s.jpg"%i, "wb") as f:
                f.write(pic)


if __name__ == '__main__':
    url = "https://m.weibo.cn/api/container/getIndex?uid=5404464551&luicode=10000011&lfid=100103type%3D3%26q%3D%E6\
    %9D%A8%E6%99%A8%E6%99%A8%26t%3D0&type=uid&value=5404464551&containerid=1076035404464551"
    s = Spider(url)
    print(s.catch_since_id())
