import requests
import json
from bs4 import BeautifulSoup

s = requests.Session()

class API():
    def startSession(self, npst_pass):
        req = s.get('https://ctf.phst.no/login', timeout=5)
        soup = BeautifulSoup(req.text, 'html.parser')
        nonce = soup.findAll('input', {'name': 'nonce'})[0]['value']
        data = {
            'password': npst_pass,
            'name': 'Påskekylling BOT',
            'nonce': nonce
        }
        s.post('https://ctf.phst.no/login', data=data, timeout=5)

    def getID(self, challname): 
        r = s.get(url='https://ctf.phst.no/api/v1/challenges', timeout=5)
        parsed = json.loads(r.text[23:-2])
        for item in parsed:
            if item['name'].lower() == challname.lower():
                return item['id']
        return 0

    def getChalls(self): 
        r = s.get(url='https://ctf.phst.no/api/v1/challenges', timeout=5)
        parsed = json.loads(r.text[23:-2])
        challs = []
        for item in parsed:
            challs.append(item['name'])
        return challs

    def getChallScore(self, id):
        r = s.get(url=f'https://ctf.phst.no/api/v1/challenges/{id}/solves', timeout=5)
        parsed = json.loads(r.text[23:-2])
        names = []
        for x, item in enumerate(parsed):
            if x <= 9:
                names.append(item['name'])
            if x >= 9:
                return names
        return names

    def getScoreBoard(self):
        r = s.get(url='https://ctf.phst.no/scoreboard', timeout=5)
        return BeautifulSoup(r.text, 'html.parser')