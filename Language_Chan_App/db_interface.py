import sqlite3

from folder_paths import db_folder
from others import logger

# DB에 접근하는 클래스들의 상위 클래스
class DBInterface:
    # 데이터베이스와의 접속 시작
    def __init__(self, path, isolvl):
        self.conn = sqlite3.connect(path, isolation_level=isolvl)
        self.cur = self.conn.cursor()
    # 데이터베이스와의 접속 종료
    def __del__(self):
        self.cur.close()
        self.conn.close()
    # select쿼리를 처리하는 메소드
    def handleSelectQuery(self, cmd_str):
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchall()
        except Exception as err:
            logger.error("We have an error in this query : "+str(err))
            logger.error("We will return void list")
            return []
    # change계 쿼리를 처리하는 메소드
    def handleChangeQuery(self, cmd_str):
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception as err:
            logger.error("We have an error in this query : "+str(err))
            logger.error("We will return False")
            return False

# 유저정보 DB에 접근하는 클래스, 사용자 변경 가능
class UserDBInterface(DBInterface):
    def __init__(self):
        super().__init__(db_folder + "user.db", None)
        self.cur.execute("CREATE TABLE IF NOT EXISTS UserInfo(\
                         usernum INT NOT NULL UNIQUE, \
                         nickname TEXT, \
                         mailaddr TEXT, \
                         password TEXT, \
                         birthday TEXT, \
                         motherlanguage TEXT DEFAULT 'Korean', \
                         PRIMARY KEY(usernum));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS UsersChara(\
                         usernum INT, \
                         charanum INT, \
                         charalvl INT DEFAULT 1, \
                         FOREIGN KEY(usernum) REFERENCES UserInfo(usernum));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS UsersItem(\
                         usernum INT, \
                         money INT DEFAULT 100, \
                         jewel INT DEFAULT 10, \
                         FOREIGN KEY(usernum) REFERENCES UserInfo(usernum));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS UsersProgress(\
                         usernum INT, \
                         classnum INT, \
                         progress INT, \
                         FOREIGN KEY(usernum) REFERENCES UserInfo(usernum));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS UsersFriends(\
                         usernum INT, \
                         friendnum INT, \
                         FOREIGN KEY(usernum) REFERENCES UserInfo(usernum), \
                         FOREIGN KEY(friendnum) REFERENCES UserInfo(usernum));")
    def login(self, nickname, password):
        cmd_str = "SELECT usernum FROM UserInfo WHERE nickname='{}' AND password='{}';".format(nickname, password)
        return self.handleSelectQuery(cmd_str)
    def insertUserInfo(self, nickname, mailaddr, password):
        # 이미 있는지 확인한다
        check = self.login(nickname, password)
        if check != []:
            return
        # 새로운 유저의 번호를 결정한다
        self.cur.execute("SELECT COUNT(*) FROM UserInfo;")
        new_num = self.cur.fetchone()[0] + 1
        # 새로운 유저의 정보를 등재한다
        cmd_str = "INSERT INTO UserInfo(usernum, nickname, mailaddr, password) VALUES({}, '{}', '{}', '{}');".format(new_num, nickname, mailaddr, password)
        result = self.handleChangeQuery(cmd_str)
        # 새로운 유저에게 초기 아이템을 지급한다
        self.insertNewusersItem(new_num)
        self.insertUsersChara(new_num, 1)
        self.insertUsersChara(new_num, 2)
        # 종료
        return result
    def selectUsersLang(self, usernum):
        cmd_str = "SELECT motherlanguage FROM UsersOption WHERE usernum={}".format(usernum)
        return self.handleSelectQuery(cmd_str)
    def updateUsersLang(self, usernum):
        cmd_str = "UPDATE UserInfo SET motherlanguage WHERE usernum={}".format(usernum)
        return self.handleChangeQuery(cmd_str)
    def selectUsersChara(self, usernum):
        cmd_str = "SELECT charanum, charalvl FROM UsersChara WHERE usernum={}".format(usernum)
        return self.handleSelectQuery(cmd_str)
    def insertUsersChara(self, usernum, charanum):
        cmd_str = "INSERT INTO UsersChara VALUES({}, {}, 1);".format(usernum, charanum)
        return self.handleChangeQuery(cmd_str)
    def selectUsersMoney(self, usernum):
        cmd_str = "SELECT money FROM UsersItem WHERE usernum={}".format(usernum)
        return self.handleSelectQuery(cmd_str)
    def selectUsersJewel(self, usernum):
        cmd_str = "SELECT jewel FROM UsersItem WHERE usernum={}".format(usernum)
        return self.handleSelectQuery(cmd_str)
    def insertNewusersItem(self, new_usernum):
        cmd_str = "INSERT INTO UserItem(usernum, money, jewel) VALUES({}, 100, 10)".format(new_usernum)
        return self.handleChangeQuery(cmd_str)
    def updateUsersMoney(self, usernum, money):
        cmd_str = "UPDATE UsersItem SET money={} WHERE usernum={}".format(money, usernum)
        return self.handleChangeQuery(cmd_str)
    def updateUsersJewel(self, usernum, jewel):
        cmd_str = "UPDATE UsersItem SET jewel={} WHERE usernum={}".format(jewel, usernum)
        return self.handleChangeQuery(cmd_str)
userDBinter = UserDBInterface()

# 개체정보 DB에 접근하는 클래스, 개발자만 변경 가능
class EntityDBInterface(DBInterface):
    def __init__(self):
        super().__init__(db_folder + "entity.db", None)
    def selectCharaName(self, charanum):
        cmd_str = "SELECT charaname FROM CharaInfo WHERE charanum={}".format(charanum)
        return self.handleSelectQuery(cmd_str)
    def selectCharaProfileimg(self, charanum):
        cmd_str = "SELECT profileimg FROM CharaInfo WHERE charanum={}".format(charanum)
        return self.handleSelectQuery(cmd_str)
    def selectCharaFullimg(self, charanum):
        cmd_str = "SELECT fullimg FROM CharaInfo WHERE charanum={}".format(charanum)
        return self.handleSelectQuery(cmd_str)
    def selectEnemyName(self, enemynum):
        cmd_str = "SELECT * FROM EnemyInfo WHERE enemynum={}".format(enemynum)
        return self.handleSelectQuery(cmd_str)
entityDBinter = EntityDBInterface()

# 퀴즈 및 클래스 정보에 접근하는 클래스, 개발자만 변경 가능
class QuizDBInterface(DBInterface):
    def __init__(self):
        super().__init__(db_folder + "quiz.db", None)
    def selectAllClassInfo(self):
        cmd_str = "SELECT * FROM ClassInfo"
        return self.handleSelectQuery(cmd_str)
quizDBinter = QuizDBInterface()