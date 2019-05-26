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
        走査するWebサイトとその際のユーザーエージェントをコンストラクタで設定して使用する
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

    def _read_robots(self):
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
    
    def _is_robots_ng(self, url):
        """
            指定のURLがrobots.txtでアクセス許可されているURLかどうかを判定する
        """
        return not self.robotparser.can_fetch(self.user_agent, url)

    def _is_end(self):
        """
            クローリングを終了するかを判定する
        """
        len_all = len(self.all_url_list)
        return self.target_index >= len_all or len_all > self.limit_number

    def _remove_out_of_target_website(self, url_list):
        """
            走査対象のWebサイト外のURLをリストから削除する
        """
        return list(filter(lambda u: u.startswith(self.website_url), url_list))
    
    @staticmethod
    def is_nofollow_page(beautiful_soup):
        """
            このページのrobots metaがnofollowかどうかを判定する.
            引数：BeautifulSoup解析済みオブジェクト
        """
        for robots_meta in beautiful_soup.select("meta[name='robots']"):
            if 'nofollow' in robots_meta['content']:
                return True
    
    @staticmethod
    def select_a_tag_removed_nofollow(beautiful_soup):
        """
            rel属性がnofollowではないaタグ一覧を取得する.
            引数：BeautifulSoup解析済みオブジェクト
        """
        return list(filter(
            lambda tag: not 'nofollow' in (tag.get('rel') or ''), 
            beautiful_soup.select('a'))
        )

    @staticmethod
    def remove_url_flagment(url_list):
        """
            URLフラグメントを取り除き、純粋なURLのリストを返却する
            引数：URLのリスト
            （URLフラグメント：'https://foo.com/hoo#top'の#以降のこと）
        """
        return [(
            lambda u: re.match('(.*?)#.*?', u) or re.match('(.*)', u)
        )(url).group(1) for url in url_list]
    
    @staticmethod
    def remove_duplicates(url_list):
        """
            リスト中の文字列から重複するものを削除する
        """
        return sorted(set(url_list), key=url_list.index)

    def crawl(self):
        """
            インスタンス作成時に指定したWebサイトをクローリングし、
            収集したURLのリストを返却する。
        """
        print('クローリング開始')

        # robots.txtの読み込み
        self._read_robots()

        while True:

            # 走査対象のindexをカウントアップする
            self.target_index += 1

            # 走査対象の要素番号が収集したURLのリストの最後尾に達したか、
            # 収集したURLが200ページを越えていたら走査終了
            if self._is_end():
                print('クローリング終了')
                break

            # 初回以降は走査開始まで最低でも1秒は空ける（連続したアクセスでサイトへの負荷をかけないため）
            self.target_index and time.sleep(2)

            print(f'{self.target_index + 1}ページ目開始')

            # 走査対象のURL
            url = self.all_url_list[self.target_index]
            print(f'走査対象：{url}')

            # クローラのアクセスが制限されているページの場合、次のURLの走査に移行する
            if self._is_robots_ng(url):
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
            if self.is_nofollow_page(soup):
                print(f'{url}内のリンクはアクセスが許可されていません')
                continue  # 次ループへの移行

            # ページ内のaタグ一覧を取得
            # なお、このうちrel属性がnofollowのタグはクローラがアクセスしてはならないので除去する
            a_tag_list = self.select_a_tag_removed_nofollow(soup)

            # aタグ一覧からこのページのURL一覧を取得（href属性の値を取得）
            # この際相対パスを絶対パスに変換する
            url_list = [
                urljoin(url, a_tag.get('href')) for a_tag in a_tag_list
            ]

            # このページで取集したURLのリストから余分な情報を除去する
            # (対象Webサイト外のURLとURLフラグメントの除去)
            cleaned_url_list = self.remove_url_flagment(
                self._remove_out_of_target_website(url_list)
            )
            print(f'このページで収集したURL件数：{len(cleaned_url_list)}')

            # 収集したURLの追加
            before_extend_num = len(self.all_url_list)
            self.all_url_list.extend(cleaned_url_list)

            # 重複したURLの除去
            before_duplicates_num = len(self.all_url_list)
            self.all_url_list = self.remove_duplicates(self.all_url_list)
            after_duplicates_num = len(self.all_url_list)
            print(f'重複除去件数：{before_duplicates_num - after_duplicates_num}')
            print(f'URL追加件数：{after_duplicates_num - before_extend_num}')
        
        return self.all_url_list


# メイン処理の実行
if __name__ == '__main__':

    # 走査対象のURL
    target_website = input(
        'クローリングする対象のWebサイトのURLを入力してください >>> '
    )

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