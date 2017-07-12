import sqlite3, os

#DB = os.path.join(os.path.dirname(__file__), 'data.db')
DB = os.path.join(os.path.dirname(__file__), '..', '..', 'anigod', 'db.sqlite3')
#ANIME_TABLE_NAME = 'ANIME'
#COMIC_TABLE_NAME = 'COMIC'
ANIME_TABLE_NAME = 'SUBS_ANIME'
COMIC_TABLE_NAME = 'SUBS_COMIC'


def update(anime):
    conn = sqlite3.connect(DB)
    conn.execute('UPDATE %s set VOLUME=%d WHERE ID=%d' % (ANIME_TABLE_NAME, anime['volume'], anime['id']))
    conn.execute('UPDATE %s set WATCH_URL="%s" WHERE ID=%d' % (ANIME_TABLE_NAME, anime['watchUrl'], anime['id']))
    conn.commit()
    conn.close()
    print('Updated anime %s[%d]: %s' % (anime['name'], anime['volume'], anime['watchUrl']))

