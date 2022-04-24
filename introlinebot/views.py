from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
    
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .intro import academic_intro, tech_intro, reason_intro, open_source_intro, side_project_intro, try_again

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
    
    
@csrf_exempt
def introduce(request):
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
    
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
    
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == '1':
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=academic_intro)
                    )
                elif event.message.text == '2':
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=reason_intro)
                    )
                elif event.message.text == '3':
                    line_bot_api.reply_message( 
                        event.reply_token,
                        TextSendMessage(text=open_source_intro)
                    )
                elif event.message.text == '4':
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=side_project_intro)
                    )
                elif event.message.text == '5':
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=tech_intro)
                    )
                else:
                    line_bot_api.reply_message( 
                        event.reply_token,
                        TextSendMessage(text=try_again)
                    ) 
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# def callback(request):
    
#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')
    
#         try:
#             events = parser.parse(body, signature)  # 傳入的事件
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()
    
#         for event in events:
#             if isinstance(event, MessageEvent):  # 如果有訊息事件
#                 line_bot_api.reply_message(  # 回復傳入的訊息文字
#                     event.reply_token,
#                     TextSendMessage(text=event.message.text)
#                 )
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()
