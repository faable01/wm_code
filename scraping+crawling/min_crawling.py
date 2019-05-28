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

for i in range(5):

    # アクセスするURL(初期値はクローリングを開始するURL)
    url = start_url

    # for i in range(5):
    # 対象ページのhtml
    html = requests.get(url, headers=headers).text

    # ページ中のaタグ内のURLを取得する
    url = random.choice(re.findall('<a.*?href="(https://.+?)".*?>', html))

    # 取得したURLの出力
    print(url)

    # 次のループに行く前に最低でも1秒以上待機する(サイトに負荷をかけないため)
    time.sleep(2)