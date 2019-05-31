"""
    ---- 目的 ----
    Workhisp Magazineのサイトをクローリングし、サイト内のURLを収集する

    ---- 事前調査で判明していること -----
    Workship MagazineのURL：https://goworkship.com/magazine/
    これ以外の情報は持たない状態で、クローリングを実装する
"""

# requests: 使いやすさが評価されているPythonのHTTPライブラリ
# BeautifulSoup: HTML、XMLのパーサ（構文解析をするためのライブラリ）
# urljoin: 相対パスを絶対パスに変換するための関数
# urlparase: URL解析のための関数
# time: 時刻に関する関数を提供するモジュール
# re: 正規表現操作モジュール
# robotparser: robots.txt(サイト側がクローラへアクセス制御を指示するためのtxt)を読み取るモジュール
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import time
import re
import urllib.robotparser


class WebsiteCrawler:
    """
        特定のWebサイト内のリンクを走査し、URLを収集するクローラ.
        走査するWebサイトとその際のユーザーエージェント、収集するURLの限界数をコンストラクタで設定して使用する
    """

    def __init__(self, website_url, user_agent, limit_number):
        """
           website_url: 走査するWebサイトのURL
           user_agent: ユーザエージェント名
           limit_number: 収集するURLの限界数
           all_url_list: 収集したURLを格納するリスト
           target_index: 走査する対象の要素番号
           robotparser: robots.txtを解析するパーサ
        """
        self.website_url = website_url
        self.user_agent = user_agent
        self.limit_number = limit_number
        self.all_url_list = [website_url]
        self.target_index = -1
        self.robotparser = urllib.robotparser.RobotFileParser()

    def __read_robots__(self):
        """
           走査対象のWebサイトのrobots.txtを読み込む
        """
        # クローリングを開始する先頭ページのURLの解析
        parsed = urlparse(self.website_url)

        # robots.txtの配置場所
        robots_url = f'{parsed.scheme}://{parsed.netloc}/robots.txt'

        # robots.txtの読み込み
        self.robotparser.set_url(robots_url)
        self.robotparser.read()
    
    def _clean_url_list(self, url_list):
        """
            収集したURLのリストから余分な情報を除外する
        """
        # 走査対象のWebサイトの外のURLを除去
        website_url_list = list(filter(
            lambda u: u.startswith(self.website_url), url_list
        ))

        # 各URL末尾のURLフラグメントを除去
        non_flagment_url_list = [(
            lambda u: re.match('(.*?)#.*?', u) or re.match('(.*)', u)
        )(url).group(1) for url in website_url_list]
        
        return non_flagment_url_list
    
    def _extract_url(self, beautiful_soup):
        """
            BeautifulSoup解析済みオブジェクトから余分な情報を除外したURLを抽出する
        """
        # rel属性がnofollowではないaタグ一覧を取得する
        a_tag_list = list(filter(
            lambda tag: not 'nofollow' in (tag.get('rel') or ''),
            beautiful_soup.select('a')
        ))

        # aタグ一覧からこのページのURL一覧を取得（href属性の値を取得）
        # この際相対パスを絶対パスに変換する
        url_list = [
            urljoin(self.website_url, tag.get('href')) for tag in a_tag_list
        ]

        # 余分な情報を除外したURL一覧を返ぎ却する
        return self._clean_url_list(url_list)

    def crawl(self):
        """
            インスタンス作成時に指定したWebサイトをクローリングし、
            収集したURLのリストを返却する。
        """
        print('クローリング開始')

        # robots.txtの読み込み
        self.__read_robots__()

        while True:

            # 走査対象のindexをカウントアップする
            self.target_index += 1

            # 走査を終えるかの判定
            len_all = len(self.all_url_list)
            if self.target_index >= len_all or len_all > self.limit_number:
                print('クローリング終了')
                break

            # 初回以降は走査開始まで最低でも1秒は空ける（連続したアクセスでサイトへの負荷をかけないため）
            self.target_index and time.sleep(2)

            print(f'{self.target_index + 1}ページ目開始')

            # 走査対象のURL
            url = self.all_url_list[self.target_index]
            print(f'走査対象：{url}')

            # URLがrobots.txtでアクセス許可されているURLかどうかを判定する
            if not self.robotparser.can_fetch(self.user_agent, url):
                print(f'{url}はアクセスが許可されていません')
                continue  # 次ループへの移行
            
            # 通信結果
            headers = {'User-Agent': self.user_agent}
            res = requests.get(url, headers=headers)

            # 通信結果異常判定
            if res.status_code != 200:
                print(f'通信に失敗しました（ステータス：{res.status_code}）')
                continue  # 次ループへの移行
            
            # 通信結果のHTMLを解析したBeautifulSoupオブジェクト
            soup = BeautifulSoup(res.text, 'html.parser')

            # robots meta判定
            for robots_meta in soup.select("meta[name='robots']"):
                if 'nofollow' in robots_meta['content']:
                    print(f'{url}内のリンクはアクセスが許可されていません')
                    continue  # 次ループへの移行
            
            # 解析済みBeautifulSoupオブジェクトから余分な情報を除去したURL一覧を抽出
            cleaned_url_list = self._extract_url(soup)

            print(f'このページで収集したURL件数：{len(cleaned_url_list)}')

            # 収集したURLの追加
            before_extend_num = len(self.all_url_list)
            self.all_url_list.extend(cleaned_url_list)

            # 重複したURLの除去
            before_duplicates_num = len(self.all_url_list)
            self.all_url_list = sorted(
                set(self.all_url_list), key=self.all_url_list.index
            )
            after_duplicates_num = len(self.all_url_list)

            print(f'重複除去件数：{before_duplicates_num - after_duplicates_num}')
            print(f'URL追加件数：{after_duplicates_num - before_extend_num}')
        
        return self.all_url_list


# メイン処理の実行
if __name__ == '__main__':

    # 走査対象のURL
    target_website = 'https://goworkship.com/magazine/'

    # ユーザーエージェント
    user_agent = 'sig-Bot/1.0 (@sig_Left: https://twitter.com/sig_Left)'

    # 収集するURLの最大件数
    limit_number = 200

    # クローラの作成
    crawler = WebsiteCrawler(target_website, user_agent, limit_number)

    # クローリングの実行
    result_url_list = crawler.crawl()

    # 収集したURLの出力
    print('-------- 結果出力 --------')
    for url in result_url_list:
        print(url)

    print(f'総件数：{len(result_url_list)}')