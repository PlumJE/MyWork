from kivy.uix.popup import Popup
from kivy.uix.label import Label
from requests.exceptions import RequestException
import requests


# 응답 코드를 저장한 예외 클래스
class ResponseException(RequestException):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    def __str__(self):
        return '{} : {}'.format(self.code, self.message)

# 서버와의 인터페이스 베이스 클래스
class DBInterface:
    _url = 'http://127.0.0.1:8000/'
    # http 통신을 실행하는 함수. json()결과물이나 REsponseException()을 리턴만 하고, 예외를 발생시키지 않는다.
    def __execute(self, method, url, headers, data):
        try:
            response = method(url, headers=headers, data=data)
            match response.status_code:
                case 200:
                    return response.json()
                case 201:
                    return response.json()
                case _:
                    raise ResponseException(response.status_code, response.json().get('error'))
        except ResponseException as e:
            return e
        except Exception as e:
            return ResponseException(499, 'Internal client error')
    def _post(self, url, headers={}, data={}):
        return self.__execute(requests.post, url, headers, data)
    def _get(self, url, headers={}, data={}):
        return self.__execute(requests.get, url, headers, data)
    def _put(self, url, headers={}, data={}):
        return self.__execute(requests.put, url, headers, data)
    def _delete(self, url, headers={}, data={}):
        return self.__execute(requests.delete, url, headers, data)

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
        if type(result) == ResponseException:
            raise result

        self.token = result.get('token')
        self.usernum = result.get('usernum') 
    def logout(self):
        url = self.url + 'loginout/'
        headers = {
            'Autorization': 'Token ' + self.token
        }

        result = self._delete(url, headers=headers)
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
            raise result
    def unregister(self):
        url = self.url + 'signupdown/'
        headers = {
            'Authorization': 'Token ' + self.token
        }

        result = self._delete(url, headers=headers)
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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
        if type(result) == ResponseException:
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