"""
    クローリングを説明するための最小限のコードを書く
"""

import re
import requests
import time
import random

# クローリングを開始するURL
start_url = "https://goworkship.com/magazine/"

# サイト管理者に分かるよう自身の連絡先などをUser-Agentに記載する
headers = {
    'User-Agent': 'sig-Bot/1.0 (@sig_Left: https://twitter.com/sig_Left)'
}

# アクセスするURL(初期値はクローリングを開始するURL)
url = start_url

# HTMLの格納場所
html_list = []

for i in range(5):
    print(f'{i + 1}ページ目クローリング開始')
    
    # 対象ページのhtml
    html = requests.get(url, headers=headers).text
    
    # 取得したHTMLの格納
    html_list.append(html)
    
    # ページ中のaタグ内のURLを取得する
    url = random.choice(re.findall('<a.+?href="(https://.+?)".*?>', html))
    
    # 次のループに行く前に最低でも1秒以上待機する(サイトに負荷をかけないため)
    time.sleep(2)

# 収集したHTMLの出力
for i, html in enumerate(html_list):
    print(f'{i + 1}ページ取得結果')
    print(html)