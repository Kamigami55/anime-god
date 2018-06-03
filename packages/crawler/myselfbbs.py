# coding: utf8

import logging
import re
from .crawlerBase import CrawlerBase


class MyselfBBSCrawler(CrawlerBase):

    def parseEpisode(self):
        # Get episode number from page
        episodeElems = self.soup.select('.z a:nth-of-type(5)')
        if episodeElems == []:
            logging.warning('Could not find episode elements')
            return
        logging.info(episodeElems[0].getText())
        episodeNumText = re.search('【\D*(\d+)', episodeElems[0].getText())
        if episodeNumText is None:
            logging.warning('Could not find episodeNumText')
            return
        episodeNum = int(episodeNumText.group(1))
        logging.info('Found episode ' + str(episodeNum))
        self.episode = episodeNum
        return self.episode

    def parseName(self):
        # Get episode number from page
        episodeElems = self.soup.select('.z a:nth-of-type(5)')
        if episodeElems == []:
            logging.warning('Could not find episode elements')
            return
        logging.info(episodeElems[0].getText())
        # Parse name
        nameElems = re.search('^(.+)【', episodeElems[0].getText())
        if nameElems is None:
            logging.warning('Could not find nameElems')
            return
        self.name = nameElems.group(1)
        logging.info('Found name ' + str(self.name))
        return self.name
