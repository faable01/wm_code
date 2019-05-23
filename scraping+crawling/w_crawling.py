"""
    ---- 事前調査で判明していること -----
    Workship MagazineのURL：https://goworkship.com/magazine/
    これ以外の情報は持たない状態で、クローリングを実装する
"""

# 使いやすさが評価されているPythonのHTTPライブラリ
import requests

# HTML、XMLのパーサ（構文解析をするためのライブラリ）
from bs4 import BeautifulSoup

# 時刻に関する関数を提供するモジュール
import time

# Workship MagazineのURL
url = 'https://goworkship.com/magazine/'

# 通信時のHTTPヘッダに設定する値
headers = {
    # User-Agentに設定する値
    # サイト管理者に分かるよう自身の連絡先などを記載する
    'User-Agent': 'sig-Bot/1.0 (@sig_Left: https://twitter.com/sig_Left)'
}

# 収集したURLのリスト
url_list = [url] # 最初のスタート地点であるTOPページを格納

# # クローリング開始
# while True:
# 収集したURLのリストの最後尾を走査対象とする
target_url = url_list[-1]

# 通信結果
res = requests.get(target_url, headers=headers)

# 指定ページのHTML
html = res.text

# HTMLを解析したBeautifulSoupオブジェクト
soup = BeautifulSoup(html, 'html.parser')



def is_wm_url(target: str) -> str:
    """
        第一引数の文字列が Workship MagazineのURLかどうかを判定する。
        ・'/magazine/business/'のような相対パス : Workship Mgazine URL
        ・'http'
    """