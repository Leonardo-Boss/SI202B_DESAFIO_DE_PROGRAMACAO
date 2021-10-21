import requests
import re
import time
import datetime
from bs4 import BeautifulSoup

class Moodle:
    def __init__(self, username:str, password:str):
        self.data = {"username": username, "password": password, "login": "Entrar"}
        self.session = requests.session()
        self.sesskey = None
        self.__login()
    
    def __login(self):
        self.session.get('https://moodle.ggte.unicamp.br/')
        response = self.session.get('https://moodle.ggte.unicamp.br/login/index.php')
        soup = BeautifulSoup(response.content, 'html.parser')
        action = soup.find("form", id="kc-form-login")
        response = self.session.post(action['action'], self.data)
        self.sesskey = re.search(r'sesskey":".*?"', response.text).group().removeprefix('sesskey":"').removesuffix('"')

    def get_events(self):
        url = f'https://moodle.ggte.unicamp.br/lib/ajax/service.php?sesskey={self.sesskey}&info=core_calendar_get_action_events_by_timesort'
        payload = '[{"index":0,"methodname":"core_calendar_get_action_events_by_timesort","args":{"limitnum":26,"timesortfrom":' + str(int(time.mktime(datetime.date.today().timetuple()))) + ',"limittononsuspendedevents":true}}]'
        response = self.session.post(url, data=payload)
        return response.json()