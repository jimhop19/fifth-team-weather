import requests
import json



def get_location_weather(location):
    print(location)
    url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-577D74D8-60E3-4434-B224-D428D6549CB4&locationName="+str(location)
    print(url)
    response=requests.get(url)
    if response.status_code == 200:
        data=json.loads(response.text)
        reply=[]
        replytext=""
        replytext+="地點:"+data["records"]["location"][0]["locationName"]+"\n" #地點
        replytext+="今天天氣:"+data["records"]["location"][0]["weatherElement"][0]["time"][1]["parameter"]["parameterName"]+"\n" #早上天氣6:00~18:00
        replytext+="降雨機率:"+data["records"]["location"][0]["weatherElement"][1]["time"][1]["parameter"]["parameterName"]+"%\n" #早上降雨機率
        replytext+="最低溫度:"+data["records"]["location"][0]["weatherElement"][2]["time"][1]["parameter"]["parameterName"]+"\n" #早上最低溫度
        replytext+="最高溫度:"+data["records"]["location"][0]["weatherElement"][4]["time"][1]["parameter"]["parameterName"]+"\n" #早上最高溫度
        reply.append(replytext)
        replytext=""
        replytext+="地點:"+data["records"]["location"][0]["locationName"]+"\n" #地點
        replytext+="今天天氣:"+data["records"]["location"][0]["weatherElement"][0]["time"][2]["parameter"]["parameterName"]+"\n" #晚上天氣18:00~24:00
        replytext+="降雨機率:"+data["records"]["location"][0]["weatherElement"][1]["time"][2]["parameter"]["parameterName"]+"%\n" #晚上降雨機率
        replytext+="最低溫度:"+data["records"]["location"][0]["weatherElement"][2]["time"][2]["parameter"]["parameterName"]+"\n" #晚上最低溫度
        replytext+="最高溫度:"+data["records"]["location"][0]["weatherElement"][4]["time"][2]["parameter"]["parameterName"]+"\n" #晚上最高溫度
        reply.append(replytext)
        return reply #陣列 > 第0個是早上天氣，第1個是晚上天氣
    else:
        print("something wrong")
