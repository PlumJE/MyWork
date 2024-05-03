from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from db_interface import stageDBinter
from folder_paths import GUI_folder, bg_folder

Builder.load_file(GUI_folder + 'stages_GUI.kv')

class StageTemplate(Screen):
    buttons = 0
    def __init__(self, language, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.name = language
        self.ids.stage_bg.source = bg_folder + str(language) + "_stage_bg.jpg"
    def setButton(self, x, y):
        self.buttons += 1
        button = ButtonTemplate(level=str(self.buttons), size_hint=(0.2, 0.1), pos=(x, y))
        self.ids.button_field.add_widget(button)
    def goto_stage(self):
        self.manager.current = str(self.name)
    def goto_quiz(self, level):
        self.parent.parent.parent.goto_quizscreen(str(self.name), int(level))

class ButtonTemplate(Button):
    level = 0
    def __init__(self, level, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.level = int(level)
        self.text = "Level " + str(level)
        self.on_release = self.goto_quiz
    def goto_quiz(self):
        self.parent.parent.parent.goto_quiz(int(self.level))

english_stage = StageTemplate("english")
english_stage.setButton(10, 30)

chinese_stage = StageTemplate("chinese")
chinese_stage.setButton(20, 40)

stages = [english_stage, chinese_stage]
