# coding: utf8

#####################################################
#
#  anigamer/anigamer.py
#
#  by Eason Chang
#
#  解析巴哈姆特動畫瘋網站資料
#  https://ani.gamer.com.tw/
#
#
#####################################################

import requests, bs4, re, os, sys
from ..db.update import update
from ..myEmail.email import sendEmail

ANIGAMER_URL = 'https://ani.gamer.com.tw/'


def fetchAll():
    # Get page
    res = requests.get(ANIGAMER_URL)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    animeElems = soup.select('.index_season')[0].select('.newanime')
    animes = []
    for animeElem in animeElems:
        watchUrl = animeElem.select('.newanime__content')[0].get('href')
        name = animeElem.select('.newanime-title')[0].getText()
        volume = int(re.search('\d+', animeElem.select('.newanime-vol')[0].getText()).group(0))
        imageUrl = animeElem.find('img').get('data-src')

        # Download image
        try:
            imageSrc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images', '%s.jpg' % (name))
            res = requests.get(imageUrl)
            imageFile = open(imageSrc, 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        except requests.exceptions.MissingSchema:
            print("Can't find image: %s" % name)

        animes.append({'watchUrl': watchUrl,
                       'imageUrl': imageUrl,
                       'name': name,
                       'volume': volume,
                       'imageSrc': imageSrc
                        })
    return animes


def fetch(fetchName):
    # Get page
    res = requests.get(ANIGAMER_URL)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    animeElems = soup.select('.newanime')

    for animeElem in animeElems:
        name = animeElem.select('.newanime-title')[0].getText()
        if name == fetchName:
            watchUrl = animeElem.select('.newanime__content')[0].get('href')
            volume = int(re.search('\d+', animeElem.select('.newanime-vol')[0].getText()).group(0))
            imageUrl = animeElem.find('img').get('data-src')

            # Download image
            imageSrc = os.path.join(os.path.dirname(__file__), 'images', '%s.jpg' % (name))
            res = requests.get(imageUrl)
            imageFile = open(imageSrc, 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

            return {'watchUrl': watchUrl,
                    'imageUrl': imageUrl,
                    'name': name,
                    'volume': volume,
                    'imageSrc': imageSrc
                     }
    return None


def check(anime, animes, comics):
    print('Check [巴哈]%s...' % anime['name'])
    fetchAnime = fetch(anime['name'])
    if fetchAnime['volume'] > anime['volume']:
        anime['volume'] = fetchAnime['volume']
        anime['watchUrl'] = fetchAnime['watchUrl']
        print('[動畫] %s 更新了第 %d 集!' % (anime['name'], anime['volume']))
        sendEmail(anime, animes, comics)
        update(anime)
        
