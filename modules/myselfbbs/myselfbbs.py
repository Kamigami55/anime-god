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
        sourceElems = volumeElem.select('ul a')
        for sourceElem in sourceElems:
            if sourceElem.getText() == '雲端':
                fetchAnime = deepcopy(anime)
                fetchAnime['watchUrl'] = sourceElem.get('data-href')
                fetchAnime['volume'] = volume
                return fetchAnime
    return anime


def check(anime, animes, comics):
    print('Check [MyselfBBS]%s[%d]...' % (anime['name'], anime['volume']))
    fetchAnime = fetch(anime)
    if fetchAnime['volume'] > anime['volume']:
        anime['volume'] = fetchAnime['volume']
        anime['watchUrl'] = fetchAnime['watchUrl']
        print('[動畫] %s 更新了第 %d 集!' % (anime['name'], anime['volume']))
        sendEmail(anime, animes, comics)
        update(anime)

