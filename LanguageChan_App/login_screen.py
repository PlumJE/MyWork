from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from db_interface import usersDBinterface
from folder_paths import GUI_folder

Builder.load_file(GUI_folder + 'login_screen_GUI.kv')

class LoginWin(GridLayout):
    def login(self):
        nickname = self.ids.nickname.text
        password = self.ids.password.text
        try:
            if nickname.strip() == '' or password.strip() == '':
                raise Exception('Invalid input')
            
            usersDBinterface.login(nickname, password)
            loginscreen.goto_gamescreen()
        except Exception as e:
            Popup(
                title='Login Error', 
                content=Label(text=str(e)), 
                size_hint=(1, 0.2), 
                auto_dismiss=True
            ).open()
    def showRegwin(self):
        loginscreen.showRegWin()
loginwin = LoginWin()

class RegWin(GridLayout):
    def register(self):
        nickname = self.ids.nickname.text
        mailaddr = self.ids.mailaddr.text
        password = self.ids.password.text
        pwagain = self.ids.pwagain.text
        try:
            if nickname.strip() == '' or mailaddr.strip() == '' or password.strip() == '':
                raise Exception('Invalid input')
            if password != pwagain:
                raise Exception('Pls input same password')
            
            usersDBinterface.register(nickname, mailaddr, password)
            Popup(
                title='Congrats!', 
                content=Label(text='Registration succeeded!'), 
                size_hint=(1, 0.2), 
                auto_dismiss=True
            ).open()
        except Exception as e:
            Popup(
                title='Registration Error', 
                content=Label(text=str(e)), 
                size_hint=(1, 0.2), 
                auto_dismiss=True
            ).open()
    def showLoginWin(self):
        loginscreen.showLoginWin()
regwin = RegWin()

class LoginScreen(Screen):
    def goto_gamescreen(self):
        usersDBinterface.post_item()
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