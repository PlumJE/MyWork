"""
작성자 : 외기러기
작성시작일 : 2024-09-24
버전 정보 : 1.0.0 at 0000-00-00
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""


from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from game import gamescreen
from story import storyscreen
from folder_paths import GUI_folder, graphics_folder


Builder.load_file(GUI_folder + '\main_GUI.kv')

class StartScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(StartScreen, self).__init__(*args, **kwargs)
        self.bg_img = graphics_folder + '\start.png'
    def game_start(self, *args, **kwargs):
        self.manager.current = 'Game over'# 'Story'
startscreen = StartScreen(name='Start')

class GameOverScreen(Screen):
    def game_restart(self, *args, **kwargs):
        self.manager.current = 'Start'
gameoverscreen = GameOverScreen(name='Game over')

class EndScreen(Screen):
    def game_restart(self, *args, **kwargs):
        self.manager.current = 'Start'
endscreen = EndScreen(name='End')

class ReconstructorGame_App(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screenmanager = ScreenManager()
    def build(self):
        self.screenmanager.add_widget(startscreen)
        self.screenmanager.add_widget(storyscreen)
        self.screenmanager.add_widget(gamescreen)
        self.screenmanager.add_widget(gameoverscreen)
        self.screenmanager.add_widget(endscreen)
        return self.screenmanager
reconstructorgame_app = ReconstructorGame_App()

if __name__ == '__main__':
    try:
        reconstructorgame_app.run()
    except Exception as e:
        print(e)