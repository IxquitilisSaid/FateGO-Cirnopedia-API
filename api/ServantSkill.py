import re

from bs4 import NavigableString, Tag

from api.Constants import *


class ServantSkill:
    class Effect:
        def __init__(self, effect):
            self.effect = effect
            self.demerit = False

    def __init__(self, navigator):
        navigator = navigator.find_next('td', class_='profile')
        self.image = CIRNOPEDIA_ROOT + '/' + navigator.a.img.attrs['src']

        navigator = navigator.find_next('td', class_='desc')
        self.name = navigator.spanh.text.rstrip()
        self.rankUp = False
        self.description = ''
        self.effects = []
        contentsList = navigator.contents
        for item in contentsList:
            if type(item) is NavigableString:
                result = re.search("\[(.+)\]", item)
                if result is not None:
                    self.description += result.group(1) + '\n'
                elif item.rstrip() is not "":
                    self.effects.append(self.Effect(item.rstrip()))
            if type(item) is Tag:
                if 'Demerit' in item.text:
                    self.effects[self.effects.__len__() - 1].demerit = True
                elif 'Rank Up Quest Power Up' in item:
                    self.rankUp = True
