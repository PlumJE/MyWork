import sqlite3
import logging
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from folder_paths import db_folder

# logger객체 생성
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# logger의 로그를 파일에 저장하게 설정
file_handler = logging.FileHandler("apps_log.log")
logger.addHandler(file_handler)

# 경고 팝업 클래스
class MyPopup(Popup):
    # 제목과 내용에 문자열을 입력하면 경고 팝업을 생성한다
    def __init__(self, title, content, **kwargs):
        self.title = str(title)
        self.content = Label(text=str(content))
        self.size_hint = (1, 0.2)
        self.auto_dismiss = True
        super().__init__(**kwargs)

# 앱에다 비치명적인 필수 데이터 일부분을 저장하게 하는 클래스
class AppRegister:
    __usernum = 0
    __curparent = ''
    # 현재 접속한 유저의 id를 다루는 획설자이다
    def usernum(self, usernum=None):
        if usernum == None:
            return self.__usernum
        else:
            logger.info("usernum : {} -> {}".format(self.__usernum, usernum))
            self.__usernum = usernum
    # 지금 당장의 부모 게시글의 id를 다루는 획설자이다.
    def curparent(self, curparent=None):
        if curparent == None:
            return self.__curparent
        else:
            logger.info("parent post num : {} -> {}".format(self.__curparent, curparent))
            self.__curparent = curparent
appregister = AppRegister()

#SQLite DB 인터페이스 클래스
class DBInterface:
    conn = sqlite3.connect(db_folder + "UsersAndPosts.db", isolation_level=None)
    cur = conn.cursor()
    # 데이터베이스 접속 및 초기화
    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS UserInfo(number INT NOT NULL UNIQUE, nickname TEXT, mailaddr TEXT, password TEXT, \
                         PRIMARY KEY('number'));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS PostInfo(id TEXT NOT NULL UNIQUE, writer INT, writedate DATE, content TEXT, \
                         PRIMARY KEY('id'));")
        self.cur.execute("INSERT OR IGNORE INTO PostInfo VALUES('/0', 0, '2000-01-01', 'Welcome!!');")
    # 데이터베이스와의 접속 종료
    def __del__(self):
        self.cur.close()
        self.conn.close()
    # 예외상황을 처리하는 메소드
    def handleError(self, err, rtn=None):
        logger.error("We have an error in this query : {}".format(err))
        logger.error("We will return {}".format(rtn))
        return rtn
    # 닉네임과 패스워드를 통해 유저 번호를 select
    def selectByNickPswd(self, nickname, password):
        cmd_str = "SELECT number FROM UserInfo WHERE nickname='{}' AND password='{}';".format(str(nickname), str(password))
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchone()
        except Exception as err:
            return self.handleError(err)
    # 유저 번호를 통해 유저 정보를 select
    def selectByUsernum(self, usernum=None):
        if usernum == None:
            usernum = appregister.usernum()
        if type(usernum) != int:
            return [usernum]
        cmd_str = "SELECT nickname, mailaddr FROM UserInfo WHERE number={};".format(int(usernum))
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchone()
        except Exception as err:
            return self.handleError(err)
    # 유저의 닉네임을 update
    def updateUsernick(self, newnick, usernum=None):
        if usernum == None:
            usernum = appregister.usernum()
        cmd_str = "UPDATE UserInfo SET nickname='{}' WHERE number={};".format(str(newnick), int(usernum))
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception as err:
            return self.handleError(err, False)
    # 새로운 유저 정보를 insert
    def insertNewMember(self, nickname, mailaddr, password):
        if self.selectByNickPswd(nickname, password) != None:
            return False
        self.cur.execute("SELECT COUNT(*) FROM UserInfo;")
        new_num = self.cur.fetchone()[0] + 1
        cmd_str = "INSERT INTO UserInfo VALUES({}, '{}', '{}', '{}');".format(new_num, str(nickname), str(mailaddr), str(password))
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception as err:
            return self.handleError(err, False)
    # id가 parent인 게시글과, 그의 자식 게시글들을 select
    def selectPosts(self, parent=''):
        if parent == '':
            order = "ORDER BY writedate DESC"
        else:
            order = ""
        cmd_str = "SELECT * FROM PostInfo \
            WHERE (id LIKE '{0}' OR id LIKE '{0}/%') AND (id NOT LIKE '{0}/%/%') {1};".format(str(parent), order)
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchall()
        except Exception as err:
            return self.handleError(err, False)
    # 새로운 글을 insert
    def insertPost(self, writer, writedate, content):
        self.cur.execute("SELECT COUNT(*) FROM PostInfo \
                         WHERE (id LIKE '{0}' OR id LIKE '{0}/%') AND (id NOT LIKE '{0}/%/%');".format(appregister.curparent()))
        new_id = appregister.curparent() + '/' + str(self.cur.fetchone()[0])
        cmd_str = "INSERT INTO PostInfo VALUES('{}', '{}', '{}', \"{}\");".format(new_id, str(writer), str(writedate), str(content))
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception as err:
            return self.handleError(err, False)
dbinterface = DBInterface()
