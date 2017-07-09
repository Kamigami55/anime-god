# coding: utf8

import smtplib
from os import path, environ
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# Load my email addresses and password from ./.mails
load_dotenv(path.join(path.dirname(__file__), '.emails'))
SENDER_EMAIL = environ.get('SENDER_EMAIL')
SENDER_PASSWORD = environ.get('SENDER_PASSWORD')
#RECEIVER_EMAILS = environ.get('RECEIVER_EMAILS')
RECEIVER_EMAILS = 'samkami@icloud.com'


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


def sendEmailWithOneImage(subject, content, imgSource):

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = SENDER_EMAIL
    msgRoot['To'] = RECEIVER_EMAILS
    
    # Attach content
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgAlternative.attach(MIMEText(content.encode('utf-8'), 'html', 'utf-8'))

    # Attach image
    fp = open(imgSource, 'rb')
    msgImage = MIMEImage(fp.read())
    msgImage.add_header('Content-ID', '<image%s>' % (path.basename(imgSource)))
    msgRoot.attach(msgImage)

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(SENDER_EMAIL, SENDER_PASSWORD)
    smtpObj.send_message(msgRoot)
    smtpObj.quit()


def generateSubList(animes, comics):
    # Add content
    content = '''
        <br/>
        <br/>
        ===============================<br/>
        目前追蹤清單：<br/>
        <br/>
        -------- 動畫 --------<br/>
        '''
    for elem in animes:
        if elem['ended']:
            status = '已完結'
        else:
            status = '連載中'
        content += '<a href="%s">[%s] %s【%d】</a><br/>' % (elem['watchUrl'], status, elem['name'], elem['volume'])
    content += '''
        <br/>
        -------- 漫畫 --------<br/>
        '''
    for elem in comics:
        if elem['ended']:
            status = '已完結'
        else:
            status = '連載中'
        content += '<a href="%s">[%s] %s【%d】</a><br/>' % (elem['watchUrl'], status, elem['name'], elem['volume'])

    return content


def generateSubject(elem):
    subject = '追劇神：%s 更新了第【%d】集！' % (elem['name'], elem['volume'])
    return subject


def generateContent(elem, animes, comics):
    content = '%s 更新了第【%d】集了！<br/><br/>戳我觀看：%s' % (elem['name'], elem['volume'], elem['watchUrl'])
    content += '<br/><br/><a href="%s"><img src="cid:image%s"></a>' % (elem['watchUrl'], path.basename(elem['imgSrc']))
    content += generateSubList(animes, comics)
    return content


# MAIN FUNCTION
def sendEmail(elem, animes, comics):
    subject = generateSubject(elem)
    content = generateContent(elem, animes, comics)
    sendEmailWithOneImage(subject, content, elem['imgSrc'])
    print('Email sent')

