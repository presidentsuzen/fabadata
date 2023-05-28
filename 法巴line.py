from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent,TextMessage,TextSendMessage , TemplateSendMessage , ButtonsTemplate , 
                                            PostbackTemplateAction , MessageTemplateAction , URITemplateAction , CarouselTemplate , 
                                           CarouselColumn , FlexSendMessage)
import re

app = Flask(__name__)

answer = []

line_bot_api = LineBotApi("")
handler = WebhookHandler("")

@app.route("/callback" , methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body:" + body)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent , message=TextMessage)
def handle_message(event):
    line=event.message.text
    if re.match(r'^(?!.*2)第\d{1,2}題[A-F]{2,6}$', line):
        count = 0
        for i in line:
            count += 1
            if count == 2:
                break
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="第{}題請重新作答！" .format(i)))
    elif re.match(r'^第\d{1,2}題[G-Z]{1,6}$', line):
        count = 0
        for i in line:
            count += 1
            if count == 2:
                break
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="第{}題請重新作答！" .format(i)))
    elif line=="開始風險測驗":
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="歡迎您進入法巴風險測驗！\n(作答方式 : 第1題A、第2題C、第3題BD(複選)以此類推)\n一、年齡\nA.未成年人(未滿18歲)\nB.18~35歲\nC.36~45歲\nD.46~55歲\nE.56~64歲\nF.65(含)以上"))
    elif line == "第1題A" or line == "第1題B" or line == "第1題C" or line == "第1題D" or line == "第1題E" or line == "第1題F":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="二、曾經使用過之投資理財工具種類(複選)？\nA.無\nB.與債券類型相關的基金（例如 : 貨幣型基金、債券型基金、債券型ETF） 或投資型保單連結前述標的或債券\nC.其他類型基金(排除B以外的基金，例如：股票型基金)或投資型保單類連結其他類型投資標的(排除B以外之投資標的.類型)\nD.股票\nE.外匯交易\nF.期貨或選擇權或結構型商品或其他衍生性金融商品"))
    elif re.match(r'^第2題[A-F]{1,6}$', line):
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="三、投資與債券類型相關商品之理財工具經驗？\nA.無經驗\nB.1年以下\nC.1年(含)~3年\nD.3年(含)~5年\nE.5年(含)以上"))
    elif re.match(r'^第2題[A-Z]{1,6}$', line):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="第2題請重新作答！"))
    elif line == "第3題A" or line == "第3題B" or line == "第3題C" or line == "第3題D" or line == "第3題E":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="四、投資與其他類型相關商品之理財工具經驗？\nA.無經驗\nB.1年以下\nC.1年(含)~3年\nD.3年(含)~5年\nE.5年(含)以上"))
    elif line == "第4題A" or line == "第4題B" or line == "第4題C" or line == "第4題D" or line == "第4題E":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="五、下列何者最符合您對投資理財工具的理解？\nA.對投資理財工具不熟悉，但有興趣進一步了解\nB.了解基本知識，如 : 股票與基金的分別\nC.了解基本知識以外，並明白分散投資及資產配置的重要性\nD.對投資理財工具及投資風險有進一步的認識，如 : 持有債券者可能因市場利率上升導致債券價格下降，使其遭受損失\nE.非常熟悉大部分投資理財工具(包括債券、股票、認股權證、選擇權及期貨等)，並明白影響這些金融產品的風險和表現的各項因素"))
    elif line == "第5題A" or line == "第5題B" or line == "第5題C" or line == "第5題D" or line == "第5題E":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="六、每年可用於購買投資理財工具之金額(NTD)？\nA.未滿50萬\nB.50萬以上~未滿100萬\nC.100萬以上~未滿300萬\nD.300萬以上"))
    elif line == "第6題A" or line == "第6題B" or line == "第6題C" or line == "第6題D":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="七、請問您的備用金(現金及存款)相當於您幾個月的生活開銷？\nA.無備用金或無須負擔生活開銷\nB.3個月以下\nC.超過3個月未達6個月\nD.超過6個月未達1年\nE.超過1年未達3年\nF.超過3年以上"))
    elif line == "第7題A" or line == "第7題B" or line == "第7題C" or line == "第7題D" or line == "第7題E" or line == "第7題F":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="八、請問您購買投資型保單連結外幣計價投資標的，每年可承受的價格損失(含匯率風險)？\nA.無法接受虧損\nB. -5%\nC. -10%\nD. -15%\nE. -20%"))
    elif line == "第8題A" or line == "第8題B" or line == "第8題C" or line == "第8題D" or line == "第8題E":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="九、請問您購買投資型保單所連結投資標的，在達到預計投資期間時(例如3年、5年)，可承受的價格損失(含匯率風險)？\nA.無法接受虧損\nB. -5%\nC. -10%\nD. -15%\nE. -20%"))
    elif line == "第9題A" or line == "第9題B" or line == "第9題C" or line == "第9題D" or line == "第9題E":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="十、您的投資回報期望？\nA.資產每年穩定成長\nB.資產短期快速成長\nC.避免資產損失"))
    elif line == "第10題A" or line == "第10題B" or line == "第10題C":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="十一、就長期投資而言，您期望的每年平均投資報酬率？\nA. 1%(含)~5%\nB. 5%(含)~10%\nC. 10%(含)~15%\nD. 15%(含)~20%"))
    elif line == "第11題A" or line == "第11題B" or line == "第11題C" or line == "第11題D":
        answer.append(line)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="十二、當投資發生虧損時或達到停損點時會採取的處理方式？\nA.持有至回本\nB.持有1年以上\nC.虧損已經6個月以上才考慮出售\nD.虧損未達6個月就賣掉\nE.先賣出一半\nF.立即賣出"))
    elif line == "第12題A" or line == "第12題B" or line == "第12題C" or line == "第12題D" or line == "第12題E" or line == "第12題F":
        answer.append(line)
        reply_message = '\n'.join(answer)
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="{}\n測驗結束，謝謝您參與本次測驗！" .format(reply_message)))
    elif re.match(r'^第一題[A-F]{1,6}$', line) or re.match(r'^第二題[A-F]{1,6}$', line) or re.match(r'^第三題[A-F]{1,6}$', line) or re.match(r'^第四題[A-F]{1,6}$', line) or re.match(r'^第五題[A-F]{1,6}$', line) or re.match(r'^第六題[A-F]{1,6}$', line) or re.match(r'^第七題[A-F]{1,6}$', line) or re.match(r'^第八題[A-F]{1,6}$', line) or re.match(r'^第九題[A-F]{1,6}$', line) or re.match(r'^第十題[A-F]{1,6}$', line) or re.match(r'^第十一題[A-F]{1,6}$', line) or re.match(r'^第十二題[A-F]{1,6}$', line):
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="請將國字數字改以阿拉伯數字重新回答此題！"))
    elif line =="作答方式":
        line_bot_api.reply_message(event.reply_token,TextSendMessage
                                   (text="作答方式 : 第1題A、第2題C、第3題BD(複選)以此類推，題號請以阿拉伯數字顯示！"))
    
    else:
        line_bot_api.reply_message(event.reply_token , 
                                   TextSendMessage(text='請輸入"開始風險測驗" 或 "作答方式"'))
        
if __name__ == "__main__":
    app.run()