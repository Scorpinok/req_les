from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

driver = webdriver.Chrome('/Users/vladimirpolishchuk/Downloads/chromedriver')

driver.get('https://account.mail.ru/login')

login = 'study.ai_172'
password = 'NextPassword172#'

driver.implicitly_wait(5)
mail_name = driver.find_element_by_xpath('//input[@name="username"]')
mail_name.send_keys(login)
mail_name.send_keys(Keys.ENTER)

driver.implicitly_wait(5)
field_passwd = driver.find_element_by_xpath('//input[@name="password"]')
field_passwd.send_keys(password)
field_passwd.send_keys(Keys.ENTER)

driver.implicitly_wait(20)
WebDriverWait(driver, timeout=15).until(EC.presence_of_element_located((By.CLASS_NAME, 'contract-trigger')))

emails_links_list = []
item = None
last = -1

while last is not None:
    driver.implicitly_wait(10)
    for i in driver.find_elements(*(By.TAG_NAME, 'a')):
        try:
            if '/inbox/0' in str(i.get_attribute('href')):
                emails_links_list.append(i.get_attribute('href'))
                item = i
        except:
            pass

    last = None if last == item else item

    if last is not None:
        last.send_keys(Keys.PAGE_DOWN)
        driver.implicitly_wait(7)

client = MongoClient('127.0.0.1', 27017)

mongo_db = client["mails_db"]
mongo_col = mongo_db["mailru_mails"]

for i in range(len(emails_links_list)):
    driver.get(emails_links_list[i])

    theme = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'thread-subject'))).text
    from_who = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))).text
    date = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))).text
    driver.implicitly_wait(10)
    text_mail = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__body'))).get_attribute('innerHTML')

    mongo_col.update_one({"Отправитель": from_who,
                                  "Дата": date,
                                  "Тема": theme,
                                  "Текст": text_mail},
                             { "$set":{"Отправитель": from_who,
                                  "Дата": date,
                                  "Тема": theme,
                                  "Текст": text_mail}}, upsert=True)


count = 0

for x in mongo_col.find():
    count += 1
    print(x)

print(f'\nОбщее число записей в базе: {count}')

driver.close()