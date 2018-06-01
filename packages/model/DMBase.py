# coding: utf8

from enum import Enum


class StatusType(Enum):
    UNKNOWN = "未知"
    FINISHED = "完結"
    SERIALING = "連載"


class DMType(Enum):
    UNKNOWN = "未知"
    ANIME = "動畫"
    MANGA = "漫畫"


class SiteType(Enum):
    UNKNOWN = "unknown"
    # Anime sites
    MYSELFBBS = "myself-bbs"
    # Manga sites
    CARTOONMAD = "cartoon-mad"


class DMBase:

    def __init__(self):
        self.name = ''
        self.episode = ''
        self.site = SiteType.UNKNOWN
        self.status = StatusType.UNKNOWN
        self.url = ''
        self.dmType = DMType.UNKNOWN

    def __str__(self):
        return "[%s %s] %s (%d)" % (self.status.value,
                                    self.dmType,
                                    self.name,
                                    self.episode)
