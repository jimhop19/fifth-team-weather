import requests
webhook_url = "https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS"

cwbURL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-9B9EE211-7CB8-4A62-B86E-8EF36E669E1B&format=JSON"

response = requests.get(cwbURL)

if response.status_code == 200:
    weather_data = response.json()

    locations = weather_data["records"]["location"] #取出內容

    for i in locations:
        location_name = i["locationName"]
        if location_name == "臺北市":
            wx12 = i['weatherElement'][0]['time'][0]['parameter']['parameterName'] # 天氣現象
            pop12 = i['weatherElement'][1]['time'][0]['parameter']['parameterName'] # 降雨機率
            mint12 = i['weatherElement'][2]['time'][0]['parameter']['parameterName'] # 最低溫
            maxt12 = i['weatherElement'][4]['time'][0]['parameter']['parameterName'] #最高溫  
            message = (f'{location_name}目前天氣{wx12}，最高溫 {maxt12} 度，最低溫 {mint12} 度，降雨機率 {pop12} %')

            embed = {
                'title': "即時天氣預報",
                "description": "提供您最即時的天氣",
                "author": {"name": "氣象將軍"},
                "thumbnail": {"url": "https://www.upmedia.mg/upload/content/20210531/jb210531134512571271.jpg"},
                'fields': [
                    {"name": "城市名稱", "value": f'{location_name}', "inline": True},
                    {'name': '目前天氣', 'value': f'{wx12}', 'inline': True},
                    {'name': '最高溫度', 'value': f'{maxt12} 度', 'inline': True},
                    {'name': '最低溫度', 'value': f'{mint12} 度', 'inline': True},
                    {'name': '降雨機率', 'value': f'{pop12}%', 'inline': True}
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
else:
    print(f"Failed to retrieve weather data. Status code: {response.status_code}")

