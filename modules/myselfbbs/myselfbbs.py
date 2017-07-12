# coding: utf8

#####################################################
#
#  myselfbbs/myselfbbs.py
#
#  by Eason Chang
#
#  解析MyselfBBS網站資料
#
#
#####################################################

import requests, bs4, re, os
from ..db.update import update
from ..myEmail.email import sendEmail
from copy import deepcopy

MYSELFBBS_LIST_URL = 'http://myself-bbs.com/forum-133-1.html'
MYSELFBBS_URL = 'http://myself-bbs.com/'


def fetchAll():

    webListUrl = MYSELFBBS_LIST_URL
    animes = []
    while True: # Loop through each list pages

        # Get page
        res = requests.get(webListUrl)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        animeElems = soup.select('.ml li')
        for animeElem in animeElems:
            listUrl = MYSELFBBS_URL + animeElem.select('.c a')[0].get('href')
            name = animeElem.select('h3 a')[0].getText() 
            imageUrl = MYSELFBBS_URL + animeElem.find('img').get('src')
            
            # Download image
            try:
                imageSrc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images', '%s.jpg' % (name.replace('/', '-')))
                res = requests.get(imageUrl)
                imageFile = open(imageSrc, 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
            except requests.exceptions.MissingSchema:
                print("Can't find image: %s" % name)
            
            # Get correct volume number and watch url
            volumeMo = re.search('\d+', animeElem.select('.ep_info')[0].getText())
            if volumeMo != None:
                # not 即將上映
                anime = {'listUrl': listUrl,
                         'name': name,
                         'volume': 0,
                         'watchUrl': ''
                        }
                fetchAnime = fetch(anime)
                watchUrl = fetchAnime['watchUrl']
                volume = fetchAnime['volume']
            else:
                volume = 0
                watchUrl = listUrl


            animes.append({'watchUrl': watchUrl,
                           'listUrl': listUrl,
                           'imageUrl': imageUrl,
                           'name': name,
                           'volume': volume,
                           'imageSrc': imageSrc
                            })
        nextButton = soup.select('.nxt')
        if nextButton == []:
            break
        else:
            webListUrl = MYSELFBBS_URL + nextButton[0].get('href')

    return animes

SRC_CLOUD = 0
SRC_BILI = 1
SRC_DM = 2
SRC_YOUKU = 3
SRC_IQUYI = 4
SRC_BACKUP = 5
SRC_HOONE = 6
SRC_NONE = 10

def fetch(anime):
    # Get page
    res = requests.get(anime['listUrl'])
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    volumeElems = soup.select('.main_list > li')
    volumeElem = soup.select('.main_list > li:nth-of-type(%s)' % len(volumeElems))[0]
    try:
        volume = int(re.search('\d+', volumeElem.select('a')[0].getText()).group(0))
    except AttributeError:
        print('Something wrong when fetch myselfbbs anime %s' % anime['name'])
        volume = 0
    if volume > anime['volume']:
        # 篩選最好的片源點
        sourceElems = volumeElem.select('ul a')
        bestSrc = SRC_NONE # 沒有對應到任何片源點
        bestWatchUrl = ''

        for sourceElem in sourceElems:
            source = sourceElem.getText()
            if source == '雲端':
                bestSrc = SRC_CLOUD
                bestWatchUrl = sourceElem.get('data-href')
                break
            elif source == 'B站' and bestSrc > SRC_BILI:
                bestSrc = SRC_BILI
                bestWatchUrl = sourceElem.get('data-href')
            elif source == 'DM' and bestSrc > SRC_DM:
                bestSrc = SRC_DM
                bestWatchUrl = sourceElem.get('data-href')
            elif source == '優酷' and bestSrc > SRC_YOUKU:
                bestSrc = SRC_YOUKU
                bestWatchUrl = sourceElem.get('data-href')
            elif source == '愛奇' and bestSrc > SRC_IQUYI:
                bestSrc = SRC_IQUYI
                bestWatchUrl = anime['listUrl']
            elif source == '備點' and bestSrc > SRC_BACKUP:
                bestSrc = SRC_BACKUP
                bestWatchUrl = anime['listUrl']
            elif source == '合壹' and bestSrc > SRC_HOONE:
                bestSrc = SRC_HOONE
                bestWatchUrl = anime['listUrl']

        if bestSrc != SRC_NONE: # 有找到可以看的片源點
            fetchAnime = deepcopy(anime)
            fetchAnime['watchUrl'] = bestWatchUrl
            fetchAnime['volume'] = volume
            return fetchAnime

    return anime # 沒有更新或沒找到可看的片源點，返回原本的anime


def check(anime, animes, comics):
    print('Check [MyselfBBS]%s[%d]...' % (anime['name'], anime['volume']))
    fetchAnime = fetch(anime)
    if fetchAnime['volume'] > anime['volume']:
        anime['volume'] = fetchAnime['volume']
        anime['watchUrl'] = fetchAnime['watchUrl']
        print('[動畫] %s 更新了第 %d 集!' % (anime['name'], anime['volume']))
        sendEmail(anime, animes, comics)
        update(anime)

