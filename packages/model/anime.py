# coding: utf8

from .DMBase import DMBase, DMType, SiteType
from ..crawler.myselfbbs import MyselfBBSCrawler
from ..crawler.bilibili import BilibiliCrawler


class Anime(DMBase):

    def __init__(self):
        super().__init__()
        self.dmType = DMType.ANIME

    def checkUpdate(self):
        crawler = None

        if self.site == SiteType.MYSELFBBS:
            crawler = MyselfBBSCrawler()
        elif self.site == SiteType.BILIBILI:
            crawler = BilibiliCrawler()

        crawler.downloadPage(self.url)
        episode = crawler.parseEpisode()

        if episode > self.episode:
            # This anime has been updated
            self.episode = episode
            print('[動畫] ' + self.name + ' 更新了第 ' + str(self.episode) + ' 集了！')
            return True
        else:
            return False

    def sendMail(self, mailClient):
        # Email me
        subject = '追劇神：[動畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！'
        content = '[動畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！\n戳我觀看：' + self.url
        mailClient.send(subject, content)
