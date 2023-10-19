from geopy.geocoders import Nominatim
from flask import *
import requests
import json
import getweather
import threading
import time
import schedule

app = Flask(__name__)

# calling the nominatim tool
geoLoc = Nominatim(user_agent="GetLoc")
 

weather_api_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
#"latitude":"25.0575931","longitude":"121.3625344"
@app.route('/get_weather', methods=['GET'])
def get_weather():
    data = request.get_json()
    authorization = data.get('Authorization')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # location = data.get('locationName')
    locname = geoLoc.reverse("25.0575931, 121.3625344")
    address_parts = locname.address.split(", ")
    if len(address_parts) >= 4:
        location = address_parts[-3]#縣市
        district = address_parts[-4]#區域
        print("縣市:", location)
        print("區域:", district)
    else:
        print("地址訊息不足")
    print(locname.address)
    if not authorization or not latitude or not longitude:
        return jsonify({'error': '前端缺少參數'})

    params = {
        'Authorization': authorization,
        'locationName': location,
        'format': 'JSON',  
    }
    try:
        response = requests.get(weather_api_url, params=params)
        response.raise_for_status()  

        try:
            weather_data = response.json()
            return jsonify(weather_data)
        except json.JSONDecodeError as e:
            return jsonify({'error': 'API無法解析為json'})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'API請求失敗'})

@app.route("/")
def index():
	return render_template("index.html")

def sendmsg(name,content):
    webhook_url="https://discordapp.com/api/webhooks/1163495849842704565/I7SJdtkonFMMvuXFs3GQTshXtwCB47N3juFGLNtBf1bLAevRIXukZdH82j31jfhRbCxQ"
    data={"content":"Hi "+name+",\n"+content}
    headers = {'Content-Type': 'application/json'}
    requests.post(webhook_url, data=json.dumps(data), headers=headers)

#control=0 =>will not send msg to discord
control=0

def schedule_sendmsg(name,content):
    global control
    while control==1:
        schedule.every().monday.at("09:00").do(sendmsg,name,content[0])#早上發
        schedule.every().tuesday.at("09:00").do(sendmsg,name,content[0])
        schedule.every().wednesday.at("09:00").do(sendmsg,name,content[0])
        schedule.every().thursday.at("09:00").do(sendmsg,name,content[0])
        schedule.every().friday.at("09:00").do(sendmsg,name,content[0])
        schedule.every().monday.at("18:00").do(sendmsg,name,content[1])#晚上發
        schedule.every().tuesday.at("18:00").do(sendmsg,name,content[1])
        schedule.every().wednesday.at("18:00").do(sendmsg,name,content[1])
        schedule.every().thursday.at("18:00").do(sendmsg,name,content[1])
        schedule.every().friday.at("18:00").do(sendmsg,name,content[1])
        schedule.run_pending()
        time.sleep(60)

#set control=1 and open clock to send msg to discord
@app.route('/api/remind', methods=['GET'])
def api_remind():
    global control
    #need to add query string ex: /api/remind?username=123&cityselect=新北市
    city=request.args.get("cityselect")
    username=request.args.get("username")
    data=getweather.get_location_weather(city)
    try:
        control=1
        task_thread = threading.Thread(target=schedule_sendmsg, args=(username, data))
        task_thread.daemon = True
        task_thread.start()

        data = {"message":"成功發送"}
        return jsonify(data)
    except Exception as e:
        return jsonify({"error":"發送失敗"+str(e)})


#set control=0 and turn off reminder
@app.route('/api/turnoff', methods=['GET'])
def api_turnoff():
    global control
    try:
        control=0
        print(control)
        data = {"message":"成功關閉"}
        return jsonify(data)
    except Exception as e:
        return jsonify({"error":"關閉失敗"+str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)