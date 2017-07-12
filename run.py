#!./venv/bin/python
# coding: utf8

###########################################################
#
#  run.py
#
#  by Eason Chang <eason@easonchang.com>
#
#  A python script to automatically check whether my favorite animes
#  have updated and then send me an email to notify me.
#
#  This script does a one-time check.
#  This script should be set as a scheduled job by using crontab.
#
###########################################################

# my own modules
from modules.anigamer import anigamer
from modules.myselfbbs import myselfbbs
from modules.db.load import loadAnimes, loadComics


animes = loadAnimes()
comics = loadComics()

for anime in animes:
    if anime['site'] == 'anigamer':
        anigamer.check(anime, animes, comics)
    elif anime['site'] == 'myselfbbs':
        myselfbbs.check(anime, animes, comics)


