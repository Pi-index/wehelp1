import json
from urllib.request import urlopen

def fetch_json_data(url):
    with urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))

def extract_district(address):
    for district in ["中正區", "萬華區", "中山區", "大同區", "大安區", "松山區", "信義區", "士林區", "文山區", "北投區", "內湖區", "南港區"]:
        if district in address:
            return district
    return ""

def write_to_csv(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for row in data:
            file.write(",".join(row) + "\n")

data1 = fetch_json_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1")
data2 = fetch_json_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2")

# 合併兩個資料集，以 serial_no 為主鍵
combined_data = {}
for item in data1['data']['results'] + data2['data']:
    serial_no = item['SERIAL_NO']
    if serial_no not in combined_data:
        combined_data[serial_no] = item
    else:
        # 優先使用 data2 if 衝突
        combined_data[serial_no].update(item)

# 提取景點資訊，並按捷運站分組
spot_data = []
mrt_data = {}

for item in combined_data.values():
    title = item['stitle']
    address = item['address']
    longitude = item.get('longitude', '')
    latitude = item.get('latitude', '')
    
    # 提取第一個圖片網址，保留 https://
    image_url = ''
    if 'filelist' in item and item['filelist']:
        filelist = item['filelist']
        if 'https://' in filelist:
            image_url = 'https://' + filelist.split('https://')[1]
        else:
            image_url = filelist

    district = extract_district(address)
    spot_data.append([title, district, longitude, latitude, image_url])

    # 按捷運站分組
    if 'MRT' in item:
        mrt_station = item['MRT']
        if mrt_station not in mrt_data:
            mrt_data[mrt_station] = []
        mrt_data[mrt_station].append(title)

# 將捷運站資料整理成 CSV 格式
mrt_csv_data = []
for mrt_station, spots in mrt_data.items():
    mrt_csv_data.append([mrt_station] + spots)

# 將資料寫入 CSV 檔案
write_to_csv("spot.csv", spot_data)
write_to_csv("mrt.csv", mrt_csv_data)