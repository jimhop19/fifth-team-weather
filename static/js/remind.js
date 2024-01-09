//name
let nameLabel = document.createElement("span");
nameLabel.textContent = "姓名";
let usernameInput = document.createElement("input");
usernameInput.id = "username";
usernameInput.type = "text";

// city
let cityLabel = document.createElement("span");
cityLabel.textContent = "公司地點";
let citySelect = document.createElement("select");
citySelect.id = "city";

let cities = ["請選擇縣市", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣", "臺北市", "新北市", "桃園市", "台中市", "台南市", "高雄市", "基隆市", "新竹縣", "新竹市", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "屏東縣"];
for (let i = 0; i < cities.length; i++) {
  let option = document.createElement("option");
  option.value = cities[i];
  option.textContent = cities[i];
  citySelect.appendChild(option);
}

// turn on remind
let remindButton = document.createElement("button");
remindButton.textContent = "開啟提醒";
remindButton.addEventListener("click", remind);

//add content
let turnoffButton = document.createElement("button");
turnoffButton.textContent = "關閉提醒";
turnoffButton.addEventListener("click", turnoff);

let container = document.getElementById("container");
container.appendChild(nameLabel);
container.appendChild(usernameInput);
container.appendChild(document.createElement("br"));
container.appendChild(cityLabel);
container.appendChild(citySelect);
container.appendChild(document.createElement("br"));
container.appendChild(remindButton);
container.appendChild(turnoffButton);


function remind(){
    let username=document.getElementById("username").value;
    let cityselect=document.getElementById("city").value;
    let url = `/api/remind?username=${username}&cityselect=${cityselect}`;
    fetch(url, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function turnoff(){

    let url = `/api/turnoff`;
    fetch(url, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}