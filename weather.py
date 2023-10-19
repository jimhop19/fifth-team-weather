from flask import *
import requests
from apscheduler.schedulers.background import BackgroundScheduler 
from apscheduler.triggers.cron import CronTrigger
import pytz

app = Flask(__name__)
app.debug = True
app.secret_key = 'your_secret_key_here'
city_name = None
webhook_url = "https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS"


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/subscribe", methods=["POST"])
def set_city():
    data = request.get_json()
    new_city_name = data.get('region', '')
    global city_name
    city_name = new_city_name
    return jsonify({"ok": True, "message": "訂閱成功"})

def subscribe_weather():
    global city_name  
    cwbURL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-9B9EE211-7CB8-4A62-B86E-8EF36E669E1B&format=JSON"
    response = requests.get(cwbURL)
    if response.status_code == 200:
        weather_data = response.json()
        locations = weather_data["records"]["location"]
        for i in locations:
            location_name = i["locationName"]
            if location_name == city_name:
                wx12 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
                pop12 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']
                mint12 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
                maxt12 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']

                embed = {
                    'title': f"{location_name}的今日天氣",
                    "description": "早安您好",
                    "author": {"name": "氣象將軍"},
                    "thumbnail": {"url": "https://www.upmedia.mg/upload/content/20210531/jb210531134512571271.jpg"},
                    'fields': [
                        {'name': '目前天氣', 'value': f'{wx12}', 'inline': False},
                        {'name': '最高溫度', 'value': f'{maxt12} 度', 'inline': False},
                        {'name': '最低溫度', 'value': f'{mint12} 度', 'inline': False},
                        {'name': '降雨機率', 'value': f'{pop12}%', 'inline': False}
                    ],
                    "footer": {"text": "氣象將軍關心您的身體健康！"}
                }

                data = {
                    'username': '氣象機器人',
                    'embeds': [embed]
                }

                headers = {
                    'Content-Type': 'application/json'
                }

                response_discord = requests.post(webhook_url, json=data, headers=headers)

                if response_discord.status_code == 204:
                    print(f"Message sent to Discord for {location_name}")
                else:
                    print(f"Failed to send message to Discord for {location_name}. Status code: {response_discord.status_code}")


if __name__ == "__main__":
    taiwan_timezone = pytz.timezone("Asia/Taipei")
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(subscribe_weather, trigger=CronTrigger(hour=10, minute=20, timezone=taiwan_timezone))  
    scheduler.start()
    app.run()