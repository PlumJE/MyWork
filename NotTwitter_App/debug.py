import logging

# logger객체 생성
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# logger의 로그를 파일에 저장하게 설정
file_handler = logging.FileHandler("apps_log.log")
logger.addHandler(file_handler)
