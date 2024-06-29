from re import compile
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from others import dbinterface, appregister, MyPopup, logger
from folder_paths import GUI_folder, graphics_folder

Builder.load_file(GUI_folder + 'login_screen_GUI.kv')

# 로그인 입력창 클래스
class LoginWindow(GridLayout):
    # 입력한 문자열이 유효한지 확인한 후에 로그인을 시도한다
    def login(self, *args):
        usernum = dbinterface.selectByNickPswd(self.ids.nickname1.text, self.ids.password1.text)
        if usernum == None:
            MyPopup('Login failed', 'We cannot find your account ;(').open()
        else:
            appregister.usernum(usernum[0])
            loginscreen.goto_post_screen()
    # 회원가입 창으로 변경한다
    def showRegWin(self, *args):
        loginscreen.showRegWin(*args)
loginwin = LoginWindow()

# 회원가입 입력창 클래스
class RegisterWindow(GridLayout):
    # 입력한 문자열이 유효한지 확인한 후에 회원가입을 시도한다
    def register(self, *args):
        if self.isInvalidStr() or self.isInvalidMailaddr() and self.isDifferentPassword() and self.isAlreadyRegistered(): # 위에는 회원가입 탈락 사유들
            logger.info("그냥 리턴으로 종료")
            return
        if dbinterface.insertNewMember(self.ids.nickname2.text, self.ids.mailaddr.text, self.ids.password2.text) == False:
            MyPopup('Registration failed', 'Your registration has denied ;(').open()
        else:
            MyPopup('Registration succeed!', 'Now you are our member! :)').open()
    # 로그인 창으로 변경한다
    def showLoginWin(self, *args):
        loginscreen.showLoginWin(*args)
    # 입력한 문자열이 유효한지 확인한다
    def isInvalidStr(self):
        for target_str in [self.ids.nickname2.text, self.ids.mailaddr.text, self.ids.password2.text]:
            logger.info("target_str : {}".format(target_str))
            if target_str.isspace() or target_str.find('"') > -1 or target_str.find("'") > -1:
                MyPopup('Registration failed', 'Please input valid letter').open()
                return True
        return False
    # 입력한 메일주소가 유효한 형식인지 확인한다
    def isInvalidMailaddr(self):
        if compile('[0-9A-Za-z]+@[0-9A-Za-z]+.[A-Za-z]+').match(self.ids.mailaddr.text):
            return False
        else:
            MyPopup('Registration failed', 'Please input valid format mail address').open()
            return True
    # 패스워드를 2번 입력할때 실수로 서로 똑같이 입력했는지 확인한다
    def isDifferentPassword(self):
        if self.ids.password2.text != self.ids.pswdagain.text:
            MyPopup('Registration failed', 'Please input same password twice').open()
            return True
        else:
            return False
    # 이미 회원가입 되었는지 확인한다
    def isAlreadyRegistered(self):
        usernum = dbinterface.selectByNickPswd(self.ids.nickname2.text, self.ids.password2.text)
        if usernum != None:
            MyPopup('Registration failed', "There's already same account").open()
            return True
        else:
            return False
regwin = RegisterWindow()

# 로그인 스크린 클래스
class LoginScreen(Screen):
    # state가 0이면 아무런 창도 없고, 1이면 로그인 창만, 2이면 회원가입 창만 있는 상태
    state = 0
    bg_path = graphics_folder + 'login_background.jpg'
    # 로그인 창을 연다
    def openLoginWin(self, *args):
        if self.state == 0:
            self.showLoginWin(args)
    # 로그인 창을 열고, 회원가입 창을 닫는다
    def showLoginWin(self, *args):
        if self.state != 1:
            self.ids.loginlayout.add_widget(loginwin)
        if self.state == 2:
            self.ids.loginlayout.remove_widget(regwin)
        self.state = 1
    # 회원가입 창을 열고, 로그인 창을 닫는다
    def showRegWin(self, *args):
        if self.state != 2:
            self.ids.loginlayout.add_widget(regwin)
        if self.state == 1:
            self.ids.loginlayout.remove_widget(loginwin)
        self.state = 2
    # 게시글 스크린으로 들어간다
    def goto_post_screen(self):
        self.manager.current = "Post Screen"
loginscreen = LoginScreen(name="Login Screen")