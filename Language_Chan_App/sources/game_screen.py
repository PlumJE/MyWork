from random import choice
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from db_interface import userDBinter, entityDBinter, quizDBinter
from folder_paths import GUI_folder, charas_folder, bg_folder
from others import logger, cur_usernum

Builder.load_file(GUI_folder + 'game_screen_GUI.kv')

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
    def show_random_chara(self):
        charanum = choice(userDBinter.selectUsersChara(cur_usernum.get()))[0]
        charaimg = entityDBinter.selectCharaFullimg(charanum)[0][0]
        self.ids.charaimg.source = charas_folder + charaimg
mainscreen = MainScreen()

class Class(Screen):
    def __init__(self, classnum, classname, bgimg, **kwargs):
        super(Class, self).__init__(**kwargs)
        self.name = str(classname)
        self.ids.bg.source = bg_folder + bgimg

class ClassesScreen(Screen):
    def __init__(self, **kwargs):
        super(ClassesScreen, self).__init__(**kwargs)
        for classinfo in quizDBinter.selectAllClassInfo():
            self.ids.class_screen_manager.add_widget(Class(*classinfo))
            self.ids.class_tabbar.data.append({"text":classinfo[1], "on_release":self.change_class(classinfo[1])})
            # None은 함수처럼 호출할 수 없습니다 오류 발생!!
    def change_class(self, classname):
        self.ids.class_screen_manager.current = classname
    def goto_quizscreen(self, language, level):
        gamescreen.goto_quizscreen(language, level)
classscreen = ClassesScreen()

class CharacterScreen(Screen):
    pass
characterscreen = CharacterScreen()

class GachaScreen(Screen):
    def gacha(self):
        jewel = userDBinter.selectUsersJewel()
        if jewel < 10:
            Popup(title="Gacha failed!", content=Label(text="Your Jewel isn't enough"), size_hint=(1, 0.2), auto_dismiss=True).open()
        else:
            jewel -= 10
            gamescreen.setJewelLabel(jewel)
            result = None
            if result == None:
                result = "1 jewel"
                jewel += 1
                gamescreen.setJewelLabel(jewel)
            Popup(title="Gacha Result", content=Label(text="You get"+result+"!"), size_hint=(1, 0.2), auto_dismiss=True).open()
gachascreen = GachaScreen()

class OptionScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.useridlbl.text = str(cur_usernum.get())
        return super().on_pre_enter(*args)
    def logout(self):
        self.ids.useridlbl.text = str(cur_usernum.init())
        gamescreen.showMainScreen()
        gamescreen.goto_loginscreen()
    def showLangChanWin(self):
        self.add_widget(langchangewin)
    def hideLangChanWin(self):
        self.remove_widget(langchangewin)
optionscreen = OptionScreen()

class LangChangeWin(BoxLayout):
    def close(self):
        optionscreen.hideLangChanWin()
    def changelang(self):
        pass
langchangewin = LangChangeWin()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.ids.game_screen_manager.add_widget(mainscreen)
        self.ids.game_screen_manager.add_widget(classscreen)
        self.ids.game_screen_manager.add_widget(characterscreen)
        self.ids.game_screen_manager.add_widget(gachascreen)
        self.ids.game_screen_manager.add_widget(optionscreen)
    def on_pre_enter(self, *kwargs):
        super().on_enter(*kwargs)
        money = userDBinter.selectUsersMoney(cur_usernum.get())
        jewel = userDBinter.selectUsersJewel(cur_usernum.get())
        self.ids.moneylabel.text = "Money : " + str(money[0][0])
        self.ids.jewellabel.text = "Jewel : " + str(jewel[0][0])
        mainscreen.show_random_chara()
    def goto_loginscreen(self):
        self.manager.current = "Login Screen"
    def goto_quizscreen(self, language, level):
        self.manager.current = "Quiz Screen"
    def showMainScreen(self):
        self.ids.game_screen_manager.current = "Main Screen"
        mainscreen.show_random_chara()
    def showStageScreen(self):
        self.ids.game_screen_manager.current = "Classes Screen"
    def showCharacterScreen(self):
        self.ids.game_screen_manager.current = "Character Screen"
    def showGachaScreen(self):
        self.ids.game_screen_manager.current = "Gacha Screen"
    def showOptionScreen(self):
        self.ids.game_screen_manager.current = "Option Screen"
    def setMoneyLabel(self, money):
        userDBinter.updateUsersMoney(money)
        self.ids.moneylabel.text = "Money : " + str(money)
    def setJewelLabel(self, jewel):
        userDBinter.updateUsersJewel(jewel)
        self.ids.jewellabel.text = "Jewel : " + str(jewel)
gamescreen = GameScreen()