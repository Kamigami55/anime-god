import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), 'data.db')

def update(anime):
    conn = sqlite3.connect(DB)
    conn.execute('UPDATE ANIME set VOLUME=? WHERE ID=?', (anime['volume'], anime['id']))
    conn.execute('UPDATE ANIME set WATCH_URL=? WHERE ID=?', (anime['watchUrl'], anime['id']))
    conn.commit()
    conn.close()
    print('Updated anime %s[%d]: %s' % (anime['name'], anime['volume'], anime['watchUrl']))

