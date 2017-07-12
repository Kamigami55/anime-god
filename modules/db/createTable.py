import sqlite3, os
from ..anigamer import anigamer
from ..myselfbbs import myselfbbs

DB = os.path.join(os.path.dirname(__file__), 'data.db')


def createTable():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE ANIME (
        ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
        NAME        CHAR(50)    NOT NULL,
        VOLUME      INTEGER     NOT NULL,
        SITE        CHAR(50)    NOT NULL,
        LIST_URL    CHAR(150)           ,
        WATCH_URL   CHAR(150)           ,
        IMG_URL     CHAR(150)           ,
        IMG_SRC     CHAR(150)           ,
        ENDED       BOOLEAN 
        );''')
    conn.execute('''CREATE TABLE COMIC (
        ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
        NAME        CHAR(50)    NOT NULL,
        VOLUME      INTEGER     NOT NULL,
        SITE        CHAR(50)    NOT NULL,
        LIST_URL    CHAR(150)           ,
        WATCH_URL   CHAR(150)           ,
        IMG_URL     CHAR(150)           ,
        IMG_SRC     CHAR(150)           ,
        ENDED       BOOLEAN             
        );''')
    conn.close()
    print('Table created')


def importAnigamer():
    animes = anigamer.fetchAll()
    conn = sqlite3.connect(DB)

    for anime in animes:
        conn.execute('''INSERT INTO ANIME
        (NAME, VOLUME, SITE, LIST_URL, WATCH_URL, IMG_URL, IMG_SRC, ENDED) VALUES
        ('%s', %d, '%s', '%s', '%s', '%s', '%s', %d)
        ''' % (anime['name'], anime['volume'], 'anigamer', 'https://ani.gamer.com.tw/', anime['watchUrl'], anime['imageUrl'], anime['imageSrc'], 0))

    conn.commit()
    conn.close()
    print('Succesfully import %d animes from AniGamer' % len(animes))


def importMyselfbbs():
    animes = myselfbbs.fetchAll()
    conn = sqlite3.connect(DB)

    for anime in animes:
        conn.execute('''INSERT INTO ANIME
        (NAME, VOLUME, SITE, LIST_URL, WATCH_URL, IMG_URL, IMG_SRC, ENDED) VALUES
        ('%s', %d, '%s', '%s', '%s', '%s', '%s', %d)
        ''' % (anime['name'], anime['volume'], 'myselfbbs', anime['listUrl'], anime['watchUrl'], anime['imageUrl'], anime['imageSrc'], 0))

    conn.commit()
    conn.close()
    print('Succesfully import %d animes from MyselfBBS' % len(animes))


def importData():
    importAnigamer()
    importMyselfbbs()
    print('Succesfully import all data')

