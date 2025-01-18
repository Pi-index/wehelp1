console.log("================task1================");
function findAndPrint(messages, currentStation) {
    // 定義綠線主線和支線的站點列表
    const greenLineMain = [
        "Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
        "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-Shek Memorial Hall",
        "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei", "Dapinglin",
        "Qizhang", "Xindian City Hall", "Xindian"
    ];
    const greenLineBranch = ["Qizhang", "Xiaobitan"];

    // 定義站點之間的距離（站數）
    const stationDistances = {};  // 初始化空物件
    for (let idx = 0; idx < greenLineMain.length; idx++) {  // 掃描所有主線站點
        const station = greenLineMain[idx];
        stationDistances[station] = idx;  // 將站點名稱與索引（距離）存入物件
    }
    stationDistances["Xiaobitan"] = stationDistances["Qizhang"] + 1;  // 支線距離為 1 站

    // 初始化最小距離和最近的朋友
    let minDistance = Infinity;
    let nearestFriend = null;

    // 遍歷messages中的每個朋友
    for (const [friend, message] of Object.entries(messages)) {
        // messenger中找朋友所在的站點
        let friendStation = null;
        for (const station of [...greenLineMain, ...greenLineBranch]) {
            if (message.includes(station)) {
                friendStation = station;
                break;
            }
        }


    // 計算當前站點和朋友所在站點之間的距離
    let currentDistance;

    // 檢查當前站點或朋友的站點是否為 Xiaobitan
    if (currentStation === "Xiaobitan" || friendStation === "Xiaobitan") {
        // 如果當前站點是 Xiaobitan，則將當前站點視為 Qizhang
        let currentStationForDistance = currentStation;
        if (currentStation === "Xiaobitan") {
            currentStationForDistance = "Qizhang";
        }

        // 如果朋友的站點是 Xiaobitan，則將朋友的站點視為 Qizhang
        let friendStationForDistance = friendStation;
        if (friendStation === "Xiaobitan") {
            friendStationForDistance = "Qizhang";
        }

        // 計算兩個站點之間的距離
        currentDistance = Math.abs(stationDistances[currentStationForDistance] - stationDistances[friendStationForDistance]);

        // 因為 Xiaobitan 是支線站點，距離 Qizhang 1 站，所以總距離需要加 1
        currentDistance += 1;
    } else {
        // 如果兩個站點都不是 Xiaobitan，則直接計算兩個站點之間的距離
        currentDistance = Math.abs(stationDistances[currentStation] - stationDistances[friendStation]);
    }

        // 如果距離小於最小距離，則更新最小距離和最近的朋友
        if (currentDistance < minDistance) {
            minDistance = currentDistance;
            nearestFriend = friend;
        }
    }
    console.log(nearestFriend);
}

const messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
};

findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian


console.log("================task2================");

function book(consultants, hour, duration, criteria) {
    // 計算預約的結束時間
    const endTime = hour + duration;

    // 檢查每個顧問的可用性
    const availableConsultants = [];
    for (const consultant of consultants) {
        // 檢查顧問是否已經有預約
        if (!consultant.bookings) {
            consultant.bookings = []; // 初始化預約列表
        }

        // 檢查是否有時間重疊
        let isAvailable = true;
        for (const booking of consultant.bookings) {
            if (!(endTime <= booking.start || hour >= booking.end)) {
                isAvailable = false;
                break;
            }
        }

        // 如果顧問可用，加入可用列表
        if (isAvailable) {
            availableConsultants.push(consultant);
        }
    }

    // 如果沒有可用的顧問，輸出 "No Service"
    if (availableConsultants.length === 0) {
        console.log("No Service");
        return;
    }

    // 根據選擇標準選擇顧問
    let selectedConsultant;
    if (criteria === "price") {
        // 選擇價格最低的顧問
        selectedConsultant = availableConsultants.reduce((min, current) => 
            current.price < min.price ? current : min
        );
    } else if (criteria === "rate") {
        // 選擇評分最高的顧問
        selectedConsultant = availableConsultants.reduce((max, current) => 
            current.rate > max.rate ? current : max
        );
    } else {
        console.log("Invalid criteria");
        return;
    }

    // 將預約時間加入顧問的預約列表
    selectedConsultant.bookings.push({ start: hour, end: endTime });

    // 輸出選擇的顧問名字
    console.log(selectedConsultant.name);
}

const consultants = [
    { name: "John", rate: 4.5, price: 1000 },
    { name: "Bob", rate: 3, price: 1200 },
    { name: "Jenny", rate: 3.8, price: 800 }
];

book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate");  // John
book(consultants, 11, 1, "rate");  // Bob
book(consultants, 11, 2, "rate");  // No Service
book(consultants, 14, 3, "price"); // John

console.log("================task3================");
function func(...data) {
    //  middle names 收集
    const middleNameMap = new Map(); //初始化
    for (const name of data) {
        const words = name.split(''); // 切字
        let middleName;
        if (words.length === 2) {
            middleName = words[1]; // 2-word names 取2
        } else if (words.length === 3) {
            middleName = words[1]; // 3-word names 取2
        } else if (words.length === 4) {
            middleName = words[2]; // 4-word names 取3
        } else  {
            middleName = words[2]; // 5-word names 取3
        } 

        // middle name 對應到 full name
        if (middleNameMap.has(middleName)) {
            middleNameMap.get(middleName).push(name);
        } else {
            middleNameMap.set(middleName, [name]);
        }
    }

    // 找出 unique middle name
    let uniqueFullName = null;
    for (const [middleName, fullNames] of middleNameMap.entries()) {
        if (fullNames.length === 1) { 
            uniqueFullName = fullNames[0];
            break;
        }
    }

    if (uniqueFullName) {
        console.log(uniqueFullName);
    } else {
        console.log("沒有");
    }
    // console.log(middleNameMap); // 這行檢查邏輯
} 

func("彭大牆", "陳王明雅", "吳明"); //print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); //print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); //print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); //print 夏曼藍波安

console.log("================task4================");
function getNumber(index) {
    // 處理 index 為 0 的情況
    if (index === 0) {
      return 0;
    }
    // 3 個一組，計算第幾組（從 0 開始） 雙斜線不能用 是註解
    const n = Math.floor(index / 3);
    // 計算組內第幾個，順序 (0, 1, 2)
    const i = index % 3;
  
    console.log ( 7 * n + 4 * i);
  }
  
  getNumber(1); // print 4
  getNumber(5); // print 15
  getNumber(10); //print 25
  getNumber(30); //print 70 

console.log("=================END=================");
console.log("========python檔名為assignment2.py========");
