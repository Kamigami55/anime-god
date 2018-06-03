# coding: utf8

import logging
import re
from .crawlerBase import CrawlerBase


class CartoonMadCrawler(CrawlerBase):

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
        episode = int(episodeNumMatch.group(1))
        logging.info('Found episode ' + str(episode))
        return episode

    def parseName(self):
        title = self.soup.title.string
        nameGroup = re.search("^(.+) - 免費", title)
        if nameGroup is None:
            logging.warning('Could not find name')
            return
        name = nameGroup.group(1)
        return name
