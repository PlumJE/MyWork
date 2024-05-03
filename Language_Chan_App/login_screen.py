from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from db_interface import userDBinter
from folder_paths import GUI_folder

Builder.load_file(GUI_folder + 'login_screen_GUI.kv')

class LoginWin(GridLayout):
    def login(self):
        if self.ids.nickname.text == '' or self.ids.password.text == '':
            return
        result = userDBinter.login(self.ids.nickname.text, self.ids.password.text)
        if result == False:
            Popup(title="Login Error", content=Label(text="Sorry, we can't find your account :("), size_hint=(1, 0.2), auto_dismiss=True).open()
        else:
            loginscreen.goto_gamescreen()
    def showRegwin(self):
        loginscreen.showRegWin()
loginwin = LoginWin()

class RegWin(GridLayout):
    def register(self):
        if self.ids.nickname.text == '' or self.ids.mailaddr.text == '' or self.ids.password.text == '':
            return
        if self.ids.password.text != self.ids.pwagain.text:
            Popup(title="Password Error", content=Label(text="Please write same pasword!!"), size_hint=(1, 0.2), auto_dismiss=True).open()
            return
        result = userDBinter.insertUserInfo(self.ids.nickname.text, self.ids.mailaddr.text, self.ids.password.text)
        if result == False:
            Popup(title="Registration Error", content=Label(text="Sorry, your registration is failed :("), size_hint=(1, 0.2), auto_dismiss=True).open()
        else:
            Popup(title="Congrats!", content=Label(text="Registration succeeded!"), size_hint=(1, 0.2), auto_dismiss=True).open()
    def showLoginWin(self):
        loginscreen.showLoginWin()
regwin = RegWin()

class LoginScreen(Screen):
    def goto_gamescreen(self):
        self.manager.current = "Game Screen"
    def showLoginWin(self):
        if regwin in self.children:
            self.remove_widget(regwin)
        if loginwin not in self.children:
            self.add_widget(loginwin)
    def showRegWin(self):
        if loginwin in self.children:
            self.remove_widget(loginwin)
        if regwin not in self.children:
            self.add_widget(regwin)
loginscreen = LoginScreen()