from flask import Flask, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from linebot.models import MessageAction, TemplateSendMessage, ConfirmTemplate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
import pandas as pd 
import warnings
from linebot import LineBotSdkDeprecatedIn30

app_line = Flask(__name__)

@app_line.route("/", methods = ["POST"])  

def linebot():
    global mount_df, msg, line_bot_api, token, access_token
    body = request.get_data(as_text = True)                    
    try:
        json_data = json.loads(body)                         
        print(json_data)
        access_token = "CuVcNmfbWzuJshyHnZwOfNO84W0xiNOsm1Xq8aBVL5HMNnbOr7hmNDDk+xQ2iXCY3eBElLNf6CpxKXHVyOtsRYIdQqUMLFLSDSZtmNBgjX4g3sOUHYGb+6YflB9tFjYgzzd9U4Jo/dGRO7Gu39QIHwdB04t89/1O/w1cDnyilFU="
        secret = "d4c4140b7dd0d80cbeaa74642ad81922"
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)                     
        signature = request.headers["X-Line-Signature"]      
        handler.handle(body, signature)                      
        token = json_data["events"][0]["replyToken"]         
        print(token)
        type = json_data["events"][0]["message"]["type"]     
        if type == "text":
            msg = json_data["events"][0]["message"]["text"]  
            print(msg)                                       
            if msg == "好呀<3":
                reply = "希望篩選的結果您會滿意!!!\n若您想了解特定步道資訊\n請輸入步道名稱喔!!"
                print(reply)
                line_bot_api.reply_message(token,TextSendMessage(reply))
            elif msg == "不謝了QQ":
                reply = "好吧您有特別想了解的步道嗎?"
                print(reply)
                line_bot_api.reply_message(token,TextSendMessage(reply))
                line_bot_api = LineBotApi("CuVcNmfbWzuJshyHnZwOfNO84W0xiNOsm1Xq8aBVL5HMNnbOr7hmNDDk+xQ2iXCY3eBElLNf6CpxKXHVyOtsRYIdQqUMLFLSDSZtmNBgjX4g3sOUHYGb+6YflB9tFjYgzzd9U4Jo/dGRO7Gu39QIHwdB04t89/1O/w1cDnyilFU=")  
                line_bot_api.push_message("U6a3ba421ceaeff0c96b0d7fbb53c09d1", TemplateSendMessage(
                    alt_text = "特定步道資訊查詢",
                    template = ConfirmTemplate(
                            text = "是否想了解特定步道資訊?",
                            actions = [
                                MessageAction(
                                    label = "Yes",
                                    text = "我想了解^_^"
                                ),
                                MessageAction(
                                    label = "No",
                                    text = "先不要好了T_T"
                                )
                            ]
                        )
                ))
            elif msg == "我想了解^_^":
                reply = "好的請輸入步道名稱>_<"
                print(reply)
                line_bot_api.reply_message(token,TextSendMessage(reply))
            elif msg == "先不要好了T_T":
                reply = "好吧若您有需要再跟我說喔T^T"
                print(reply)
                line_bot_api.reply_message(token,TextSendMessage(reply))   
            else:
                global db, mount_df
                    
                uri = "mongodb+srv://alex111122221111:sandia100alex@hiking.46ndoin.mongodb.net/?retryWrites=true&w=majority"
                client = MongoClient(uri, server_api=ServerApi('1'))
                try:
                    client.admin.command('ping')
                    print("Pinged your deployment. You successfully connected to MongoDB!")
                except Exception as e:
                    print(e)

                db = client.hikin_gdb
                col = db.hiking_col
                result = list(col.find()) 

                df = pd.DataFrame(result)
                df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
                # print(df)

                mount_df = df[df["name"].isin([str(msg)])]
                if not mount_df.empty:
                    msg_name = mount_df.iat[0,1]
                    # print(msg_name)
                    msg_score = mount_df.iat[0,3]
                    # print(msg_score)
                    msg_place = hiking_location()
                    # print(msg_place)
                    msg_difficulty = hiking_difficulty()
                    # print(msg_difficulty)
                    msg_distance = str(int(mount_df.iat[0,21]))
                    # print(msg_distance)
                    msg_time = mount_df.iat[0,22]
                    # print(msg_time)
                    msg_altitude = str(str(int(mount_df.iat[0,27]))+" ~ "+str(int(mount_df.iat[0,28])))
                    # print(msg_altitude)
                    msg_height_diff = str(int(mount_df.iat[0,29]))
                    # print(msg_height_diff)
                    msg_website = mount_df.iat[0,2]
                    # print(msg_website)
                    mount_reply = f"Name : {msg_name}\nScore : {msg_score}\nPlace : {msg_place}\nDifficulty : {msg_difficulty}\nDistance : {msg_distance} 公里\nTime : {msg_time}\nAltitude : {msg_altitude} 公尺\nHeight difference : {msg_height_diff} 公里\nWebsite : {msg_website}"
                    print(mount_reply)
                    # line_bot_api.reply_message(token,TextSendMessage(mount_reply))   
                    hiking_selection_reply(mount_reply, token, access_token)
                else:
                    reply = "可能您輸入的名稱有誤\n或是還沒有該步道資料\n因此查無相關步道資料喔T_T"
                    print(reply)
                    line_bot_api.reply_message(token,TextSendMessage(reply))
        else:
            reply = '你傳的不是文字呦～'
            print(reply)
            line_bot_api.reply_message(token,TextSendMessage(reply))
    except:
        print(body)
    
    return "OK"

