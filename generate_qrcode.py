# -*- coding:utf-8 -*-
# 生成二维码：1.获取access_token, 2.通过access_token获取ticket,3. 通过ticket换取二维码
import time
import json
import urllib2

from flask import Flask

WECHAT_APPID = "wxb0b9562ee6150a1b"
WECHAT_APP_SECRET = "77ca0a7a644ef70d0386e94ad97e7751"


class AccessToken(object):

    __access_token = {
        "access_token": "",
        "update_time": time.time(),
        "expires_in": 7200
    }

    @classmethod
    def get_access_token(cls):

        # 判断有没有access_token 判断access_token是否过期
        # if 没有access_token or 已过期
        if not cls.__access_token.get("access_token") \
                or (time.time() - cls.__access_token.get("update_time") > cls.__access_token.get("expires_in")):
            # 获取access_token
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (WECHAT_APPID, WECHAT_APP_SECRET)
            # 使用urllib2去发送请求
            response = urllib2.urlopen(url)
            # 读取到响应中数据
            data = response.read()
            data_dict = json.loads(data)
            # 将相关信息保存到 __access_token
            if "errcode" in data_dict:
                # 请求错误/参数有问题
                raise Exception("get accesstoken failed")

            # 设置数据
            cls.__access_token["access_token"] = data_dict.get("access_token")
            cls.__access_token["expires_in"] = data_dict.get("expires_in")
            cls.__access_token["update_time"] = time.time()

        return cls.__access_token.get('access_token')

app = Flask(__name__)


@app.route('/get_qrcode/<int:scene_id>')
def index(scene_id):
    access_token = AccessToken.get_access_token()
    # 定义url和参数
    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token
    params = {
        "expire_seconds": 604800,
        "action_name": "QR_SCENE",
        "action_info": {"scene": {"scene_id": scene_id}}
    }

    # 将字典装成JSON字符串
    params = json.dumps(params)
    # 发起请求获取响应
    response = urllib2.urlopen(url, params)
    # 获取到响应体
    resp_data = response.read()
    # 转成字典
    resp_dict = json.loads(resp_data)
    # 获取ticket
    ticket = resp_dict.get("ticket")

    return '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s">' % ticket

if __name__ == '__main__':
    app.run(debug=True)