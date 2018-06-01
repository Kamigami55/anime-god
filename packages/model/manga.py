# coding: utf8

from .DMBase import DMBase, StatusType, DMType, SiteType
from ..crawler.cartoonmad import checkCartoonMad
from ..gmail.mailClient import MailClient


class Manga(DMBase):

    def __init__(self):
        super().__init__()
        self.dmType = DMType.MANGA

    def check(self):
        result = False

        if self.site == SiteType.CARTOONMAD:
            result = checkCartoonMad(self)

        return result

    def sendMail(self, mailClient):
        # Email me
        subject = '追劇神：[漫畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！'
        content = '[漫畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！\n戳我觀看：' + self.url
        mailClient.send(subject, content)
