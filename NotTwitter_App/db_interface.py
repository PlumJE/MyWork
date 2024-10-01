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

# 유저 관리 인터페이스 클래스
class UsersDBInterface(DBInterface):
    def __init__(self):
        super(UsersDBInterface, self).__init__()
        self._url += 'users/'
        self._token = ''
        self._usernum = 0
    # 성공시 None, 실패시 Popup을 리턴
    def login(self, nickname, password):
        url = self._url + 'loginout/'
        data = {
            'nickname': nickname,
            'password': password
        }

        response = self._post(url, data=data)

        if type(response) == ResponseException:
            return Popup(
                title='Login failed',
                content=Label(text=str(response)),
                size_hint=(1, 0.2),
                auto_dismiss=True
            )
        
        self._token = response.get('token')
        self._usernum = response.get('usernum')
    # 성공시 None, 실패시 Popup을 리턴
    def logout(self):
        url = self._url + 'loginout/'
        headers = self.get_header()

        response = self._delete(url, headers=headers)

        if type(response) == ResponseException:
            return Popup(
                title='Logout failed',
                content=Label(text=str(response)),
                size_hint=(1, 0.2),
                auto_dismiss=True
            )

        self._token = ''
        self._usernum = 0
    # 성공시 None, 실패시 Popup을 리턴
    def signup(self, nickname, mailaddr, password):
        url = self._url + 'signupdown/'
        data = {
            'nickname': nickname,
            'mailaddr': mailaddr,
            'password': password
        }

        response = self._post(url, data=data)

        if type(response) == ResponseException:
            return Popup(
                title='Signup failed',
                content=Label(text=str(response)),
                size_hint=(1, 0.2),
                auto_dismiss=True
            )
    # 성공시 None, 실패시 Popup을 리턴
    def signdown(self):
        url = self._url + 'signupdown/'
        headers = self.get_header()
        
        response = self._delete(url, headers=headers)

        if type(response) == ResponseException:
            return Popup(
                title='Signdown failed',
                content=Label(text=str(response)),
                size_hint=(1, 0.2),
                auto_dismiss=True
            )
    # 성공시 유저명, 실패시 Popup을 리턴
    def get_nickname(self, usernum=None):
        if usernum == None:
            usernum = self._usernum

        url = self._url + 'nickname/'
        headers = self.get_header()

        response = self._get(url, headers=headers)

        if type(response) == ResponseException:
            print('Nickname not founded!!!!!')
            return Popup(
                title='Database error has occurred!',
                size_hint=(1, 0.2),
                auto_dismiss=True
            )
        
        return response.get('nickname')
    # 성공시 None, 실패시 Popup을 리턴
    def put_nickname(self, nickname):
        url = self._url + 'nickname/'
        headers = self.get_header()
        data = {
            'nickname': nickname
        }

        response = self._put(url, headers=headers, data=data)

        if type(response) == ResponseException:
            print('nickname change failed!!!')
            return Popup(
                title='Database error has occurred!',
                size_hint=(1, 0.2),
                auto_dismiss=True
            )
    # http 헤더를 생성
    def get_header(self):
        return {
            'Authorization': 'Token ' + self._token,
            'usernum': str(self._usernum)
        }
usersdbinterface = UsersDBInterface()

# 포스트 관리 인터페이스 클래스
class PostsDBInterface(DBInterface):
    def __init__(self):
        super(PostsDBInterface, self).__init__()
        self._url += 'posts/'
        self._id_prefix = ''
    # 성공시 리스트, 실패시 Popup을 리턴
    def get_postlist(self):
        url = self._url + 'postlist/'
        headers = usersdbinterface.get_header()
        data = {
            'id_prefix': self._id_prefix
        }

        response = self._get(url, headers=headers, data=data)

        if type(response) == ResponseException:
            if response.code == 404:
                return []
            else:
                return Popup(
                    title='Getting post list failed',
                    content=Label(text=str(response)),
                    size_hint=(1, 0.2),
                    auto_dismiss=True
                )

        return response.get('id_list')
    # 성공시 {...}, 실패시 Popup을 리턴
    def get_post(self, id):
        try:
            url = self._url + 'post/'
            headers = usersdbinterface.get_header()
            data = {
                'id': id
            }

            response = self._get(url, headers=headers, data=data)
            if type(response) == ResponseException:
                if response.status_code == 404:
                    return {}
                else:
                    return Popup(
                    title='Getting post list failed',
                    content=Label(text=str(response)),
                    size_hint=(1, 0.2),
                    auto_dismiss=True
                )
            
            return response
        except Exception as e:
            return Popup(
                title='Loading post information failed',
                content=Label(text=str(e)),
                size_hint=(1, 0.2),
                auto_dismiss=True
            )
    # 성공시 None, 실패시 Popup을 리턴
    def post_post(self, writedate, content):
        try:
            url = self._url + 'post/'
            headers = usersdbinterface.get_header()
            data = {
                'id_prefix': self._id_prefix,
                'writer': usersdbinterface.get_header().get('usernum'),
                'writedate': writedate,
                'content': content
            }

            response = self._post(url, headers=headers, data=data)
            if type(response) == ResponseException:
                return Popup(
                    title='Getting post list failed',
                    content=Label(text=str(response)),
                    size_hint=(1, 0.2),
                    auto_dismiss=True
                )
        except Exception as e:
            return Popup(
                title='Saving new post failed',
                content=Label(text=str(e)),
                size_hint=(1, 0.2),
                auto_dismiss=True
            )
    # 현재 id_prefix를 읽음
    def get_id_prefix(self):
        return self._id_prefix
    # 현재 id_prefix를 새로 씀
    def put_id_prefix(self, id_prefix):
        self._id_prefix = id_prefix
postsdbinterface = PostsDBInterface()
