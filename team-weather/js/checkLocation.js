if ("geolocation" in navigator) {
    console.log("可以取得位置")
    navigator.geolocation.getCurrentPosition(function (position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;
      // 在控制台打印经度和纬度
      console.log("纬度：" + latitude);
      console.log("经度：" + longitude);
  
    });
  } else {
    console.log("不支援gps");
  }
  