def hiking_first_ask():

    line_bot_api = LineBotApi("CuVcNmfbWzuJshyHnZwOfNO84W0xiNOsm1Xq8aBVL5HMNnbOr7hmNDDk+xQ2iXCY3eBElLNf6CpxKXHVyOtsRYIdQqUMLFLSDSZtmNBgjX4g3sOUHYGb+6YflB9tFjYgzzd9U4Jo/dGRO7Gu39QIHwdB04t89/1O/w1cDnyilFU=")  
    line_bot_api.push_message("U6a3ba421ceaeff0c96b0d7fbb53c09d1", TemplateSendMessage(
    alt_text = "個人化步道挑選",
    template = ConfirmTemplate(
            text = "是否要個人化步道挑選?",
            actions = [
                MessageAction(
                    label = "Yes",
                    text = "好呀<3"
                ),
                MessageAction(
                    label = "No",
                    text = "不謝了QQ"
                )
            ]
        )
))

def hiking_location():
    global mount_location
    db = client.hikin_gdb
    col = db.hiking_col
    result = list(col.find()) 

    df = pd.DataFrame(result)
    df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])

    if mount_df.iat[0,5] == "-":
        mount_location = mount_df.iat[0,4]
    else:
        if mount_df.iat[0,6] == "-":
            mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]
        else:
            if mount_df.iat[0,7] == "-":
                mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]
            else:
                if mount_df.iat[0,8] == "-":
                    mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]
                else:
                    if mount_df.iat[0,9] == "-":
                        mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]
                    else:
                        if mount_df.iat[0,10] == "-":
                            mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]
                        else:
                            if mount_df.iat[0,11] == "-":
                                mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]
                            else:
                                if mount_df.iat[0,12] == "-":
                                    mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]
                                else:
                                    if mount_df.iat[0,13] == "-":   
                                        mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]
                                    else:
                                        if mount_df.iat[0,14] == "-":  
                                            mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]+mount_df.iat[0,13]
                                        else:
                                            if mount_df.iat[0,15] == "-":
                                                mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]+mount_df.iat[0,13]+"\n"+mount_df.iat[0,14]
                                            else:
                                                if mount_df.iat[0,16] == "-":
                                                    mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]+mount_df.iat[0,13]+"\n"+mount_df.iat[0,14]+mount_df.iat[0,15]
                                                else:
                                                    if mount_df.iat[0,17] == "-":
                                                        mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]+mount_df.iat[0,13]+"\n"+mount_df.iat[0,14]+mount_df.iat[0,15]+"\n"+mount_df.iat[0,16]
                                                    else:
                                                        if mount_df.iat[0,18] == "-":
                                                            mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]+mount_df.iat[0,13]+"\n"+mount_df.iat[0,14]+mount_df.iat[0,15]+"\n"+mount_df.iat[0,16]+mount_df.iat[0,17]
                                                        else:
                                                            if mount_df.iat[0,19] == "-":
                                                                mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]+mount_df.iat[0,13]+"\n"+mount_df.iat[0,14]+mount_df.iat[0,15]+"\n"+mount_df.iat[0,16]+mount_df.iat[0,17]+"\n"+mount_df.iat[0,18]
                                                            else:
                                                                mount_location = mount_df.iat[0,4]+mount_df.iat[0,5]+"\n"+mount_df.iat[0,6]+mount_df.iat[0,7]+"\n"+mount_df.iat[0,8]+mount_df.iat[0,9]+"\n"+mount_df.iat[0,10]+mount_df.iat[0,11]+"\n"+mount_df.iat[0,12]+mount_df.iat[0,13]+"\n"+mount_df.iat[0,14]+mount_df.iat[0,15]+"\n"+mount_df.iat[0,16]+mount_df.iat[0,17]+"\n"+mount_df.iat[0,18]+mount_df.iat[0,19]
    return mount_location

def hiking_difficulty():
    global mount_difficulty
    if str(mount_df.iat[0,20]) == "1":
        mount_difficulty = "低"
    elif str(mount_df.iat[0,20]) == "2":
        mount_difficulty = "低-中"
    elif str(mount_df.iat[0,20]) == "3":
        mount_difficulty = "中"
    elif str(mount_df.iat[0,20]) == "4":
        mount_difficulty = "中-高"
    elif str(mount_df.iat[0,20]) == "5":
        mount_difficulty = "高"
    return mount_difficulty

def hiking_selection_reply(msg, Reply_token, Access_token):
    headers = {"Authorization": f"Bearer {Access_token}","Content-Type":"application/json"}    
    body = {
    "replyToken":str(Reply_token),
    "messages":[{
          "type": "text",
          "text": str(msg)
        }]
    }
    req = requests.request("POST", "https://api.line.me/v2/bot/message/reply", headers=headers,data=json.dumps(body).encode("utf-8"))
    print(req.text)

if __name__ == "__main__":

    uri = "mongodb+srv://alex111122221111:sandia100alex@hiking.46ndoin.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    hiking_first_ask()
    app_line.run()

    warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)


