import { switchWeatherData , getChart } from './index.js';

  async function getWeather() {
    if ("geolocation" in navigator) {
        try {
            console.log("可以取得位置");
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject);
            });

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            console.log("經度：" + latitude);
            console.log("緯度：" + longitude);

            const params = {
                Authorization: "CWA-EA196565-58F6-478D-8540-2FC424BF12BA",  
                latitude: latitude,
                longitude: longitude,
            };

            const response = await fetch('/get_weather', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(params),
            });

            const data = await response.json();
            switchWeatherData(data);
            getChart(data);
            console.log('天氣數據：', data);
        } catch (error) {
            console.error('獲取位置失敗：', error);
        }
    } else {
        console.log("不支援 GPS");
    }
}

getWeather();