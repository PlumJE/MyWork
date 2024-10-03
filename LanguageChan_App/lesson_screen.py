import random
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image

from folder_paths import GUI_folder

Builder.load_file(GUI_folder + '/lesson_screen_GUI.kv')

class LessonScreen(Screen):
    def __init__(self, **kwargs):
        super(LessonScreen, self).__init__(**kwargs)
lessonscreen = LessonScreen()