# coding: utf8

import logging
import re
from .crawlerBase import CrawlerBase
from .helper.chinese_digit import getResultForDigit


class BilibiliCrawler(CrawlerBase):

    def parseEpisode(self):
        # Get episode number from page
        result = re.findall('"index":"([^"]+)"', self.soup.get_text())
        if result is None:
            print("can't find result")
            return None
        episodeText = result[-1]
        episodeNumText = re.search('\d+', episodeText)

        self.episode = 0
        if episodeNumText is None:
            logging.info('Could not find episodeNumText, maybe chinese?')
            episodeNumText = re.search('[零一二三四五六七八九十]+', episodeText)
            if episodeNumText is None:
                logging.warning('Could not find episodeNumText')
                return None
            else:
                # convert chinese number to digital number
                print(episodeNumText.group(0))
                self.episode = getResultForDigit(episodeNumText.group(0))
        else:
            # normal number
            self.episode = int(episodeNumText.group(0))
        logging.info('Found episode ' + str(self.episode))
        return self.episode

    def parseName(self):
        titleElems = self.soup.select('.media-info-title-t')
        if titleElems is None:
            logging.warning('Could not find episode elements')
            return
        self.name = titleElems[0].getText()
        logging.info('Found name ' + str(self.name))
        return self.name
