print("================task1================")
def find_and_print(messages, current_station):
    # 定義綠線主線和支線的站點列表
    green_line_main = [
        "Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
        "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-Shek Memorial Hall",
        "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei", "Dapinglin",
        "Qizhang", "Xindian City Hall", "Xindian"
    ]
    green_line_branch = ["Qizhang", "Xiaobitan"]

    station_distances = {
        "Songshan": 0,
        "Nanjing Sanmin": 1,
        "Taipei Arena": 2,
        "Nanjing Fuxing": 3,
        "Songjiang Nanjing": 4,
        "Zhongshan": 5,
        "Beimen": 6,
        "Ximen": 7,
        "Xiaonanmen": 8,
        "Chiang Kai-Shek Memorial Hall": 9,
        "Guting": 10,
        "Taipower Building": 11,
        "Gongguan": 12,
        "Wanlong": 13,
        "Jingmei": 14,
        "Dapinglin": 15,
        "Qizhang": 16,
        "Xindian City Hall": 17,
        "Xindian": 18,
        "Xiaobitan": 17  # 距離 Qizhang1站
    }

    # 初始化最小距離和最近的朋友
    min_distance = float('inf')
    nearest_friend = None

    # 掃完messages中的每個朋友
    for friend, message in messages.items():
        # messenger中提取朋友所在站點
        friend_station = None
        for station in green_line_main + green_line_branch:
            if station in message:
                friend_station = station
                break
        # 如果找不到朋友的站點，跳過這個朋友
        if friend_station is None:
            continue

        # 計算當前站點和朋友所在站點之間的距離
        if current_station == "Xiaobitan" or friend_station == "Xiaobitan":
            # 如果current站點是 Xiaobitan         
            current_station_for_distance = current_station
            if current_station == "Xiaobitan":
                current_station_for_distance = "Qizhang"

            # 如果朋友的站點是 Xiaobitan
            friend_station_for_distance = friend_station
            if friend_station == "Xiaobitan":
                friend_station_for_distance = "Qizhang"

            # 計算兩個站點之間的距離，並加1
            current_distance = abs(station_distances[current_station_for_distance] - station_distances[friend_station_for_distance]) + 1
        else:
            # 如果兩個站點都不是 Xiaobitan，則直接計算
            current_distance = abs(station_distances[current_station] - station_distances[friend_station])

        # 如果距離小於最小距離，則更新最小距離和最近的朋友
        if current_distance < min_distance:
            min_distance = current_distance
            nearest_friend = friend
    
    print(nearest_friend)


messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")  # print Leslie
find_and_print(messages, "Ximen")  # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian
# find_and_print(messages, "Xiaobitan")  # print Leslie

print("================task2================")
def book(consultants, hour, duration, criteria):
    # 計算預約的結束時間
    end_time = hour + duration

    # 檢查每個顧問的可用性
    available_consultants = []
    for consultant in consultants:
        # 檢查顧問是否已經有預約
        if "bookings" not in consultant:
            consultant["bookings"] = []  # 初始化預約列表

        # 檢查是否有時間重疊
        is_available = True
        for booking in consultant["bookings"]:
            if not (end_time <= booking["start"] or hour >= booking["end"]):
                is_available = False
                break

        # 如果顧問可用，加入可用列表
        if is_available:
            available_consultants.append(consultant)

    # 如果沒有可用的顧問，輸出 "No Service"
    if not available_consultants:
        print("No Service")
        return

    # 根據選擇標準選擇顧問
    if criteria == "price":
        # 選擇價格最低的顧問
        selected_consultant = min(available_consultants, key=lambda x: x["price"])
    elif criteria == "rate":
        # 選擇評分最高的顧問
        selected_consultant = max(available_consultants, key=lambda x: x["rate"])
    else:
        print("Invalid criteria")
        return

    # 將預約時間加入顧問的預約列表
    selected_consultant["bookings"].append({"start": hour, "end": end_time})

    # 輸出選擇的顧問名字
    print(selected_consultant["name"])

consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]

book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")   # John
book(consultants, 11, 1, "rate")   # Bob
book(consultants, 11, 2, "rate")   # No Service
book(consultants, 14, 3, "price")  # John

print("================task3================")
def func(*data):
    # middle names 收集進字典 
    middle_name_dict = {}
    for name in data:
        words = list(name)  # 用list切字元
        if len(words) == 2:
            middle_name = words[1]  # 2-word names 取2
        elif len(words) == 3:
            middle_name = words[1]  # 3-word names 取2
        elif len(words) == 4:
            middle_name = words[2]  # 4-word names 取3
        else :
            middle_name = words[2]  # 5-word names 取3

        # middle name 對應到 full name，用append將字典的value用list加入
        if middle_name in middle_name_dict:
            middle_name_dict[middle_name].append(name)
        else:
            middle_name_dict[middle_name] = [name]

    # 找出 unique middle name
    unique_full_name = None  #對應空值印沒有
    for middle_name, full_names in middle_name_dict.items():
        if len(full_names) == 1:  
            unique_full_name = full_names[0]
            break

    # Print 
    if unique_full_name:
        print(unique_full_name)
    else:
        print("沒有")
    
    # print(middle_name_dict)  這行檢查邏輯

func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安

print("================task4================")
def get_number(index):

    if index == 0 :
        return 0
    #3個一組 計算第幾組  從0開始
    n=index//3
    #計算組內第幾個  順序(0,1,2)  
    i=index%3
    print(7*n+4*i)
    
get_number(1)# print 4
get_number(5) # print 15
get_number(10)# print 25
get_number(30)# print 70

print("=================END=================")
