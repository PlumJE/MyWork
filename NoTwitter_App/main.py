"""
작성자 : 외기러기
작성시작일 : 2024-03-05
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from login_screen import loginscreen
from post_screen import postscreen
from edit_screen import editscreen
from setting_screen import settingscreen
from others import logger
from traceback import format_exc

class LoginPostingApp(App):
    screen_manager = ScreenManager()
    # 앱 전체를 만들어서 리턴한다
    def build(self):
        self.screen_manager.add_widget(loginscreen)
        self.screen_manager.add_widget(postscreen)
        self.screen_manager.add_widget(editscreen)
        self.screen_manager.add_widget(settingscreen)
        return self.screen_manager

if __name__ == "__main__":
    try:
        LoginPostingApp().run()
        logger.info("")
    except:
        logger.critical(format_exc())