from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random
app = Flask(__name__)
#line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
#line_handler = WebhookHandler('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi('Kn/qq4TXdnH1+2epazdNTeGeA5DopMr9kUlSffK+P+xyKQ7e0OHlAzY56y5FOrFqzS3Hytsn0REHFj03OfPffoCwbOntdhtkn+a/9VsnpZKbQqX2w79XhGAFbUZ+Hn6xL8qgNPmnKniHriMrnriQBwdB04t89/1O/w1cDnyilFU=')
line_handler = WebhookHandler('1a25e2c5a08c224d76f7053db6f9be9c')
@app.route('/')
def home():
    return 'Hello World'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def myG():
    myW=['你好','吃飽了嗎','天氣如何']
    return random.choice(myW)

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    getA=event.message.text        

    if getA =='0' :        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG())))      
        
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="輸入0"))

if __name__ == "__main__":
    app.run()