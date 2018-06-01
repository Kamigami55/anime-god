#!/usr/bin/python3
# coding: utf8

import jsonpickle
from os import path
from packages.model.anime import Anime
from packages.model.manga import Manga
from packages.model.DMBase import DMType, StatusType, SiteType

DMs = []
filePath = path.join(path.dirname(__file__), 'storage.json')


def seedData():
    global DMs
    anime = Anime()
    anime.name = '我的英雄學院'
    anime.episode = 3
    anime.site = SiteType.MYSELFBBS
    anime.url = 'http://myself-bbs.com/thread-43679-1-1.html'
    anime.dmType = DMType.ANIME
    anime.status = StatusType.SERIALING
    DMs.append(anime)

    manga = Manga()
    manga.name = '我的英雄學院漫畫'
    manga.episode = 3
    manga.site = SiteType.CARTOONMAD
    manga.url = 'http://www.cartoonmad.com/comic/4085.html'
    manga.dmType = DMType.MANGA
    manga.status = StatusType.SERIALING
    DMs.append(manga)

def updateFile():
    # Update episode numbers to ./storage.json
    global filePath
    global DMs

    jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    jsonpickle.set_encoder_options('demjson', sort_keys=True, indent=4)

    fileContent = jsonpickle.encode(DMs)
    # fileContent = json.dumps(animes, indent=4, ensure_ascii=False)
    file = open(filePath, 'w')
    file.write(fileContent)
    file.close()


def main():
    seedData()
    updateFile()


if __name__ == '__main__':
    main()
