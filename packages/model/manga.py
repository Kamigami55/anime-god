# coding: utf8

from .DMBase import DMBase, DMType, SiteType
from ..crawler.cartoonmad import CartoonMadCrawler


class Manga(DMBase):

    def __init__(self):
        super().__init__()
        self.dmType = DMType.MANGA

    def checkUpdate(self):
        crawler = None

        if self.site == SiteType.CARTOONMAD:
            crawler = CartoonMadCrawler()

        crawler.downloadPage(self.url)
        episode = crawler.parseEpisode()

        if episode > self.episode:
            # This manga has been updated
            self.episode = episode
            print('[漫畫] ' + self.name + ' 更新了第 ' + str(self.episode) + ' 集了！')
            return True
        else:
            return False

    def sendMail(self, mailClient):
        # Email me
        subject = '追劇神：[漫畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！'
        content = '[漫畫] ' + self.name + ' 更新了第【' + str(self.episode) + '】集！\n戳我觀看：' + self.url
        mailClient.send(subject, content)
