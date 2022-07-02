from bs4 import BeautifulSoup
import requests
import unicodedata
import pandas as pd

text_to_url = 'python'

url = f'https://russia.superjob.ru/vacancy/search/'

session = requests.Session()
params = {'keywords': text_to_url, 'page': ''}
response = session.get(url, params=params)

res_html = BeautifulSoup(response.text, 'html.parser')

vac_name = res_html.find_all('span', class_='_37mRb z4PWH _2Rwtu')
vac_sal = res_html.find_all('span', class_='_4Gt5t f-test-text-company-item-salary')

names = [vac_name[i].text for i in range(len(vac_name))]
salary_min = [unicodedata.normalize("NFKD",vac_sal[i].text[-25:-10])[3:] if unicodedata.normalize("NFKD",vac_sal[i].text[-25:-10])[3:] != 'дого' else None for i in range(len(vac_sal))]
sal_val = [vac_sal[i].text[-10:-7] if vac_sal[i].text[-10:-7] != 'вор' else None for i in range(len(vac_sal))]
links = [url+vac_name[i].find('a').get('href') for i in range(len(vac_name))]

pages = res_html.find_all('span', class_='_28Wuq KNGBZ _4N0O3 _3lqNe _27m6C _R43B')
if len(pages):
    page_nums = int(pages[len(pages)-2].text)

    for i in range(2, page_nums):
        params = {'keywords': text_to_url, 'page': i}
        response = session.get(url, params=params)

        res_html = BeautifulSoup(response.text, 'html.parser')

        vac_name = res_html.find_all('span', class_='_37mRb z4PWH _2Rwtu')
        vac_sal = res_html.find_all('span', class_='_4Gt5t f-test-text-company-item-salary')

        names = names + [vac_name[i].text for i in range(len(vac_name))]
        salary_min = salary_min + [unicodedata.normalize("NFKD", vac_sal[i].text[-25:-10])[3:] if unicodedata.normalize("NFKD",vac_sal[i].text[-25:-10])[3:] != 'дого' else None for i in range(len(vac_sal))]
        sal_val = sal_val + [vac_sal[i].text[-10:-7] if vac_sal[i].text[-10:-7] != 'вор' else None for i in range(len(vac_sal))]
        links = links + [url + vac_name[i].find('a').get('href') for i in range(len(vac_name))]


sal_min = []
sal_max = []
for i in salary_min:
    if i:
        if i.find('—'):
            sal_min.append(i.split('—')[0].strip())
            if len(i.split('—')) > 1:
                sal_max.append(i.split('—')[1].strip())
            else:
                sal_max.append(None)
        else:
            sal_min.append(i)
            sal_max.append(None)
    else:
        sal_max.append(None)
        sal_min.append(None)


res_df = pd.DataFrame({"Название": names,
                   "Зарплата_мин": sal_min,
                    "Зарплата_макс": sal_max,
                   "Валюта": sal_val,
                   "Ссылка": links,
                   })

res_df.to_csv("res_file.csv")
