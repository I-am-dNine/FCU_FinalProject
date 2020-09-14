# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 01:00:17 2018

@author: yeh
"""


from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import mongodb
import re
import schedule
import urllib.parse
import datetime
from bs4 import BeautifulSoup
import time
import search
import order
import tech

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('0RESBNWCfsvSRF4MMUJnu5uTKCeS3MFN05XAoDkNUmLh/JwfjZZqV1hisMl8GsR6wG175trlcY/74iN0sJ1A98hLE1v2takoD7UNfNY8Fu102jM7C6agGKWOQNAqYZzKK2sEh+eZtx86OO4bhxh6kAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('54cd451ffb3d2728924e284de5f836bd')

line_bot_api.push_message('Ud5ccf6452c79b7add21fcb8a008b0717', TextSendMessage(text='開始'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ### 抓到顧客的資料 ###
    #message = TextSendMessage(text="你說的是不是"+event.message.text)
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id #使用者ID
    usespeak=str(event.message.text) #使用者講的話
    if re.match('[0-9]{4}[<>][0-9]',usespeak): # 先判斷是否是使用者要用來存股票的
        mongodb.write_user_stock_fountion(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        
        return 0 
    elif re.match('刪除[0-9]{4}',usespeak): # 刪除存在資料庫裡面的股票
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0
    elif re.match('[0-9]{4}[.][TW]',usespeak):
        answer = search.getPrice(usespeak)
        #line_bot_api.reply_message(event.reply_token, search.getPrice(usespeak))
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('取消委託',usespeak):#取消委託
        answer = order.cancelOrder(usespeak[4:])
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('[B|S]',usespeak):
        answer = order.putOrder(usespeak[0], usespeak[2:9], usespeak[10:13], usespeak[14:18], usespeak[19:])    
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('查詢委託',usespeak):#查詢委託
        answer = search.getOrder()
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('庫存',usespeak):#查詢庫存
        answer = search.getInStock()
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif usespeak=='成交':#查詢成交
        answer = search.getDeal()
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('熱門股',usespeak):#查詢熱門股
        name ='vol'
        answer = tech.url_re(name)
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('漲幅排行',usespeak):#查詢單日漲幅排行
        name ='up'
        answer = tech.url_re(name)
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('跌幅排行',usespeak):#查詢單日跌幅排行
        name ='down'
        answer = tech.url_re(name)
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif re.match('當沖指標排行',usespeak):#查詢當沖指標排行
        name ='pdis'
        answer = tech.url_re(name)
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif usespeak =='成交價排行':#查詢成交價排行
        name ='pri'
        answer = tech.url_re(name)
        line_bot_api.push_message(uid, TextSendMessage(answer))
    elif usespeak =='成交值排行':#查詢成交值排行
        name ='amt'
        answer = tech.url_re(name)
        line_bot_api.push_message(uid, TextSendMessage(answer))      
    elif event.message.text == "台股網站":
        line_bot_api.reply_message(event.reply_token, imagemap_message())
    elif event.message.text == "查詢功能":
        line_bot_api.reply_message(event.reply_token, buttons_template())

#@imagemap.add(MessageEvent, message=TextMessage)
def imagemap_message():
    message = ImagemapSendMessage(
            base_url='https://i.imgur.com/R6gvyxC.png',
            alt_text='台股網站',
            base_size=BaseSize(height=2000, width=2000),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.cnyes.com/twstock/',
                    area=ImagemapArea(
                        x=0, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://tw.stock.yahoo.com/',
                    area=ImagemapArea(
                        x=1000, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.wantgoo.com/',
                    area=ImagemapArea(
                        x=0, y=1000, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.twse.com.tw/zh/',
                    area=ImagemapArea(
                        x=1000, y=1000, width=1000, height=1000
                    )
                )
            ]
    )
    return message

def buttons_template(): #尚未更正: 其他使用者看不到請輸入..
    buttons = TemplateSendMessage(
            alt_text='查詢功能',
            template=ButtonsTemplate(
                    title='請選擇查詢項目',
                    text='股票助理提供以下查詢功能',
                thumbnail_image_url='https://i.imgur.com/R6gvyxC.png',
                actions=[
                     MessageTemplateAction(
                        label='委託紀錄',
                        text='請輸入TC'
                    ),
                     MessageTemplateAction(
                        label='庫存紀錄',
                        text='請輸入SK'
                    ),
                     MessageTemplateAction(
                        label='成交紀錄',
                        text='請輸入DL'
                    ),
                    MessageTemplateAction(
                        label='股價查詢',
                        text='請輸入股票代碼 ex. 2330.TW'
                    )
                ]
            )
    ) 
    return buttons

        


if __name__ == '__main__':
    app.run(debug=True)