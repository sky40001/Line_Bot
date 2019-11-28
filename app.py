# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# 填入你的 message api 資訊
line_bot_api = LineBotApi('eo75reS/9r7FTW7/p/jseQiuUJV27QHoot3BVsnM9Y+l4z8hJtRtYBLYr8yQtI9xVjEnUw/lhnpYUVRU1ivLWQD7a6FEB8hd4x8YGyPclgRp0eStWLwYcQqQg11hZ+oFlqC2o4BtHj+Au/bNpFUtJQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('21f62ce5b8b8e90cd9c82f6216a68e9a')

# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("https://line-bot0001.herokuapp.com/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])