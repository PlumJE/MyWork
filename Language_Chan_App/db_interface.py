import sqlite3
from folder_paths import db_folder

class EntityDBInterface:
    conn = sqlite3.connect(db_folder + "entity.db", isolation_level=None)
    cur = conn.cursor()
    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS CharaInfo();")
        self.cur.execute("CREATE TABLE IF NOT EXISTS EnemyInfo();")
        self.cur.execute("INSERT OR REPLACE INTO CharaInfo VALUES(1, 'English Chan', '', '', '', '');")
    def __del__(self):
        self.conn.close()
    def selectCharaInfo(self, charanum):
        cmd_str = "SELECT * FROM CharaInfo WHERE charanum={}".format(charanum)
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchall()
        except Exception:
            print("Error :", cmd_str)
            return
#entityDBinter = EntityDBInterface()

class StageDBInterface:
    conn = sqlite3.connect(db_folder + "stage.db", isolation_level=None)
    cur = conn.cursor()
    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS StageInfo(language text NOT NULL, stagebgi TEXT, quizbgi TEXT, maxlvl INTEGER, PRIMARY KEY(language));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS StagesEnemy(language text, enemynum int, FOREIGN KEY(language) REFERENCES StageInfo(language));")
        self.cur.execute("INSERT OR REPLACE INTO StageInfo VALUES('English', 'English_stage_background', '\English_quiz_background', 5);")
    def __del__(self):
        self.conn.close()
    def selectStageList(self, motherlanaguage):
        cmd_str = "SELECT * FROM StageInfo WHERE lanaguage!='{}';".format(motherlanaguage)
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchall()
        except Exception:
            print("Error :", cmd_str)
            return
stageDBinter = StageDBInterface()

class UserDBInterface:
    conn = sqlite3.connect(db_folder + "user.db", isolation_level=None)
    cur = conn.cursor()
    current_usernum = 0
    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS UserInfo(usernum int NOT NULL, nickname text, mailaddr text, password text, motherlanguage text DEFAULT 'Korean', coins int DEFAULT 100, jewels int DEFAULT 10, PRIMARY KEY(usernum));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS UsersChara(usernum int, charanum int, charalvl int DEFAULT 1, FOREIGN KEY(usernum) REFERENCES UserInfo(usernum));")
        #self.cur.execute("INSERT OR REPLACE INTO UserInfo VALUES(1, 'leejieung', 'lje64257@gmail.com', 'dlwldmd', 'Korean', 100, 10)")
    def __del__(self):
        self.conn.close()
    def currentUserNum(self, set=None):
        if set == None:
            return self.current_usernum
        else:
            self.current_usernum = set
    def login(self, nickname, password):
        cmd_str = "SELECT usernum FROM UserInfo WHERE nickname='{}' AND password='{}';".format(nickname, password)
        try:
            self.cur.execute(cmd_str)
            self.current_usernum = self.cur.fetchone()[0]
            return True
        except Exception:
            print("Error :", cmd_str)
            return False
    def insertUserInfo(self, nickname, mailaddr, password):
        self.cur.execute("SELECT COUNT(*) FROM UserInfo;")
        new_num = self.cur.fetchone()[0] + 1
        cmd_str = "INSERT INTO UserInfo VALUES({}, '{}', '{}', '{}');".format(new_num, nickname, mailaddr, password)
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception:
            print("Error :", cmd_str)
            return False
    def selectUsersChara(self):
        cmd_str = "SELECT charanum, charalvl FROM UsersChara WHERE usernum={}".format(self.current_usernum)
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchall()
        except Exception:
            print("Error :", cmd_str)
    def insertUsersChara(self, charanum):
        cmd_str = "INSERT INTO UsersChara VALUES({}, {}, 1);".format(self.current_usernum, charanum)
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception:
            print("Error :", cmd_str)
            return False
    def selectUsersMoney(self):
        cmd_str = "SELECT money FROM UserInfo WHERE usernum={}".format(self.current_usernum)
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchone()[0]
        except Exception:
            print("Error :", cmd_str)
    def selectUsersJewel(self):
        cmd_str = "SELECT jewel FROM UserInfo WHERE usernum={}".format(self.current_usernum)
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchone()[0]
        except Exception:
            print("Error :", cmd_str)
    def updateUsersMoney(self, money):
        cmd_str = "UPDATE UserInfo SET money={} WHERE usernum={}".format(money, self.current_usernum)
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception:
            print("Error :", cmd_str)
            return False
    def updateUsersJewel(self, jewel):
        cmd_str = "UPDATE UserInfo SET jewel={} WHERE usernum={}".format(jewel, self.current_usernum)
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception:
            print("Error :", cmd_str)
            return False
    def selectUsersLang(self):
        cmd_str = "SELECT motherlanguage FROM UsersOption WHERE usernum={}".format(self.current_usernum)
        try:
            self.cur.execute(cmd_str)
            return self.cur.fetchone()[0]
        except Exception:
            print("Error :", cmd_str)
    def updateUsersLang(self):
        cmd_str = "UPDATE UserInfo SET motherlanguage WHERE usernum={}".format(self.current_usernum)
        try:
            self.cur.execute(cmd_str)
            return True
        except Exception:
            print("Error :", cmd_str)
            return False
userDBinter = UserDBInterface()
