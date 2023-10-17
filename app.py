from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify
import requests
import json
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

if __name__ == '__main__':
    app.run()
