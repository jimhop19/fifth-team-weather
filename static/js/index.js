//create map
let svg = d3.select("svg");
const g = svg.append("g");

let projectmethod = d3.geoMercator().center([122, 23.6]).scale(7000);
let pathGenerator = d3.geoPath().projection(projectmethod);

d3.json("./data/COUNTY_MOI_1090820_topo.json")
  .then(data => {     
    const geometries = topojson.feature(data, data.objects.COUNTY_MOI_1090820)     
    g.append("path")
    const paths = g.selectAll("path").data(geometries.features)    
    paths.enter()
      .append("path")
        .attr("d", pathGenerator)
        .attr("class","county")
        .attr("id",t => t.properties["COUNTYNAME"]);   
  })
  .then(()=>{
      const county = document.querySelectorAll(".county")
      county.forEach(e => e.addEventListener("mouseenter",() => functionCheck(e.id)));
      fetchTodayWeatherData("臺北市")
  })

function fetchTodayWeatherData(inputString){    
    const countyName = document.getElementById("countyName");
    countyName.textContent = inputString;    
    const cwaURL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-9B9EE211-7CB8-4A62-B86E-8EF36E669E1B&format=JSON";
    fetch(`${cwaURL}&locationName=${inputString}`)
    .then((data) => {        
        return data.json();        
    })
    .then((result) =>{        
        switchWeatherData(result);        
    })
}
function switchWeatherData(input){
    //weathercondition
    let weatherConditionData = input.records.location[0].weatherElement[0].time[1].parameter.parameterName;
    const weatherCondition = document.getElementById("weatherCondition");
    weatherCondition.textContent = weatherConditionData;
    //comfort
    let comfortData = input.records.location[0].weatherElement[3].time[1].parameter.parameterName;
    const comfort = document.getElementById("comfort");
    comfort.textContent = comfortData;    
    //raining chance
    let raingingData = input.records.location[0].weatherElement[1].time[1].parameter.parameterName;
    const raining = document.getElementById("raining");
    raining.textContent = raingingData;
    //temperature
    let lowestTemperatureData = input.records.location[0].weatherElement[2].time[1].parameter.parameterName;
    const lowestTemperature = document.getElementById("lowestTemperature");
    lowestTemperature.textContent = lowestTemperatureData;
    let highestTemperatureData = input.records.location[0].weatherElement[4].time[1].parameter.parameterName;
    const highestTemperature = document.getElementById("highestTemperature");
    highestTemperature.textContent = highestTemperatureData;
}
//show correspond information
const functionButton = document.querySelectorAll("input[name=functionButton]")
functionButton.forEach(e => e.addEventListener("click",() => {console.log(e.value)}))
//check and swith fuction
function functionCheck(inputData){
    const check = document.querySelector("input:checked")    
    if (check.value === "today"){
        fetchTodayWeatherData(inputData)
    }
}