#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

USERNAME = 'scorpinok'
url_to_get = f'https://api.github.com/users/{USERNAME}/repos'

res_req = requests.get(url_to_get)

repos_list = [i['name'] for i in res_req.json()]

jf_name = f'repos_for_{USERNAME}.json'

with open(jf_name, 'w', encoding='UTF-8') as res_f:
    json.dump(repos_list, res_f)

json_string = json.dumps(repos_list, indent=4, ensure_ascii=False)
print(f'Содержимое json файла: \n {json_string}')

with open(jf_name, 'r', encoding='UTF-8') as res_f:
    print(f"Считали файл json:\n{json.load(res_f)}")



