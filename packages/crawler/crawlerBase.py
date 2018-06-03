# coding: utf8

import requests
import bs4


class CrawlerBase():

    def __init__(self, url=None):
        if url is not None:
            self.downloadPage(url)

    def downloadPage(self, url):
        # Download page
        res = requests.get(url)
        res.raise_for_status()
        # HACK resolve cartoonmad big5 encoding problem
        if "cartoonmad.com" in url:
            res.encoding = 'big5'
        self.url = url
        self.soup = bs4.BeautifulSoup(res.text, 'html.parser')
