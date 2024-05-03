from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from db_interface import userDBinter
from folder_paths import GUI_folder
from stages import stages

Builder.load_file(GUI_folder + 'game_screen_GUI.kv')
        
class MainScreen(Screen):
    pass
mainscreen = MainScreen()

class StageScreen(Screen):
    def __init__(self, **kwargs):
        super(StageScreen, self).__init__(**kwargs)
        datas = []
        for stage in stages:
            datas.append({'text':stage.name, 'on_release':stage.goto_stage})
            self.ids.stage_screen_manager.add_widget(stage)
        self.ids.stage_tabbar.data = datas
    def goto_quizscreen(self, language, level):
        gamescreen.goto_quizscreen(language, level)
stagescreen = StageScreen()

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
        self.ids.useridlbl.text = str(userDBinter.currentUserNum())
        return super().on_pre_enter(*args)
    def logout(self):
        userDBinter.currentUserNum(0)
        gamescreen.showMainScreen()
        gamescreen.goto_loginscreen()
    def showLangChanWin(self):
        self.add_widget(langchanwin)
    def hideLangChanWin(self):
        self.remove_widget(langchanwin)
optionscreen = OptionScreen()

class LangChanWin(BoxLayout):
    def close(self):
        optionscreen.hideLangChanWin()
    def changelang(self):
        pass
langchanwin = LangChanWin()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.ids.game_screen_manager.add_widget(mainscreen)
        self.ids.game_screen_manager.add_widget(stagescreen)
        self.ids.game_screen_manager.add_widget(characterscreen)
        self.ids.game_screen_manager.add_widget(gachascreen)
        self.ids.game_screen_manager.add_widget(optionscreen)
    def on_pre_enter(self, *args):
        self.ids.moneylabel.text = "Money : " + str(userDBinter.selectUsersMoney())
        self.ids.jewellabel.text = "Jewel : " + str(userDBinter.selectUsersJewel())
        return super().on_enter(*args)
    def goto_loginscreen(self):
        self.manager.current = "Login Screen"
    def goto_quizscreen(self, language, level):
        self.manager.current = "Quiz Screen"
        print("language :", language, "level :", level)
    def showMainScreen(self):
        self.ids.game_screen_manager.current = "Main Screen"
    def showStageScreen(self):
        self.ids.game_screen_manager.current = "Stage Screen"
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
