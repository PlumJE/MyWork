import logging

class Log:
    ger = logging.getLogger()
    def __init__(self):
        self.ger.setLevel(logging.INFO)
        self.ger.addHandler(logging.FileHandler("apps_log.log"))
log = Log()