"""
작성자 : 외기러기
작성일 : 2022-11-07
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""


from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager
import sqlite3


Builder.load_file('main_GUI.kv')

#SQLite DB 인터페이스 클래스
class DBInterFace:
    conn = sqlite3.connect("LoginApp.db", isolation_level=None)
    cur = conn.cursor()
    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS UserInfo(nickname text, mailaddr text, password text);")
    def __del__(self):
        self.conn.close()
    def selectByNickPswd(self, nickname, password):
        try:
            self.cur.execute("SELECT ROWID FROM UserInfo WHERE nickname=? AND password=?", (str(nickname), str(password)))
            result = self.cur.fetchone()
        except Exception as err:
            print("Select query failed :", str(err))
            result = None
        return result if result == None else result[0]
    def insertNewMember(self, nickname, mailaddr, password):
        try:
            if self.selectByNickPswd(nickname, password) != None:
                result = False
            else:
                self.cur.execute("INSERT INTO UserInfo VALUES(?, ?, ?)", (str(nickname), str(mailaddr), str(password)))
                result = True
        except Exception as err:
            print("Insert query failed :", str(err))
            result = False
        return result

#로그인 화면 클래스
class LoginScreen(AnchorLayout):
    titleimage = ObjectProperty()
    loginWin = ObjectProperty()
    regWin = ObjectProperty()
    nickname1 = ObjectProperty()
    password1 = ObjectProperty()
    nickname2 = ObjectProperty()
    mailaddr = ObjectProperty()
    password2 = ObjectProperty()
    pswdagain = ObjectProperty()
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.titleimage.bind(on_press=self.showLoginWin)
        self.remove_widget(self.loginWin)
        self.remove_widget(self.regWin)
    def showLoginWin(self, *args):
        self.titleimage.unbind(on_press=self.showLoginWin)
        self.add_widget(self.loginWin)
        self.remove_widget(self.regWin)
    def login(self, *args):
        if LoginApp.dbinterface.selectByNickPswd(self.nickname1.text, self.password1.text) != None:
            LoginApp.screen_manager.current = "Main Screen"
        else:
            Popup(content=Label(text="Your login has failed ;("), size_hint=(1, 0.2), auto_dismiss=True).open()
    def showRegWin(self, *args):
        self.remove_widget(self.loginWin)
        self.add_widget(self.regWin)
    def register(self, *args):
        if (self.nickname2.text == "" or self.mailaddr.text == "" or self.password2.text == ""):
            Popup(content=Label(text="Please input valid info"), size_hint=(1, 0.2), auto_dismiss=True).open()
            return
        if (self.password2.text != self.pswdagain.text):
            Popup(content=Label(text="Please input same password twice"), size_hint=(1, 0.2), auto_dismiss=True).open()
            return
        if LoginApp.dbinterface.insertNewMember(self.nickname2.text, self.mailaddr.text, self.password2.text) == True:
            Popup(content=Label(text="You regist successfully! :)"), size_hint=(1, 0.2), auto_dismiss=True).open()
        else:
            Popup(content=Label(text="Your registration has denied ;("), size_hint=(1, 0.2), auto_dismiss=True).open()

#로그인 이후 메인 화면 클래스
class MainScreen(AnchorLayout):
    pass

#앱 전체를 나타내는 클래스
class LoginApp(App):
    screen_manager = ScreenManager()
    dbinterface = DBInterFace()
    def build(self):
        screen = Screen(name="Login Screen")
        screen.add_widget(LoginScreen())
        self.screen_manager.add_widget(screen)

        screen = Screen(name="Main Screen")
        screen.add_widget(MainScreen())
        self.screen_manager.add_widget(screen)

        return self.screen_manager
if __name__ == "__main__":
    LoginApp().run()