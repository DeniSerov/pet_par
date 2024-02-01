import json
import requests
import datetime
import os
import sys
from icecream import ic
import re
import lxml
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from logging.handlers import RotatingFileHandler
import logger
from typing import TypedDict, NotRequired





class anki_parser():
    def __init__(self):
        self.website = "" #https://www.wildberries.ru/
        self.zapros = ""
        self.driver = ""
        self.wait_marker = ""
        self.log = ""
        self.log_file = ""
        self.log_file_err = ""
        self.result = ""

    def init_rotating(self, filename, level=logging.INFO, prev_filename=None, log_name='log'):
        log_instance = logging.getLogger(log_name)
        if prev_filename is not None:
            for h in log_instance.handlers:
                h.flush()
                h.close()
                log_instance.removeHandler(h)
            os.rename(prev_filename, filename)
        log_instance.setLevel(level)
        handler = logging.handlers.RotatingFileHandler(filename, maxBytes=10000, backupCount=2)
        log_instance.addHandler(handler)
        return log_instance

    @classmethod
    def change_zapros(cls,zapros):
        cls.zapros = zapros # test "алмазная мозайка пейзаж 40х50" "ноутбук Hasee" "кошачий корм"

    def wait_load(self):
        wait = WebDriverWait(self.driver, timeout=20)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    def dowload_page(self,page_source):
        with open(self.web_name_short()+".html", "w", encoding="utf-8") as file_html:
            file_html.write(page_source)
        self.log_mes("Downloaded page")

    def web_name_short(self):
        return (self.website[self.website.find(".") + 1:self.website.rfind(".")])

    def connection(self):
        options = webdriver.FirefoxOptions() #options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
        #options.add_argument('--headless')  # видимость
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.website)
        self.wait_load()


    def start(self):
        try:
            self.log_mes("Start dowload head website")
            self.connection()
            self.log_mes("Got the main page, start pasring")
            self.body()
            self.log_mes("End pasring")
            self.exit()
            self.log_mes("End exit website")
        except:
            self.log_mes_err()
            self.exit()

    def log_mes_err(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        data_message = str(date) + " " + str(self.website) + " " + "Line_error = %s, type_error = %s" % (exc_traceback.tb_lineno, exc_value) + "\x0A"
        ic.disable()
        ic(data_message)
        self.log_file_err.error(data_message)

    def log_mes(self, message):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_message = str(date) + " " + str(self.website) + " " + str(message) + "\x0A"
        ic.enable()
        ic(data_message)
        self.log_file.info(msg = data_message)


    class product(TypedDict):
            site: str
            zapros: str
            result_name: str
            result_price : int
            result_href: str
            noch_file : NotRequired[dict]

    def exit(self):
        self.driver.close()
        self.driver.quit()

    @staticmethod
    def delete_con(*args):
        description_min_left = re.search(r"(?<=(\b))", args[0])
        description_min_middle = args[0][description_min_left.start():]
        description_min_rigt = re.search(r"(\W)*\Z", description_min_middle)
        description_mini = description_min_middle[:description_min_rigt.start()]
        if not description_mini:
            return args[0]
        return description_mini

    def body(self):
        pass
