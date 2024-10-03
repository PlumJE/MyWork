"""
작성자 : 외기러기
작성시작일 : 2024-01-01
버전 : 0.0
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""


from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from login_screen import loginscreen
from game_screen import gamescreen
from lesson_screen import lessonscreen
from debug import logger

Window.clearcolor = (1, 1, 1, 1)
Window.size = (375, 750)    # 내 폰(갤럭시 퀀텀)과 비슷하게 기준잡음

# 앱 전체를 나타내는 클래스
class LanguageChanApp(App):
    screen_manager = ScreenManager()
    def build(self):
        self.screen_manager.add_widget(loginscreen)
        self.screen_manager.add_widget(gamescreen)
        self.screen_manager.add_widget(lessonscreen)
        return self.screen_manager
languagechanapp = LanguageChanApp()

# 앱 실행
if __name__ == "__main__":
    try:
        languagechanapp.run()
    except Exception as e:
        logger.critical('Leathal error has occured! ' + str(e))