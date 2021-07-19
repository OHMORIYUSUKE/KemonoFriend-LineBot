import os
import sys
from pathlib import Path

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, FollowEvent, UnfollowEvent,
    StickerMessage,
)

import reply_message_create

app = Flask(__name__)

# デプロイ時はコメントアウトを取り消す
# 環境変数からchannel_secret・channel_access_tokenを取得
channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']


# # -----デプロイ時は消す-----
# import json
#
# json_open = open('key.json', 'r')
# json_load = json.load(json_open)
# channel_secret = json_load['LINE_CHANNEL_SECRET']
# channel_access_token = json_load['LINE_CHANNEL_ACCESS_TOKEN']
# print(channel_access_token)
# print(channel_secret)
# # -----デプロイ時は消すEND-----

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_secret)
handler = WebhookHandler(channel_access_token)


@app.route("/")
def hello_world():
    return "hello world!"

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

@handler.add(FollowEvent)
def handle_follow(event):
    # 画像の送信
    image_url = "https://kemonofriendlinebot.herokuapp.com/static/images/ReplyImage/sabal.png"
    text_message1 = "あたらしいフレンズだ！"
    text_message2 = "私はサーバルだよ！\nよろしくね！"

    line_bot_api.reply_message(event.reply_token,
                               [TextSendMessage(text=text_message1),
                                ImageSendMessage(preview_image_url=image_url,
                                                 original_content_url=image_url),
                                TextSendMessage(text=text_message2)])

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print("Got Unfollow event:" + event.source.user_id)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = reply_message_create.main(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

@handler.add(MessageEvent,message=StickerMessage)
def handle_sticker(event):
    print("スタンプ")
    # 画像の送信
    image_url = "https://kemonofriendlinebot.herokuapp.com/static/images/ReplyImage/sabal_naki.png"
    text_message = "スタンプ分からないよー！"
    line_bot_api.reply_message(event.reply_token,
                               [ImageSendMessage(preview_image_url=image_url,original_content_url=image_url),
                                TextSendMessage(text=text_message)])

# @handler.add(MessageEvent,message=ImageMessage)
# def handle_image(event):
#     # 画像の送信
#     image_url = "https://pbs.twimg.com/media/DKuRcKqUEAACAID.png"
#     text_message = "画像分からないよー！"
#     line_bot_api.reply_message(event.reply_token,
#                                [ImageSendMessage(preview_image_url=image_url,original_content_url=image_url),
#                                 TextSendMessage(text=text_message)])

# ----------------------------------------------------------
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id

    try:
        # message_idから画像のバイナリデータを取得
        message_content = line_bot_api.get_message_content(message_id)

        message_content = line_bot_api.get_message_content(message_id)

        with open('static/images/ImageMessage', 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

        print("id : "+message_id)
        main_image_path = f"static/images/ImageMessage/{message_id}.jpg"
        preview_image_path = f"static/images/ImageMessage/{message_id}.jpg"

        # 画像の送信
        image_message = ImageSendMessage(
            original_content_url=f"https://kemonofriendlinebot.herokuapp.com/{main_image_path}",
            preview_image_url=f"https://kemonofriendlinebot.herokuapp.com/{preview_image_path}",
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    except:
        import traceback
        traceback.print_exc()
# ----------------------------------------------------------

if __name__ == "__main__":
    app.run()
