from ancient_class import *

#_dataClass = ancient_class.anki_parser()
# пользуем BS4 для парсинга

class WB_parser(anki_parser):
    def __init__(self):
        anki_parser.__init__(self)
        self.website = "https://www.WB.ru/"  #
        self.zapros = "алмазная мозайка пейзаж 40х50"  # test "алмазная мозайка пейзаж 40х50" "ноутбук Hasee" "кошачий корм"
        self.result = ""
        self.wait_marker = "WB"
        self.log = 'log/%s' % (self.web_name_short())
        self.log_file = self.init_rotating(filename='%s.log' % (self.log))
        self.log_file_err = self.init_rotating(filename='%s.err' % (self.log),level=logging.ERROR,log_name = "error")
        logging.basicConfig(filename='%s.err' % (self.log), level=logging.ERROR)

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
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-card__wrapper")))
        self.driver.find_element(By.ID, "searchInput").send_keys(self.zapros)
        self.log_mes("Запрос прошел успешно")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'applySearchBtn')))
        self.driver.find_element(By.ID, "applySearchBtn").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "searching-results__text")))
        page_source = self.driver.page_source
        self.dowload_page(page_source)
        soup = BeautifulSoup(page_source, 'lxml')
        with open("wb.json", "w") as tech_file:
            for i in range(len(soup.findAll('article')) - 1):
                tmp_elemet = soup.findAll('article')[i].contents[0]
                description = re.search(r"(?<=<img alt).*?(?=class=)", str(tmp_elemet))
                if not description:
                    description = re.search(r"(?<=aria-label=).*?(?=class=)", str(tmp_elemet))
                description_mini = self.delete_con(description[0])
                price = re.search(r"(?<=price__lower-price).*?(?=</ins>)", str(tmp_elemet))
                if price:
                    price_mini = self.delete_con(price[0])
                    price_mini = ''.join([i for i in price_mini if i.isnumeric()])
                else:
                    continue # если нет цены - значит отсуствует товар или не доставляется
                    #price_mini = 0
                nayeb_price = re.search(r"(?<=<del>).*?(?=</del>)", str(tmp_elemet))
                if nayeb_price:  # не у всех есть скидки
                    nayeb_price_mini = self.delete_con(nayeb_price[0]).replace(" ", "")
                    nayeb_price_mini = ''.join([i for i in nayeb_price_mini if i.isnumeric()])
                else:
                    nayeb_price_mini = 0
                href_tmp = re.search(
                    r'''(?<=class="product-card__link j-card-link j-open-full-product-card").*?(?=target="_blank")''',
                    str(tmp_elemet))
                href = re.search(r'''(?<=href=).*?''', str(href_tmp[0]))
                href_mini = self.delete_con(href_tmp[0][href.start():])
                if (minimal_price > int(price_mini) or minimal_price == 0) and int(price_mini) != 0:
                    minimal_price = int(price_mini)
                    for i_param, tmp in enumerate([description_mini, price_mini, href_mini]):
                        tech_min_price[i_param] = tmp
                ic(i, description_mini, price_mini, nayeb_price_mini, href_mini)
                tmp : pod_product = {"id": i, "name": description_mini,"price": price_mini,"href": href_mini,"naeb_price": nayeb_price_mini}
                pod_result_dict.append(tmp)
        ic("Самый дешевый вариант по запросу %s" % (self.zapros), tech_min_price)
        self.result: anki_parser.product = {"site": self.web_name_short(), 'zapros': self.zapros, "result_name": tech_min_price[0],"result_price": int(tech_min_price[1]),
                           "result_href": tech_min_price[2],"noch_file": pod_result_dict}
        ic(self.result)

a = WB_parser()
a.start()