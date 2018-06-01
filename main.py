#!/usr/bin/python3
# coding: utf8

###########################################################
#
#  anime-checker.py
#
#  by Eason Chang <eason@easonchang.com>
#
#  A python script to automatically check whether my favorite animes
#  have updated and then send me an email to notify me.
#
#  This script does a one-time check.
#  This script should be set as a scheduled job by using crontab.
#
#  Contains 2 config files:
#   - .env        : stores environment variables of my email addresses and
#                   password.
#   - animes.json : stores a list of my favorite animes, including title,
#                   website url, and current episode number.
#
###########################################################

import logging
import jsonpickle
from os import path
from packages.gmail.mailClient import MailClient
from packages.model.anime import Anime
from packages.model.manga import Manga
from packages.model.DMBase import DMType, StatusType, SiteType


# Set logging config
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
# Disable logging
logging.disable(logging.CRITICAL)

# A flag whether there is an anime update during this one-time check
hasDMUpdated = False
DMs = None
filePath = path.join(path.dirname(__file__), 'storage.json')
mailClient = MailClient()


def loadDMs():
    global filePath
    global DMs
    # Load list of my favorite animes from ./storage.json
    file = open(filePath, 'r')
    fileContent = file.read()
    file.close()
    DMs = jsonpickle.decode(fileContent)
    # animes = json.loads(fileContent)


def performCheck():
    global hasDMUpdated
    global DMs
    global mailClient

    for i in range(len(DMs)):
        DM = DMs[i]
        if DM.check():
            # this DM has updated
            # send email
            DM.sendMail(mailClient)
            # set flag to true
            hasDMUpdated = True

    # Loop through each anime in my animes list
    # for i in range(len(animes['animes'])):
        # anime = animes['animes'][i]
        # if anime['site'] == 'myself-bbs':
            # checkMyselfBBS(anime, i)

    # # Loop through each comic in my comics list
    # for i in range(len(animes['comics'])):
        # comic = animes['comics'][i]
        # if comic['site'] == 'cartoonmad':
            # checkCartoonMad(comic, i)


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
    loadDMs()
    performCheck()
    if hasDMUpdated:
        updateFile()
        print('File updated')
    else:
        print('新番尚未更新哦')


if __name__ == '__main__':
    main()
