from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from login_screen import loginscreen
from game_screen import gamescreen
from quiz_screen import quizscreen

Window.clearcolor = (1, 1, 1, 1)

class LanguageChanApp(App):
    screen_manager = ScreenManager()
    def build(self):
        self.screen_manager.add_widget(loginscreen)
        self.screen_manager.add_widget(gamescreen)
        self.screen_manager.add_widget(quizscreen)
    
        return self.screen_manager
languagechanapp = LanguageChanApp()

if __name__ == "__main__":
    languagechanapp.run()
