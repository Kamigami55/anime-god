#!./venv/bin/python
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
from email.mime.image import MIMEImage

# Set logging config
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
#logging.disable(logging.CRITICAL) # Disable logging

# Load my email addresses and password from ./.env
load_dotenv(path.join(path.dirname(__file__), '.env'))
SENDER_EMAIL = environ.get('SENDER_EMAIL')
SENDER_PASSWORD = environ.get('SENDER_PASSWORD')
RECEIVER_EMAILS = environ.get('RECEIVER_EMAILS')

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
def sendEmailToMyself(subject, content, hasImage=False, url='', index='0'):
    global animes
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(SENDER_EMAIL, SENDER_PASSWORD)

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = SENDER_EMAIL
    msgRoot['To'] = RECEIVER_EMAILS
    
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # Add content
    content = content + "<a href='" + url + "'><img src='cid:image" + index + "'></a><br/><br/>===============================<br/>目前追蹤清單：<br/><br/>-------- 動畫 --------<br/>"
    for anime in animes['animes']:
        if anime['finished']:
            status = '已完結'
        else:
            status = '連載中'
        content = content + '<a href="' + anime['url'] + '">[' + status + '] ' + anime['title'] + '【' + str(anime['episode']) + '】</a><br/>'
    content = content + "<br/>-------- 漫畫 --------<br/>"
    for comic in animes['comics']:
        if comic['finished']:
            status = '已完結'
        else:
            status = '連載中'
        content = content + '<a href="' + comic['url'] + '">[' + status + '] ' + comic['title'] + '【' + str(comic['episode']) + '】</a><br/>'

    msgAlternative.attach(MIMEText(content.encode('utf-8'), 'html', 'utf-8'))

    # Add image
    if hasImage:
        with open(path.join(path.dirname(__file__), 'image.jpg'), 'rb') as fp:
            msgImage = MIMEImage(fp.read())
        msgImage.add_header('Content-ID', '<image' + index + '>')
        msgRoot.attach(msgImage)

    smtpObj.send_message(msgRoot)
    smtpObj.quit()
    print('Email sent')


# Check animes on Myself-bbs
def checkMyselfBBS(anime, index):
    global animes
    global hasAnimeUpdated
    title = anime['title']
    url = anime['url']
    episode = anime['episode']

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
    episodeNumText = re.search('【更新至第 (\d+)', episodeElems[0].getText())
    if episodeNumText == None:
        logging.warning('Could not find episodeNumText')
        return
    episodeNum = int(episodeNumText.group(1))
    logging.info('Found episode ' + str(episodeNum))
    episodeStatus = re.search('【全', episodeElems[0].getText())
    if episodeStatus != None:
        hasEnded = True
        logging.info('已完結')
    else:
        hasEnded = False
        logging.info('連載中')

    # Check whether the anime has been updated.
    if episodeNum > episode:
        print('[動畫] ' + title + ' 更新了第 ' + str(episodeNum) + ' 集了！')
        # Update episode status
        hasAnimeUpdated = True
        animes['animes'][index]['episode'] = episodeNum
        if hasEnded:
            print('[動畫] ' + title + ' 已完結！！！')
            animes['animes'][index]['finished'] = True
        # Download anime image for email
        imgElem = soup.select('.info_img_box img')
        if imgElem == []:
            logging.warning('Could not find image elem')
            hasImage = False
        else:
            imgUrl = imgElem[0].get('src')
            res = requests.get(imgUrl)
            imageFile = open(path.join(path.dirname(__file__), 'image.jpg'), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            hasImage = True


        # Email me
        subject = '追劇神：[動畫] ' + title + ' 更新了第【' + str(episodeNum) + '】集！'
        content = '[動畫] ' + title + ' 更新了第【' + str(episodeNum) + '】集！<br/><br/>戳我觀看：' + url + '<br/><br/>'
        sendEmailToMyself(subject, content, hasImage, url, str(index))
        # TODO: Download episode video for me


# Check comics on CartoonMad
def checkCartoonMad(comic, index):
    global animes
    global hasAnimeUpdated
    title = comic['title']
    url = comic['url']
    episode = comic['episode']

    # Download page
    logging.info('Checking [CartoonMad] ' + title + '[' + str(episode) + '] : ' + url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    
    # Get episode number from page
    # Only works for serializing comics
    # TODO: Fix it
    episodeElemImg = soup.find("img", src='/image/chap1.gif')
    if episodeElemImg == None:
        logging.warning('Could not find episode element img')
        return
    rx_blanks=re.compile(r"\s+")
    episodeNumText = rx_blanks.sub("", episodeElemImg.parent.contents[2].getText())
    episodeNumMatch = re.search('~(\d+)', episodeNumText)
    if episodeNumMatch == None:
        logging.warning('Could not find episodeNumText')
        return
    episodeNum = int(episodeNumMatch.group(1))
    logging.info('Found episode ' + str(episodeNum))

    # Check whether the anime has been updated.
    if episodeNum > episode:
        print('[漫畫] ' + title + ' 更新了第 ' + str(episodeNum) + ' 集了！')
        # Update episode num
        animes['comics'][index]['episode'] = episodeNum
        hasAnimeUpdated = True
        # Email me
        subject = '追劇神：[漫畫] ' + title + ' 更新了第【' + str(episodeNum) + '】集！'
        content = '[漫畫] ' + title + ' 更新了第【' + str(episodeNum) + '】集！\n戳我觀看：' + url
        sendEmailToMyself(subject, content, False)
        # TODO: Download this comic for me



# Loop through each anime in my animes list
for i in range(len(animes['animes'])):
    anime = animes['animes'][i]
    if anime['site'] == 'myself-bbs':
        checkMyselfBBS(anime, i)

# Loop through each comic in my comics list
for i in range(len(animes['comics'])):
    comic = animes['comics'][i]
    if comic['site'] == 'cartoonmad':
        checkCartoonMad(comic, i)


# If there is an anime update, then update episode numbers to ./animes.json
if hasAnimeUpdated:
    fileContent = json.dumps(animes, indent=4, ensure_ascii=False)
    file = open(jsonPath, 'w')
    file.write(fileContent)
    file.close()
    print('File updated')
else:
    print('新番尚未更新哦')

