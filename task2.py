import urllib.request
from bs4 import BeautifulSoup
import csv

def fetch_ptt_page(url):
    # """抓取 PTT 頁面內容"""
    req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Cookie': 'over18=1'
    })
    with urllib.request.urlopen(req) as response:
        return BeautifulSoup(response.read(), "html.parser")

def extract_article_data(soup):
    # """從 PTT 頁面中提取文章資料"""
    article_data = []
    articles = soup.find_all("div", {"class": "r-ent"})
    for article in articles:
        # 找標題
        title_tag = article.find("div", {"class": "title"})
        if not title_tag or "[deleted]" in title_tag.text.strip():
            continue
        title = title_tag.text.strip()

        # 找日期和時間
        date_tag = article.find("div", {"class": "date"})
        if date_tag:
            publish_time = date_tag.text.strip()
        else:
            publish_time = ""

        # 找按讚數
        count_tag = article.find("div", {"class": "nrec"})
        count = count_tag.text.strip() if count_tag else "0"

        article_data.append([title, count, publish_time])
    return article_data

def write_to_csv(filename, data):
    # """將資料寫入 CSV 檔案"""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

if __name__ == "__main__":
    base_url = "https://www.ptt.cc/bbs/Lottery/index.html"
    all_article_data = []
    max_pages = 3

    current_page_url = base_url
    for _ in range(max_pages):
        soup = fetch_ptt_page(current_page_url)
        if not soup:
            break

        articles_data = extract_article_data(soup)
        if articles_data:
            all_article_data.extend(articles_data)

        prev_page_link = soup.find("a", "btn wide", text="‹ 上頁")
        if prev_page_link:
            current_page_url = "https://www.ptt.cc" + prev_page_link["href"]
        else:
            break

    write_to_csv("article.csv", all_article_data)