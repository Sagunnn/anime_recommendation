from flask import Flask, jsonify
from bs4 import BeautifulSoup
import json
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/api/home", methods=['GET'])

def return_home():
  updates = manhwa_updates()
  return updates

def manhwa_updates():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Fri, 02 Aug 2024 15:13:32 GMT',
        'priority': 'u=0, i',
        'referer': 'https://elarctoons.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    elarcpage = requests.get('https://elarctoons.biz/', headers=headers)
    elarc = BeautifulSoup(elarcpage.content, 'html.parser')

    # Attempt to find the element with error handling
    manhwa_elarc = elarc.find_all('div', class_='luf')[:10]

    data_json = []
    for name in manhwa_elarc:
        if name:
            manhwa_link = name.find('a')['href']
            chapter = name.find('li').find('a').text
            chapter_link = name.find('li').find('a')['href']
            update = name.find('li').find('span').text
            manhwa_title = name.find('a')['title'].strip()
            data_json.append({
                "Title": manhwa_title,
                "Chapter": chapter,
                "Chapter Link": chapter_link,
                "Update": update,
                "Link": manhwa_link
            })
        else:
            print("End of List")

    return data_json

if __name__ == "__main__":
    app.run(debug=True,port=5000)
