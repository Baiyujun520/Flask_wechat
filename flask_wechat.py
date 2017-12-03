# -*- coding:utf-8 -*-

from flask import Flask, request, make_response
import hashlib
import xmltodict
import time


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/wechat8000', methods=['GET', 'POST'])
def wechat():
    # 设置token
    token = 'baiyujun'
    # 获取参数
    data = request.args
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')

    # 对参数进行排序
    temp = [timestamp, nonce, token]
    temp.sort()
    temp = "".join(temp)
    sig = hashlib.sha1(temp).hexdigest()
    # 进行对比
    if signature == sig:
        # 当发来的是get请求的时候则返回echostr
        if request.method == 'GET':
            return echostr

        # 以下的是POST请求发来的
        xml_data = request.data
        # 将xml转换为dict
        xml_dict = xmltodict.parse(xml_data)['xml']
        msg_type = xml_dict['MsgType']

        if "text" == msg_type:
            res_dict = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": xml_dict.get("Content"),
            }
            print xml_dict.get("Content")

        elif "voice" == msg_type:
            # 接受语音消息
            res_dict = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": xml_dict.get("Recognition"),
            }

            print xml_dict.get('Recognition')
        else:
            res_dict = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": "就是这么骚",
            }

        res_dict = {'xml': res_dict}
        return xmltodict.unparse(res_dict)
    else:
        return 'error', 403


if __name__ == '__main__':
    app.run(port=8000)

