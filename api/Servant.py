import requests
import re
from bs4 import BeautifulSoup

from api.ServantClass import ServantClass


class Servant:
    def __init__(self, id):
        CIRNOPEDIA_ROOT = "http://fate-go.cirnopedia.org"
        CIRNOPEDIA_SERVANT_PAGE = CIRNOPEDIA_ROOT + "/servant_profile.php"

        self.raw = BeautifulSoup(requests.get(CIRNOPEDIA_SERVANT_PAGE, params={'servant' : id}).text, 'lxml')
        self.id = id
        navigator = self.raw.body.find('a', {'class': 'fancybox', 'rel': 'servant'})
        self.portraits = {}
        if navigator.attrs['title'] == "Gutentag Omen":
            self.portraits['chibi'] = CIRNOPEDIA_ROOT + '/' + navigator.attrs['href']
            navigator = navigator.find_next('a', {'class': 'fancybox', 'rel': 'servant'})
        self.portraits['base'] = CIRNOPEDIA_ROOT + '/' + navigator.attrs['href']
        navigator = navigator.find_next('a', {'class': 'fancybox', 'rel': 'servant'})
        self.portraits['ascension 1'] = CIRNOPEDIA_ROOT + '/' + navigator.attrs['href']
        navigator = navigator.find_next('a', {'class': 'fancybox', 'rel': 'servant'})
        self.portraits['ascension 2'] = CIRNOPEDIA_ROOT + '/' + navigator.attrs['href']
        navigator = navigator.find_next('a', {'class': 'fancybox', 'rel': 'servant'})
        self.portraits['ascension 3'] = CIRNOPEDIA_ROOT + '/' + navigator.attrs['href']

        navigator = navigator.find_next('td', class_='profile', text=re.compile('Name'))
        self.name = navigator.find_next('td', class_='desc').spanh.text.rstrip()
        navigator = navigator.find_next('tr').find_next('td', class_='desc')
        self.alias = navigator.a.text.rstrip().split(',')
        [x.strip() for x in self.alias]
        navigator = navigator.find_next('td', class_='desc')
        classAssigner = {
            "Shielder": ServantClass.SHIELDER,
            "Saber": ServantClass.SABER,
            "Lancer": ServantClass.LANCER,
            "Archer": ServantClass.ARCHER,
            "Caster": ServantClass.CASTER,
            "Rider": ServantClass.RIDER,
            "Assassin": ServantClass.ASSASSIN,
            "Berseker": ServantClass.BERSEKER,
            "Ruler": ServantClass.RULER,
            "Avenger": ServantClass.AVENGER,
            "Alterego": ServantClass.ALTEREGO,
            "Moon cancer": ServantClass.MOONCANCER,
            "Foreigner": ServantClass.FOREIGNER,
            "Beast": ServantClass.BEAST,
            "Beast I": ServantClass.BEAST,
            "Beast II": ServantClass.BEAST,
            "Beast III": ServantClass.BEAST,
            "Unknown": ServantClass.UNKNOWN,
        }
        self.class_ = classAssigner.get(navigator.text.rstrip(), ServantClass.UNKNOWN)
        navigator = navigator.find_next('td', class_='rare5 desc')
        self.rarity = int(navigator.text.count('★'))
        navigator = navigator.find_next('td', class_='desc')
        self.cost = int(navigator.text)
        navigator = navigator.find_next('td', class_='desc')
        self.maxLv = int(navigator.text)
        navigator = navigator.find_next('td', class_='desc')
        self.atk_1 = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        self.hp_1 = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        self.atk_90 = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        self.hp_90 = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        self.atk_100 = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        self.hp_100 = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        self.maxAtk = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        self.maxHp = int(navigator.text.replace(',',''))
        navigator = navigator.find_next('td', class_='desc')
        match = re.match("Attack: (\d+\.\d+)% ・ Defense: (\d+\.\d+)%", navigator.text)
        self.npGain = {'attack': float(match.group(1)), 'defense': float(match.group(2)) }
        navigator = navigator.find_next('td', class_='desc')
        self.hits = {}
        match = re.match("(\d+) Hits", navigator.text)
        self.hits['quick'] = int(match.group(1))
        navigator = navigator.find_next('td', class_='desc')
        self.starWeigth = int(navigator.text)
        navigator = navigator.find_next('td', class_='desc')
        match = re.match("(\d+) Hits", navigator.text)
        self.hits['arts'] = int(match.group(1))
        navigator = navigator.find_next('td', class_='desc')
        match = re.match("(\d+\.\d+)%", navigator.text)
        self.starRate = float(match.group(1))
        navigator = navigator.find_next('td', class_='desc')
        match = re.match("(\d+) Hits", navigator.text)
        self.hits['buster'] = int(match.group(1))
        navigator = navigator.find_next('td', class_='desc')
        match = re.match("(\d+\.\d+)%", navigator.text)
        self.deathRate = float(match.group(1))
        navigator = navigator.find_next('td', class_='desc')
        match = re.match("(\d+) Hits", navigator.text)
        self.hits['extra'] = int(match.group(1))
        navigator = navigator.find_next('td', class_='desc')
        self.attribute = navigator.text.rstrip()
        navigator = navigator.find_next('td', class_='desc')
        match = re.match("(\d+) Hits", navigator.text)
        self.hits['np'] = int(match.group(1))
        navigator = navigator.find_next('td', class_='desc')
        self.traits = navigator.text.rstrip().split(',')
        [x.strip() for x in self.alias]

        self.deck = {'quick': 0, 'arts': 0, 'buster': 0}