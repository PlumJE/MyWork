import requests
from debug import log

class DBInterface:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/'
    def __execute(self, method, url, **kwargs):
        # status_code가 4xx, 5xx이면 예외객체를 리턴, 2xx 등이면 결과값을 리턴한다
        response = method(url=url, **kwargs)
        if response.status_code // 100 == 4:
            log.ger.error('Client error!: ' + str(response.status_code) + ' = ' + str(response.json().get('error')))
            match response.status_code:
                case 400:
                    return Exception('You have bad request.')
                case 401:
                    return Exception('You have wrong nickname or password')
                case 403:
                    return Exception('You were forbidden.')
                case 404:
                    return Exception("Your wanting doesn't exist.")
                case 408:
                    return Exception('Your request has timeout.')
        elif response.status_code // 100 == 5:
            log.ger.error('Server error!: ' + str(response.status_code) + ' = ' + str(response.json().get('error')))
            match response.status_code:
                case 500:
                    return Exception('We have an error.')
                case 501:
                    return Exception('We have not implemented yet.')
                case 502:
                    return Exception('We have bad gateway.')
                case 503:
                    return Exception('We are not available now.')
                case 504:
                    return Exception('Our response has timeout.')
        else:
            return response.json()
    def _get(self, url, **kwargs):
        return self.__execute(requests.get, url, **kwargs)
    def _put(self, url, **kwargs):
        return self.__execute(requests.put, url, **kwargs)
    def _post(self, url, **kwargs):
        return self.__execute(requests.post, url, **kwargs)
    def _delete(self, url, **kwargs):
        return self.__execute(requests.delete, url, **kwargs)

class UsersDBInterface(DBInterface):
    def __init__(self):
        super(UsersDBInterface, self).__init__()
        self.url += 'users/'
        self.token = 'nothing'
        self.usernum = 0
    def login(self, nickname, password):
        url = self.url + 'loginout/'
        data = {
            'nickname': nickname, 
            'password': password
        }

        result = self._post(url, data=data)
        if type(result) == Exception:
            raise result

        self.token = result.get('token')
        self.usernum = result.get('usernum') 
    def logout(self):
        url = self.url + 'loginout/'
        headers = {
            'Autorization': 'Token ' + self.token
        }

        result = self._delete(url, headers=headers)
        if type(result) == Exception:
            raise result

        self.token = ''
        self.usernum = 0
    def register(self, nickname, mailaddr, password):
        url = self.url + 'signupdown/'
        data = {
            'nickname': nickname, 
            'mailaddr': mailaddr, 
            'password': password
        }
        
        result = self._post(url, data=data)
        if type(result) == Exception:
            raise result
    def unregister(self):
        url = self.url + 'signupdown/'
        headers = {
            'Authorization': 'Token ' + self.token
        }

        result = self._delete(url, headers=headers)
        if type(result) == Exception:
            raise result
        
        self.logout()
    def get_chara_nums(self):
        url = self.url + 'charas/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum
        }

        result = self._get(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
        
        log.ger.info('Charanums are ' + str(result.get('charanums')))
        
        return result.get('charanums')
    def post_chara(self, charanum):
        url = self.url + 'chara/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'charanum': charanum
        }

        result = self._post(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
    def get_chara_info(self, charanum):
        url = self.url + 'chara/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'charanum': charanum
        }

        result = self._get(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
        
        return result
    def put_chara_lvl(self, charanum):
        lvl = self.get_charainfo(self.usernum, charanum).get('lvl') + 1
        atk = lvl * 10
        dps = lvl * 10

        url = self.url + 'chara/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'charanum': charanum,
            'lvl': lvl,
            'atk': atk,
            'dps': dps
        }

        result = self._put(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
    def post_item(self):
        url = self.url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
        }

        result = self._post(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
    def get_money(self):
        url = self.url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum
        }

        result = self._get(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
        
        return result.get('money')
    def get_jewel(self):
        url = self.url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum
        }

        result = self._get(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
        
        return result.get('jewel')
    def put_money(self, money):
        url = self.url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'money': money
        }

        result = self._put(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
    def put_jewel(self, jewel):
        url = self.url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'jewel': jewel
        }

        result = self._put(url, headers=headers, data=data)
        if type(result) == Exception:
            raise result
usersDBinterface = UsersDBInterface()

class EntitiesDBInterface(DBInterface):
    def __init__(self):
        super(EntitiesDBInterface, self).__init__()
        self.url += 'lessons/'
    def get_fullimg(self, charanum):
        return 'english_chan.jpg'
entitiesDBinterface = EntitiesDBInterface()

class LessonsDBInterface(DBInterface):
    def __init__(self):
        super(LessonsDBInterface, self).__init__()
        self.url += 'lessons/'
    def get_lessonmap_nums(self):
        url = self.url + 'lessonmaps/'

        result = self._get(url)
        if type(result) == Exception:
            raise result
        
        return result.get('lessonmapnum')
    def get_lessonmap_info(self, lessonmapnum):
        url = self.url + 'lessonmap/'
        data = {
            'lessonmapnum': lessonmapnum
        }

        result = self._get(url, data=data)
        if type(result) == Exception:
            raise result
        
        return result
lessonsDBinterface = LessonsDBInterface()