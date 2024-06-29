import io
import logging
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

# logger객체 생성
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# logger의 로그를 파일에 저장하게 설정
file_handler = logging.FileHandler("apps_log.log")
logger.addHandler(file_handler)

# 현재 로그인한 유저의 번호를 저장
class CurUsernum:
    usernum = 0
    def set(self, usernum):
        assert type(usernum) == int
        self.usernum = usernum
        return self.usernum
    def get(self):
        return self.usernum
    def init(self):
        self.usernum = 0
        return self.usernum
cur_usernum = CurUsernum()

# 바이너리를 이미지로 변환
class TransImgBi:
    def bi_to_img(self, bi, ext):
        buf = io.BytesIO(bi)
        cim = CoreImage(buf, ext=ext)
        return Image(texture=cim.texture)
transimg = TransImgBi()