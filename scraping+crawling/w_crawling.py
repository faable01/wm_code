"""
    ---- 目的 ----
    Workhisp Magazineのサイトをクローリングし、サイト内のURLを収集する

    ---- 事前調査で判明していること -----
    Workship MagazineのURL：https://goworkship.com/magazine/
    これ以外の情報は持たない状態で、クローリングを実装する
"""

# 使いやすさが評価されているPythonのHTTPライブラリ
import requests

# HTML、XMLのパーサ（構文解析をするためのライブラリ）
from bs4 import BeautifulSoup

# 相対パスを絶対パスに変換するための関数
from urllib.parse import urljoin

# URL解析のための関数
from urllib.parse import urlparse

# 時刻に関する関数を提供するモジュール
import time

# 正規表現操作モジュール
import re

# robots.txt(サイト側がクローラへアクセス制御を指示するためのtxt)を読み取るモジュール
import urllib.robotparser

# クローリングを開始する先頭のページ(今回はWorkship Magazineのトップページを指定)
top_url = 'https://goworkship.com/magazine/'

# 通信時のHTTPヘッダに設定する値
headers = {
    # User-Agentに設定する値
    # サイト管理者に分かるよう自身の連絡先などを記載する
    'User-Agent': 'sig-Bot/1.0 (@sig_Left: https://twitter.com/sig_Left)'
}

# クローリングを開始する先頭ページのURLの解析
url_parse_result = urlparse(top_url)

# robots.txtの配置場所
robots_url = f'{url_parse_result.scheme}://{url_parse_result.netloc}/robots.txt'

# robots.txtの読み込み
rp = urllib.robotparser.RobotFileParser()
rp.set_url(robots_url)
rp.read()

# 収集したURLを格納するリスト
all_url_list = [top_url] # 最初のスタート地点であるTOPページを格納

# 走査対象の要素番号
target_index = -1

print('クローリング開始')
while True:

    # 走査対象の要素番号が収集したURLのリストの最後尾に達したか、収集したURLが200ページを越えていたら走査終了
    if target_index >= len(all_url_list) -1 or len(all_url_list) >= 200:
        print('クローリング終了')
        break
    
    # 上記条件に当てはまらない場合、ページのカウントアップをし、走査を続行する
    target_index += 1
    target_index and time.sleep(2)  # 初回以降は走査開始まで最低でも1秒は空ける（連続したアクセスでサイトへの負荷をかけないため）
    print(f'{target_index + 1}ページ目開始')
    
    # 走査対象のURL
    target_url = all_url_list[target_index]

    print(f'走査対象：{target_url}')

    # robots.txtのアクセス制御判定
    is_robots_ng = not rp.can_fetch(headers['User-Agent'], target_url)

    # クローラのアクセスが制限されているページの場合、次のURLの走査に移行する
    if is_robots_ng:
        print(f'{target_url}はアクセスが許可されていません')
        continue  # 次ループへの移行
    
    # 通信結果
    res = requests.get(target_url, headers=headers)
    
    # 指定ページのHTML
    html = res.text
    
    # HTMLを解析したBeautifulSoupオブジェクト
    soup = BeautifulSoup(html, 'html.parser')
    
    # robots_metaがnofollow指定の場合、このページ内のリンクはクローラがアクセスしてはならない
    for robots_meta in soup.select("meta[name='robots']"):
        if 'nofollow' in robots_meta['content']:
            print(f'{target_url}内のリンクはアクセスが許可されていません')
            continue  # 次ループへの移行
    
    # ページ内のaタグ一覧を取得
    # なお、このうちrel属性がnofollowのタグはクローラがアクセスしてはならないので除去する
    a_tag_list = list(filter(lambda tag: not 'nofollow' in (tag.get('rel') or ''), soup.select('a')))
    
    # aタグ一覧からこのページのURL一覧を取得（href属性の値を取得）
    # この際相対パスを絶対パスに変換する
    url_list = [urljoin(target_url, a_tag.get('href')) for a_tag in a_tag_list]
    
    # URL一覧からWorkship Magazine以外のURLを除去する
    url_list_only_wm = list(filter(lambda u: u.startswith(top_url), url_list))

    # URLフラグメントの除去（'https://foo.com/hoo#top'の#top部分）
    url_list_nothing_flagment = [(lambda u: re.match('(.*?)#.*?', u) or re.match('(.*)', u))(url).group(1) for url in url_list_only_wm]
    
    # 収集したURLのリストにこのページで取得したURL一覧を追加
    size_before_extend = len(all_url_list)
    all_url_list.extend(url_list_nothing_flagment)
    
    # 重複するURLを削除する
    size_before_delete = len(all_url_list)
    all_url_list = sorted(set(all_url_list), key=all_url_list.index)
    size_after_delete = len(all_url_list)
    print(f'重複削除件数：{size_before_delete - size_after_delete}')
    print(f'URL追加件数：{size_after_delete -size_before_extend}')
    
    print(f'{target_index + 1}ページ目終了')

# 収集したURLの出力
for url in all_url_list:
    print(url)

print(f'総件数：{len(all_url_list)}')