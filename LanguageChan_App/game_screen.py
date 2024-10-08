from random import choice
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from folder_paths import GUI_folder, bg_folder, charas_folder
from db_interface import usersDBinterface, entitiesDBinterface, lessonsDBinterface

Builder.load_file(GUI_folder + '/game_screen_GUI.kv')

# 메인 화면
class MainScreen(Screen):
    _bg_path = bg_folder + '/main_background.jpg'
    def show_random_chara(self):
        charanums = usersDBinterface.get_chara_nums()
        if charanums == []:
            return
        else:
            charanum = choice(charanums)
            charaimg = entitiesDBinterface.get_fullimg(charanum)
            self.ids.charaimg.source = charas_folder + charaimg
mainscreen = MainScreen()

# 레슨맵 한 개 단위
class LessonMap(Screen):
    def __init__(self, name, bgimg, **kwargs):
        super(self.LessonMapScreen, self).__init__(**kwargs)
        self.name = str(name)
        self.ids.bg.source = bg_folder + bgimg

# 여러개의 레슨맵이 있는 화면
class LessonMapScreen(Screen):
    def __init__(self, **kwargs):
        super(LessonMapScreen, self).__init__(**kwargs)
        # for lessonmap_num in lessonsDBinterface.get_lessonmap_nums():
        #     name = lessonsDBinterface.get_lessonmap_name(lessonmap_num)
        #     bgimg = lessonsDBinterface.get_lessonmap_bgimg(lessonmap_num)
        #     LessonMap(name, bgimg)
    def change_class(self, classname):
        self.ids.class_screen_manager.current = classname
    def goto_quizscreen(self, language, level):
        gamescreen.goto_quizscreen(language, level)
lessonmapscreen = LessonMapScreen()

# 캐릭터 육성 화면
class CharacterScreen(Screen):
    _bg_path = bg_folder + "/character_background.jpg"
characterscreen = CharacterScreen()

# 뽑기 화면
class GachaScreen(Screen):
    _bg_path = bg_folder + "/gacha_background.jpg"
    def gacha(self):
        try:
            jewel = gamescreen.load_jewel()
            if jewel < 10:
                raise Exception("Your jewel is/arn't enough")
            jewel -= 10
            result = None
            if result == None:
                result = "1 jewel"
                jewel += 1
            gamescreen.save_jewel(jewel)
            Popup(
                title="Gacha Result", 
                content=Label(text="You get" + result + "!"), 
                size_hint=(1, 0.2), 
                auto_dismiss=True
            ).open()
        except Exception as e:
            Popup(
                title='Gacha failed!', 
                content=Label(text=str(e)), 
                size_hint=(1, 0.2), 
                auto_dismiss=True
            ).open()
gachascreen = GachaScreen()

# 나머지 모음 화면
class OthersScreen(Screen):
    _bg_path = bg_folder + "/gacha_background.jpg"
    def on_pre_enter(self, *args):
        self.ids.useridlbl.text = str()
    def logout(self):
        self.ids.useridlbl.text = '0'
        usersDBinterface.logout()
        gamescreen.showMainScreen()
        gamescreen.goto_loginscreen()
    def showLangChanWin(self):
        self.add_widget(langchangewin)
    def hideLangChanWin(self):
        self.remove_widget(langchangewin)
othersscreen = OthersScreen()

class LangChangeWin(BoxLayout):
    def close(self):
        othersscreen.hideLangChanWin()
    def changelang(self):
        pass
langchangewin = LangChangeWin()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.ids.game_screen_manager.add_widget(mainscreen)
        self.ids.game_screen_manager.add_widget(lessonmapscreen)
        self.ids.game_screen_manager.add_widget(characterscreen)
        self.ids.game_screen_manager.add_widget(gachascreen)
        self.ids.game_screen_manager.add_widget(othersscreen)
    def on_pre_enter(self, **kwargs):
        self.load_money()
        self.load_jewel()
        mainscreen.show_random_chara()
    def goto_loginscreen(self):
        self.manager.current = "Login Screen"
    def goto_quizscreen(self, lessonmap, lesson):
        # self.manager.current = "Quiz Screen"
        pass
    def showMainScreen(self):
        self.ids.game_screen_manager.current = "Main Screen"
        mainscreen.show_random_chara()
    def showStageScreen(self):
        self.ids.game_screen_manager.current = "Lesson Map Screen"
    def showCharacterScreen(self):
        self.ids.game_screen_manager.current = "Character Screen"
    def showGachaScreen(self):
        self.ids.game_screen_manager.current = "Gacha Screen"
    def showOthersScreen(self):
        self.ids.game_screen_manager.current = "Others Screen"
    def load_money(self):
        money = usersDBinterface.get_money()
        self.ids.moneylabel.text = 'Money : ' + str(money)
        return money
    def load_jewel(self):
        jewel = usersDBinterface.get_jewel()
        self.ids.jewellabel.text = 'Jewel : ' + str(jewel)
        return jewel
    def save_money(self, money):
        usersDBinterface.put_money(money)
        self.ids.moneylabel.text = "Money : " + str(money)
    def save_jewel(self, jewel):
        usersDBinterface.put_jewel(jewel)
        self.ids.jewellabel.text = "Jewel : " + str(jewel)
gamescreen = GameScreen()