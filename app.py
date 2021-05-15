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

YOUR_CHANNEL_ACCESS_TOKEN = 'Kqfp8pS6PwIwsf5H2uxHGx2thkkkoQfomF1KKSodbptecS3DNQJ5Hiq9A1w1ZQStQZbE6eElttqqjhIPCdiuNUGoeLf2v4Gf25qhXSqcxNx9VeTzGe/bFwqdzMZxJDtSGSkAJz+JCUVFvnPIvs7s0AdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '9dc532dcffbb965de17cf5ef2f9e8bf1'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

 
import os

@app.route("/")
def hello_world():
    return "hello Imanyu"

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    port = os.getenv('PORT')
    app.run(host='0.0.0.0', port=port)