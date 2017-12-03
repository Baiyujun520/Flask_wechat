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

        elif "event" == msg_type:
            if "subscribe" == xml_dict.get('Event'):
                # 代表当前用户关注了
                res_dict = {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "感谢你的关注",
                }
                if xml_dict.get("EventKey"):
                    res_dict["Content"] += ";场景值是："
                    res_dict["Content"] += xml_dict.get("EventKey")

            elif "SCAN" == xml_dict.get("Event"):
                # 代表当前用户已经关注，扫描二维码
                res_dict = {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "感谢你的扫描"
                }

                if xml_dict.get("EventKey"):
                    res_dict["Content"] += "；场景值是："
                    res_dict["Content"] += xml_dict.get("EventKey")

            else:
                # 可能取消了关注
                print '取消了关注'
                res_dict = None

        else:
            res_dict = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": "就是这么骚",
            }
        if res_dict:
            res_dict = {'xml': res_dict}
            return xmltodict.unparse(res_dict)
        else:
            return ""
    else:
        return 'error', 403


if __name__ == '__main__':
    app.run(port=8000)

