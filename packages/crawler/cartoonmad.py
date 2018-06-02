# coding: utf8

import logging
import requests
import bs4
import re

class CartoonMadCrawler():

    def downloadPage(self, url):
        # Download page
        # logging.info('Checking [CartoonMad] ' + title + '[' + str(episode) + '] : ' + url)
        res = requests.get(url)
        res.raise_for_status()
        self.soup = bs4.BeautifulSoup(res.text, 'html.parser')

    def parseEpisode(self):
        # Get episode number from page
        # Only works for serializing comics
        # TODO: Fix it
        episodeElemImg = self.soup.find("img", src='/image/chap1.gif')
        if episodeElemImg is None:
            logging.warning('Could not find episode element img')
            return
        rx_blanks = re.compile(r"\s+")
        episodeNumText = rx_blanks.sub("", episodeElemImg.parent.contents[2].getText())
        episodeNumMatch = re.search('~(\d+)', episodeNumText)
        if episodeNumMatch is None:
            logging.warning('Could not find episodeNumText')
            return
        episodeNum = int(episodeNumMatch.group(1))
        logging.info('Found episode ' + str(episodeNum))
        self.episode = episodeNum
        return self.episode
