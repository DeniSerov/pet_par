import time

from ancient_class import *
import undetected_chromedriver as uc
from fake_useragent import UserAgent


class YM_parser(anki_parser):
    def __init__(self):
        anki_parser.__init__(self)
        self.website = "https://www.YM.ru/"
        self.zapros = ""
        self.result = ""
        self.wait_marker = "YM"
        self.log = 'log/%s' % (self.web_name_short())
        self.log_file = self.init_rotating(filename='%s.log' % (self.log))
        self.log_file_err = self.init_rotating(filename='%s.err' % (self.log),level=logging.ERROR,log_name = "error")
        logging.basicConfig(filename='%s.err' % (self.log), level=logging.ERROR)

    def connection(self):
        response = requests.get(self.website, headers={'User-Agent': UserAgent().firefox})
        for key, value in response.request.headers.items():
            ic(key + ": " + value)

    def body(self):
        pass




a = YM_parser()
a.start()