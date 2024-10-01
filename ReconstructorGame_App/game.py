from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from folder_paths import GUI_folder


Builder.load_file(GUI_folder + '/game_GUI.kv')

class GameScreen(Screen):
    pass
gamescreen = GameScreen(name='Game')