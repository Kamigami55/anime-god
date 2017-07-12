import sqlite3, os

#DB = os.path.join(os.path.dirname(__file__), 'data.db')
DB = os.path.join(os.path.dirname(__file__), '..', '..', 'anigod', 'db.sqlite3')
#ANIME_TABLE_NAME = 'ANIME'
#COMIC_TABLE_NAME = 'COMIC'
ANIME_TABLE_NAME = 'SUBS_ANIME'
COMIC_TABLE_NAME = 'SUBS_COMIC'


def loadAnimes():
    conn = sqlite3.connect(DB)
    cursor = conn.execute('SELECT ID, NAME, VOLUME, SITE, LIST_URL, WATCH_URL, IMG_URL, IMG_SRC, SUBSCRIBE, ENDED FROM %s' % ANIME_TABLE_NAME)
    animes = []
    for row in cursor:
        id = row[0]
        name = row[1]
        volume = row[2]
        site = row[3]
        listUrl = row[4]
        watchUrl = row[5]
        imgUrl = row[6]
        imgSrc = row[7]
        subscribe = row[8]
        ended = row[9]
        animes.append({
            'id': id,
            'name': name,
            'volume': volume,
            'site': site,
            'listUrl': listUrl,
            'watchUrl': watchUrl,
            'imgUrl': imgUrl,
            'imgSrc': imgSrc,
            'subscribe': subscribe,
            'ended': ended
            })
    conn.close()
    return animes


def loadComics():
    conn = sqlite3.connect(DB)
    cursor = conn.execute('SELECT ID, NAME, VOLUME, SITE, LIST_URL, WATCH_URL, IMG_URL, IMG_SRC, SUBSCRIBE, ENDED FROM %s' % COMIC_TABLE_NAME)
    comics = []
    for row in cursor:
        id = row[0]
        name = row[1]
        volume = row[2]
        site = row[3]
        listUrl = row[4]
        watchUrl = row[5]
        imgUrl = row[6]
        imgSrc = row[7]
        subscribe = row[8]
        ended = row[9]
        comics.append({
            'id': id,
            'name': name,
            'volume': volume,
            'site': site,
            'listUrl': listUrl,
            'watchUrl': watchUrl,
            'imgUrl': imgUrl,
            'imgSrc': imgSrc,
            'subscribe': subscribe,
            'ended': ended
            })
    conn.close()
    return comics


def printTable():
    animes = loadAnimes()
    comics = loadComics()
    print('======== Animes ========')
    for anime in animes:
        print('id: ' + str(anime['id']))
        print('name: ' + anime['name'])
        print('volume: ' + str(anime['volume']))
        print('site: ' + anime['site'])
        print('listUrl: ' + anime['listUrl'])
        print('watchUrl: ' + anime['watchUrl'])
        print('imgUrl: ' + anime['imgUrl'])
        print('imgSrc: ' + anime['imgSrc'])
        print('subscribe: ' + str(anime['subscribe']))
        print('ended: ' + str(anime['ended']))
        print('========================')
    print('Anime count: ' + str(len(animes)))

    print('\n======== Comics ========')
    for comic in comics:
        print('id: ' + str(comic['id']))
        print('name: ' + comic['name'])
        print('volume: ' + str(comic['volume']))
        print('site: ' + comic['site'])
        print('listUrl: ' + comic['listUrl'])
        print('watchUrl: ' + comic['watchUrl'])
        print('imgUrl: ' + comic['imgUrl'])
        print('imgSrc: ' + comic['imgSrc'])
        print('subscribe: ' + str(anime['subscribe']))
        print('ended: ' + str(comic['ended']))
        print('========================')
    print('Comic count: ' + str(len(comics)))

