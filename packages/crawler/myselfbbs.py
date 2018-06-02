# coding: utf8

import logging
import requests
import bs4
import re


class MyselfBBSCrawler():

    def downloadPage(self, url):
        # Download page
        # logging.info('Checking [Myself-bbs] ' + title + '[' + str(episode) + '] : ' + url)
        res = requests.get(url)
        res.raise_for_status()
        self.soup = bs4.BeautifulSoup(res.text, 'html.parser')

    def parseEpisode(self):
        # Get episode number from page
        episodeElems = self.soup.select('.z a:nth-of-type(5)')
        if episodeElems == []:
            logging.warning('Could not find episode elements')
            return
        logging.info(episodeElems[0].getText())
        episodeNumText = re.search('\d+', episodeElems[0].getText())
        if episodeNumText is None:
            logging.warning('Could not find episodeNumText')
            return
        episodeNum = int(episodeNumText.group(0))
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
        self.name = int(nameElems.group(1))
        logging.info('Found name ' + str(self.name))
        return self.name
