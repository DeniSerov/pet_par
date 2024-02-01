from ancient_class import *
import time
import undetected_chromedriver as uc # обходим защиту от парсинга
from fake_useragent import UserAgent

class OZ_parser(anki_parser):
    def __init__(self):
        anki_parser.__init__(self)
        self.website = "https://www.OZ.ru/" 
        self.zapros = "алмазная мозайка пейзаж 40х50"
        self.result = ""
        self.wait_marker = "ozon"
        self.log = 'log/%s' % (self.web_name_short())
        self.log_file = self.init_rotating(filename='%s.log' % (self.log))
        self.log_file_err = self.init_rotating(filename='%s.err' % (self.log),level=logging.ERROR,log_name = "error")
        logging.basicConfig(filename='%s.err' % (self.log), level=logging.ERROR)

    def connection(self):
        options = uc.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
        # options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        options.headless = False
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(options=options,driver_executable_path='/Chrome_driver/...')
        self.driver.get(self.website)
        self.wait_load()

    def body(self):
        class pod_product(TypedDict, total=True):
            id: int
            name: str
            price: int
            href: str
            naeb_price: int

        minimal_price = 0
        tech_min_price = [0, 0, 0]
        pod_result_dict = []
        ic.enable()
        #увеличить время между запросами?
        if (EC.presence_of_element_located((By.CLASS_NAME, "tc"))):
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rb")))
            time.sleep(2)
            self.driver.find_element(By.CLASS_NAME, "rb").send_keys(self.zapros)
            page_source = self.driver.page_source
            self.dowload_page(page_source)
            self.website = "https://www.OZ.ru/" 
        page_source = self.driver.page_source
        self.dowload_page(page_source)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jg6")))
        self.driver.find_element(By.ID, "wv6").send_keys(self.zapros)
        self.log_mes("Запрос прошел успешно")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'ag15-a')))
        self.driver.find_element(By.ID, "ag15-a").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "wv6")))
        page_source = self.driver.page_source
        self.dowload_page(page_source)

a = OZ_parser()
a.start()