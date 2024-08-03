"""
작성자 : 외기러기
작성시작일 : 2024-05-03
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""

import logging
from random import choice
from traceback import format_exc

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('main_GUI.kv')


# logger객체 생성
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# logger의 로그를 파일에 저장하게 설정
file_handler = logging.FileHandler("apps_log.log")
logger.addHandler(file_handler)

# 앱의 핵심 부분을 나타내는 클래스
class PswdMakerCore(BoxLayout):
    def include_candidates(self):
        result = ''
        if self.ids.upper_toggle.state == 'down':
            result += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if self.ids.lower_toggle.state == 'down':
            result += 'abcdefghijklmnopqrstuvwxyz'
        if self.ids.number_toggle.state == 'down':
            result += '0123456789'
        if self.ids.special_toggle.state == 'down':
            result += '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

        logger.info("include : "+result)

        if result != '':
            return result
        else:
            return None
    def exclude_candidates(self, candidates):
        excludes = self.ids.exclude_textinput.text

        logger.info("exclude : "+excludes)

        if excludes == '' or not excludes.isspace():
            for char in excludes:
                candidates = candidates.replace(char, '')
            return candidates
        else:
            return None
    def set_length(self):
        try:
            result = int(self.ids.length_textinput.text)
            if result < 1:
                result = 1
            return result
        except:
            return None
    def generate_password(self):
        pswd_candidates = self.include_candidates()
        if pswd_candidates == None:
            Popup(title='Error!', content=Label(text="Ye must include at least one character type."), size_hint = (1, 0.2), auto_dismiss = True).open()
            return
        
        pswd_candidates = self.exclude_candidates(pswd_candidates)
        if pswd_candidates == None:
            Popup(title='Error!', content=Label(text="Ye must exclude valid character type."), size_hint = (1, 0.2), auto_dismiss = True).open()
            return
        
        logger.info("pswd candidates : "+pswd_candidates)

        length = self.set_length()
        if length == None:
            Popup(title='Error!', content=Label(text="The length must be valid integer."), size_hint = (1, 0.2), auto_dismiss = True).open()
            return
        
        password = ''
        for i in range(length):
            password += choice(pswd_candidates)
        self.ids.result_textinput.text = password


# 앱 전체를 나타내는 클래스
class PswdMakerApp(App):
    def build(self):
        return PswdMakerCore()

if __name__ == "__main__":
    try:
        PswdMakerApp().run()
        logger.info("")
    except:
        logger.critical(format_exc())
