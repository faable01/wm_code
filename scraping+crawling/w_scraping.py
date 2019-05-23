"""
    ---- 事前調査で判明していること -----
    Workship MagazineのENGINEERカテゴリ記事一覧：https://goworkship.com/magazine/engineer/
    １ページに最大13記事の一覧が表示
    このURLにパラメータ"page"を渡すことで、指定するページを開ける
    (例：page=1, page=2, page=3, ...)

    最大13記事の一覧の他、ページ下部には常に最新記事の一覧が4件と、トレンド記事の一覧が4件表示される
    最新記事一覧とトレンド記事一覧は無視する
    記事のタイトルはclassが"article-title"の見出しタグに記されている

    記事の存在しないページを指定すると、ページ下部の最新記事一覧4件とトレンド記事一覧4件を除いて記事が表示されない
    そのため、classが"article-title"の要素がページ内に8件しか見つからなくなったら、これ以上は記事が存在しない。
"""

# 使いやすさが評価されているPythonのHTTPライブラリ
import requests

# HTML、XMLのパーサ（構文解析をするためのライブラリ）
from bs4 import BeautifulSoup

# 時刻に関する関数を提供するモジュール
import time

# ENGIINEERカテゴリの全記事のタイトルを格納する変数
all_title_list = []

# 指定するページ（以下while文中でカウントアップしていく）
page_index = 1

# 通信時のHTTPヘッダに設定する値
headers = {
    # User-Agentに設定する値
    # サイト管理者に分かるよう自身の連絡先などを記載する
    'User-Agent': 'sig-Bot/1.0 (@sig_Left: https://twitter.com/sig_Left)'
}

# 全てのページを探索するまでループ
while True:
    print(f'{page_index}ページ目解析開始')
    
    # アクセスするURL
    url = f'https://goworkship.com/magazine/engineer/page/{page_index}/'
    
    # 通信結果
    res = requests.get(url, headers=headers)
    
    # 指定ページのHTML
    html = res.text
    
    # HTMLを解析したBeautifulSoupオブジェクト
    soup = BeautifulSoup(html, 'html.parser')
    
    # このページの記事タイトルのHTML要素一覧を取得
    title_tag_list = soup.select('.article-title')
    
    # 記事タイトルのHTML要素が8つ以下の場合、これ以上記事は存在しないためループを抜ける
    # (最新記事一覧4件とトレンド記事一覧4件を除いて記事一覧が0件の状態)
    if (len(title_tag_list) <= 8):
        print('全ページ走査完了')
        break
    
    # ページ下部に常に表示される最新記事一覧4件とトレンド記事一覧4件を省く
    target_tag_list = title_tag_list[:-8]
    
    # 記事タイトル一覧
    title_list = [tag.string for tag in target_tag_list]
    
    # タイトル一覧をループ外の変数に格納
    all_title_list.extend(title_list)
    
    print(f'{page_index}ページ目解析終了')
    
    # ページのカウントアップ
    page_index += 1
    
    # 次のループに行く前に1秒待機(サイトに負荷をかけないため)
    time.sleep(2)

# 全記事一覧を出力
for title in all_title_list:
    print(title)

