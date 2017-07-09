#!./venv/bin/python

from random import randint
from modules.db.update import update
from modules.db.load import loadAnimes, loadComics

animes = loadAnimes()
comics = loadComics()

target = animes[randint(1, len(animes))]
print('Original: %s[%d] : %s' % (target['name'], target['volume'], target['watchUrl']))

target['volume'] -= 1
target['watchUrl'] = ''

print('Set to: %s[%d] : %s' % (target['name'], target['volume'], target['watchUrl']))

update(target)
