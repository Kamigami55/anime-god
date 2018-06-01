# coding: utf8

import logging
import requests
import bs4
import re

# Check animes on Myself-bbs
def checkMyselfBBS(anime):

    # Download page
    # logging.info('Checking [Myself-bbs] ' + title + '[' + str(episode) + '] : ' + url)
    res = requests.get(anime.url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get episode number from page
    episodeElems = soup.select('.z a:nth-of-type(5)')
    if episodeElems == []:
        logging.warning('Could not find episode elements')
        return
    logging.info(episodeElems[0].getText())
    episodeNumText = re.search('\d+', episodeElems[0].getText())
    if episodeNumText == None:
        logging.warning('Could not find episodeNumText')
        return
    episodeNum = int(episodeNumText.group(0))
    logging.info('Found episode ' + str(episodeNum))

    # Check whether the anime has been updated.
    if episodeNum > anime.episode:
        print('[動畫] ' + anime.name + ' 更新了第 ' + str(episodeNum) + ' 集了！')
        # Update episode num
        anime.episode = episodeNum
        return True

    return False
