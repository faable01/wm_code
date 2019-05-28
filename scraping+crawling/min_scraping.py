"""
    スクレイピングを説明するための最小限のコードを書く.
    Workship MagazineのENGINEERカテゴリの最新記事タイトルを取得する
    記事タイトルは以下のように記述されている.
    <h3 class="article-title">IoTソフトウェア開発における7つの課題。決まらない"標準規格"</h3>
"""

import re
import requests

# スクレイピングする対象ページのURL
target_url = "https://goworkship.com/magazine/engineer/"

# サイト管理者に分かるよう自身の連絡先などをUser-Agentに記載する
headers = {
    'User-Agent': 'sig-Bot/1.0 (@sig_Left: https://twitter.com/sig_Left)'
}

# 対象ページのhtml
html = requests.get(target_url, headers=headers).text

# 正規表現で対象ページ中の必要な情報を取得する
reg = '.+article-title.+>(.+)<'
first_article_title = re.search(reg, str).group(1)

print(first_article_title)