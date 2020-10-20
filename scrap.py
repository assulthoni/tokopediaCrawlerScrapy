from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
import pandas as pd


class ScrapTokopedia(object):
    def __init__(self, DRIVERPATH, page):
        self.driver = None
        self.books = None
        self.dataframe = pd.DataFrame(columns=['title', 
        'price', 'sold','condition', 'assurance', 'weight',
        'seller', 'description'])
        self.page = page

    def driverActivate(self, DRIVERPATH):
        option = Options()
        
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2 
        })
        
        webdriver_path = DRIVERPATH
        driver = webdriver.Chrome(options=option,executable_path=webdriver_path)
        driver.maximize_window()
        return driver

    def driverGET(self, url):
        self.driver.get(url)

    def driverBack(self):
        self.driver.back()

    def driverWaitAllElementsPresence(self, time=10, BY=By.CLASS_NAME, identifier='None'):
        element = WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located((BY,identifier))
        )
        return element

    def driverWaitElementPresence(self, time=10, BY=By.CLASS_NAME, identifier='None'):
        element = WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located((BY,identifier))
        )
        return element
    def scrollPage(self, identifier='e1nlzfl3', BY=By.CLASS_NAME):
        while True:
            self.driver.execute_script('arguments[0].scrollIntoView();', self.books[-1])
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda driver: len(
                        WebDriverWait(driver, 15).until(
                            EC.presence_of_all_elements_located((BY,identifier))
                            )
                    )> len(self.books)
                    )
                self.books = self.driverWaitAllElementsPresence(time=10, 
                BY=By.CLASS_NAME, identifier=identifier)
            except:
                break

    def screenshotImage(self):
        element = self.driverWaitElementPresence(
            time=10, BY=By.CLASS_NAME, identifier="css-1ans2w0 e18n9kgb0"
        )
        image_url = element.find_elements_by_class_name("success fade").get_attributes('src')
        image_name = element.find_elements_by_class_name("success fade").get_attributes('alt')
        self.driverGET(image_url)
        self.driver.save_screenshot(os.path.join('image', image_name+'.png'))
        self.driverBack()

    def process(self):
        links = []
        for book in self.books:
            link = book.find_element_by_class_name('css-89jnbj')
            links.append(link.get_attribute('href'))

        print("LINK GOT :",len(links))
        counter = 0
        for link in links:
            counter += 1
            print(counter)
            data = {}
            try:
                self.driverGET(link)    
                time.sleep(15)
                element = self.driverWaitElementPresence(
                    time=10, BY=By.XPATH,
                    identifier='//*[contains(concat( " ", @class, " " ), concat( " ", "css-x7lc0h", " " ))]'
                )
                # basic information
                title = element.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "css-x7lc0h", " " ))]').text
                price = element.find_element_by_xpath('//h3[@data-testid="lblPDPDetailProductPrice"]').text
                sold = element.find_element_by_xpath('//*[@data-testid="lblPDPDetailProductSuccessRate"]').text
                condition = element.find_element_by_xpath('//p[@data-testid="PDPDetailConditionValue"]').text
                assurance = element.find_element_by_xpath('//p[@data-testid="PDPInfoInsuranceValue"]').text
                weight = element.find_element_by_xpath('//p[@data-testid="PDPDetailWeightValue"]').text
                seller = element.find_element_by_xpath('//*[@data-testid="llbPDPFooterShopName"]').text
                print(title, price, sold, condition, assurance,weight, seller)

                # deep information 
                time.sleep(0.1)
                image_div = element.find_element_by_xpath('//div[@class="css-10tfci1 ew904gd0"]/div[@class="css-1ans2w0 e18n9kgb0"]/img[@class="success fade"]')
                image_url = image_div.get_attribute('src')
                image_name = image_div.get_attribute('alt')
                self.driverGET(image_url)
                self.driver.save_screenshot(
                    os.path.join('image', "("+str(self.page)+'-'+str(counter)+")"+image_name+'.png')
                    )
                self.driverBack()
                time.sleep(3)

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
                time.sleep(5)
                element = self.driverWaitElementPresence(
                    time=15, BY=By.XPATH, identifier='//*[@data-testid="lblPDPDeskripsiProduk"]'
                )
                description = element.find_element_by_xpath('//*[@data-testid="lblPDPDeskripsiProduk"]').text

                data['title'] = title
                data['price'] = price
                data['sold'] = sold
                data['condition'] = condition
                data['assurance'] = assurance
                data['weight'] = weight
                data['seller'] = seller
                data['description'] = description
                
                time.sleep(15)
                self.driverBack()
            except :
                time.sleep(30)
                self.driverBack()
            self.dataframe = self.dataframe.append(data, ignore_index=True)
    def main(self, BASE_URL):
        self.driver = self.driverActivate(DRIVERPATH)
        self.driverGET(BASE_URL)
        self.books = self.driverWaitAllElementsPresence(time=10, 
                BY=By.CLASS_NAME, identifier='e1nlzfl3')
        self.scrollPage(identifier='e1nlzfl3')
        self.process()
        self.dataframe.to_csv(os.path.join('csv file','scrap page '+str(self.page)+'.csv'))
        self.driver.quit()

if __name__ == "__main__":
    DRIVERPATH = "D:/kuliah/TUGAS AKHIR/SCRAPING TOKOPEDIA/chromedriver.exe"
    BASE_URL = r'https://www.tokopedia.com/p/buku/komputer-internet/buku-programming?page={pagenum}'
    page = 20
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    print("Start Current Time =", current_time)
    for p in range(11, page+1):
        try:
            start = time.time()
            scraper = ScrapTokopedia(DRIVERPATH, p)
            URL = BASE_URL.format(pagenum=p)
            scraper.main(URL)
            print(f"SCRAPING PAGE {p} SUCCESSFUL!!!")
            end = time.time()
            elapsed_time = end - start
            print(f"Time elapsed = {elapsed_time}")
        except:
            pass
    all_end_time = time.localtime()
    current_time = time.strftime("%H:%M:%S", all_end_time)
    print("Start Current Time =", current_time)