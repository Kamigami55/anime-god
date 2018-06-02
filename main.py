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


# Set logging config
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
# Disable logging
logging.disable(logging.CRITICAL)

mailClient = MailClient()


def loadFile(filePath):
    # Load list of my favorite animes from ./storage.json
    file = open(filePath, 'r')
    fileContent = file.read()
    file.close()
    content = jsonpickle.decode(fileContent)
    return content


def performCheck(DMs):
    hasDMUpdated = False
    global mailClient

    for i in range(len(DMs)):
        DM = DMs[i]
        if DM.checkUpdate():
            # this DM has been updated

            # send email
            DM.sendMail(mailClient)
            # set flag to true
            hasDMUpdated = True

    return hasDMUpdated


def updateFile(filePath, content):
    # Update episode numbers to ./storage.json

    jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    jsonpickle.set_encoder_options('demjson', sort_keys=True, indent=4)

    fileContent = jsonpickle.encode(content)
    # fileContent = json.dumps(animes, indent=4, ensure_ascii=False)
    file = open(filePath, 'w')
    file.write(fileContent)
    file.close()


def main():

    DMs = None
    filePath = path.join(path.dirname(__file__), 'storage.json')

    DMs = loadFile(filePath)

    hasDMUpdated = performCheck(DMs)

    if hasDMUpdated:
        updateFile(filePath, DMs)
        print('File updated')
    else:
        print('新番尚未更新哦')


if __name__ == '__main__':
    main()
