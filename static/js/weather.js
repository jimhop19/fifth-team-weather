// debugger;
fetch("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-42D39801-FE06-49C5-9922-94562DF2C43B").then((response) => {
    return response.json();
}).then((data) => {
    console.log("data:", data);
    records = data.records;


    for (let i = 0; i < records.location.length; i++) {
        const location = records.location[i];
        const locationitem = document.createElement("div");
        locationitem.className = "locationName";
        locationitem.id = "chart"+ records.location[i].locationName;
        locationitem.textContent = records.location[i].locationName + ":"



        const avg = [];
        const timelist = [];
        for (let j = 0; j < 3; j++) {
            const maxT = parseFloat(records.location[i].weatherElement[4].time[j].parameter.parameterName);
            const minT = parseFloat(records.location[i].weatherElement[2].time[j].parameter.parameterName);
            const time = (records.location[i].weatherElement[2].time[j].startTime);
            console.log("maxT:" + maxT)
            console.log("minT:" + minT)
            console.log("avg1:" + avg)
            console.log(time)
            const avgvalue = (maxT + minT) / 2;
            console.log("miavgvalue:" + avgvalue)
            timelist.push(time);
            avg.push(avgvalue);
        }
        console.log("36小時平均溫度:" + avg)
        console.log(records.location[i]);
        const avgitem = document.createElement("div");
        avgitem.textContent = avg

        const canvas = document.createElement("canvas");
        canvas.id = "chart-" + i; // Unique ID for each chart

        

        canvas.classList.add("chart")
  

        locationitem.appendChild(canvas);
        const ctx = canvas.getContext("2d");

        const maxDataValue = Math.max(...avg);
        const minDataValue = Math.min(...avg);
        const yAxisMin = Math.floor(minDataValue) - 3;
        const yAxisMax = Math.ceil(maxDataValue) + 3;
        const myLineChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: timelist,
                datasets: [{
                    label: "最近溫度",
                    data: avg,
                    fill: false, // 下方是否填滿
                    borderColor: "#c08041",
                    tension: 0.1, // 曲線平滑度

                }]
            },
            options: {
                scales: {
                    y: {
                        suggestedMin: yAxisMin,
                        suggestedMax: yAxisMax
                    }
                }
            }
        });


        const container = document.querySelector("#chartInformation");
        container.appendChild(locationitem);
    }
});



