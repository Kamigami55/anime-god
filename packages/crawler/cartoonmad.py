# coding: utf8

import logging
import requests
import bs4
import re


def checkCartoonMad(manga):
    # Check comics on CartoonMad

    # Download page
    # logging.info('Checking [CartoonMad] ' + title + '[' + str(episode) + '] : ' + url)
    res = requests.get(manga.url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get episode number from page
    # Only works for serializing comics
    # TODO: Fix it
    episodeElemImg = soup.find("img", src='/image/chap1.gif')
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

    # Check whether the anime has been updated.
    if episodeNum > manga.episode:
        print('[漫畫] ' + manga.name + ' 更新了第 ' + str(episodeNum) + ' 集了！')
        # Update episode num
        manga.episode = episodeNum
        return True

    return False
