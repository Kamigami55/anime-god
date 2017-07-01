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

import requests, bs4, re, logging, smtplib, json
from os import path, environ
from dotenv import load_dotenv
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set logging config
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logging.disable(logging.CRITICAL) # Disable logging

# Load my email addresses and password from ./.env
load_dotenv(path.join(path.dirname(__file__), '.env'))
SENDER_EMAIL = environ.get('SENDER_EMAIL')
SENDER_PASSWORD = environ.get('SENDER_PASSWORD')
RECEIVER_EMAIL = environ.get('RECEIVER_EMAIL')

hasAnimeUpdated = False     # A flag whether there is an anime update during this one-time check

# Load list of my favorite animes from ./animes.json
jsonPath = path.join(path.dirname(__file__), 'animes.json')
file = open(jsonPath, 'r')
fileContent = file.read()
file.close()
animes = json.loads(fileContent)


# Functions to generate email message string
def contains_non_ascii_characters(str):
    return not all(ord(c) < 128 for c in str)   
def add_header(message, header_name, header_value):
    if contains_non_ascii_characters(header_value):
        h = Header(header_value, 'utf-8')
        message[header_name] = h
    else:
        message[header_name] = header_value    
    return message

# Send email to myself
def sendEmailToMyself(subject, content):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(SENDER_EMAIL, SENDER_PASSWORD)

    # Generate email message string
    msg = MIMEMultipart('alternative')
    msg = add_header(msg, 'Subject', subject)
    if(contains_non_ascii_characters(content)):
        plain_text = MIMEText(content.encode('utf-8'),'plain','utf-8') 
    else:
        plain_text = MIMEText(content,'plain')
    msg.attach(plain_text)

    smtpObj.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, str(msg))
    smtpObj.quit()
    print('Email sent')


# Check animes on Myself-bbs
def checkMyselfBBS(title, url, episode, index):
    global animes
    global hasAnimeUpdated

    # Download page
    logging.info('Checking [Myself-bbs] ' + title + '[' + str(episode) + '] : ' + url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    
    # Get episode number from page
    episodeElems = soup.select('.z a:nth-of-type(5)')
    if episodeElems == []:
        logging.warning('Could not find episode elements')
        return
    logging.info(episodeElems[0].getText())
    episodeNumText = re.search('\d+', episodeElems[0].getText())
    if episodeNumText == None:
        logging.warning('Could not find episodeNumText')
        return
    episodeNum = int(episodeNumText.group(0))
    logging.info('Found episode ' + str(episodeNum))

    # Check whether the anime has been updated.
    if episodeNum > episode:
        print(title + ' 更新了第 ' + str(episodeNum) + ' 集了！')
        # Update episode num
        animes['animes'][index]['episode'] = episodeNum
        hasAnimeUpdated = True
        # Email me
        subject = '追劇神：' + title + ' 更新了第【' + str(episodeNum) + '】集！'
        content = title + ' 更新了第【' + str(episodeNum) + '】集！\n戳我觀看：' + url
        sendEmailToMyself(subject, content)
        # TODO: Download episode video for me


# Loop through each anime in my animes list
for i in range(len(animes['animes'])):
    anime = animes['animes'][i]
    if anime['site'] == 'myself-bbs':
        checkMyselfBBS(anime['title'], anime['url'], anime['episode'], i)


# If there is an anime update, then update episode numbers to ./animes.json
if hasAnimeUpdated:
    fileContent = json.dumps(animes, indent=4, ensure_ascii=False)
    file = open(jsonPath, 'w')
    file.write(fileContent)
    file.close()
    print('File updated')
else:
    print('新番尚未更新哦')

