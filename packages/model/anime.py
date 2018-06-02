# coding: utf8

from .DMBase import DMBase, DMType, SiteType
from ..crawler.myselfbbs import MyselfBBSCrawler
# from ..gmail.mailClient import MailClient


class Anime(DMBase):

    def __init__(self):
        super().__init__()
        self.dmType = DMType.ANIME

    def check(self):
        result = False

        if self.site == SiteType.MYSELFBBS:
            crawler = MyselfBBSCrawler()
            result = crawler.check(self)
        # True / False
        return result

    def sendMail(self, mailClient):
        # Email me
        subject = '追劇神：[動畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！'
        content = '[動畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！\n戳我觀看：' + self.url
        mailClient.send(subject, content)
