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

# 環境変数からLINE Access TokenとChannel Secretを取得
# あるいは直接文字列として代入しますが、セキュリティのためハードコーディングは推奨されません
LINE_CHANNEL_ACCESS_TOKEN = 'f8PW1WzvJRsYXBSiqT6l6SLjCULtUK4RTdXSS3hBQATJGGqiFW67efgF6PFadg089X1wdiLcYF6F6+KovMFcp2/ZfUvF3HW9rruLcrupaVTN1LLVnmBLogBJQwB8u+cR209uUh/p4LXY84gfx+I9sAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '21e377b5d419c47446467c0c67ebcca6'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # requestのX-Line-Signatureヘッダからsignatureを取得
    signature = request.headers['X-Line-Signature']

    # requestのbodyをテキストとして取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # signatureの検証とhandle
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーからのメッセージを取得
    text = event.message.text
    
    # 取得したメッセージをユーザーに返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text)  # ユーザーのメッセージをそのまま返信
    )


if __name__ == "__main__":
    # ngrokなどを使用している場合は、port=5000を設定
    app.run(port=5000)
