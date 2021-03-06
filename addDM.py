#!/usr/bin/python3
# coding: utf8

from os import path
from main import loadFile, updateFile
import re
from packages.model.anime import Anime
from packages.model.manga import Manga
from packages.model.DMBase import SiteType, StatusType
from packages.crawler.myselfbbs import MyselfBBSCrawler
from packages.crawler.cartoonmad import CartoonMadCrawler
from packages.crawler.bilibili import BilibiliCrawler


def generateDMModel(url):
    DM = None
    if "myself-bbs.com" in url:
        DM = Anime()
        DM.url = url
        DM.site = SiteType.MYSELFBBS
        crawler = MyselfBBSCrawler(url)
        DM.name = crawler.parseName()
        DM.episode = crawler.parseEpisode()
        DM.status = StatusType.SERIALING
    elif "cartoonmad.com" in url:
        DM = Manga()
        DM.url = url
        DM.site = SiteType.CARTOONMAD
        crawler = CartoonMadCrawler(url)
        DM.name = crawler.parseName()
        DM.episode = crawler.parseEpisode()
        DM.status = StatusType.SERIALING
    elif "bilibili.com" in url:
        DM = Anime()
        DM.url = url
        DM.site = SiteType.BILIBILI
        crawler = BilibiliCrawler(url)
        DM.name = crawler.parseName()
        DM.episode = crawler.parseEpisode()
        DM.status = StatusType.SERIALING
    return DM


def main():

    filePath = path.join(path.dirname(__file__), 'storage.json')
    DMs = loadFile(filePath)
    numDMBefore = len(DMs)

    print("addDM.py")
    print("===============")
    print("Import your favorite DM to anime-god")
    print("Type 'save' to apply changes")
    print("Or press Ctrl-c to exit\n")
    try:
        while True:

            print("---------------")
            print("Enter URL to import DM: ")
            buf = input()

            if buf == "save":
                updateFile(filePath, DMs)
                print("All changes saved")
                print("Now you have %d entries" % len(DMs))
                break

            if buf == "exit":
                print("Exit without apply changes")
                print("You still have %d entries" % numDMBefore)
                break

            urlPattern = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+"
            result = re.search(urlPattern, buf)
            if result is None:
                print("Not a valid URL")
                continue
            url = result.group(0)

            hasExist = False
            for DM in DMs:
                if url == DM.url:
                    print("%s 已經在資料庫中了" % DM.name)
                    hasExist = True
                    break
            if hasExist:
                continue

            DM = generateDMModel(url)
            if DM is None:
                print("Currently not support this website")
                continue

            print("")
            DM.printDetail()

            DMs.append(DM)

    except KeyboardInterrupt:
        print("Exit with key interrupt")
        pass

    print("Done!")
    # End main()


if __name__ == '__main__':
    main()
