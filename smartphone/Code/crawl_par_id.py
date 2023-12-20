import requests
import time
import random
import pandas as pd

params = {'limit': '40',
           'include': 'advertisement',
           'aggregations': '2',
           'version': 'home-personalized',
           'trackity_id': '9afd044c-9cae-3009-9c0d-412a7f6ff1c0',
           'category': '1795',
           'page': '1',
           'urlKey': 'dien-thoai-smartphone'}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en,vi-VN;q=0.9,vi;q=0.8,en-US;q=0.7,fr-FR;q=0.6,fr;q=0.5',
    'Referer': 'https://tiki.vn/dien-thoai-smartphone/c1795',
    'X-Guest-Token': 'mtr6lHNEYZiRW9XJGI4qupQboSCMkO87',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

product_id = []
for i in range(1, 17):
    params['page'] = i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings?', headers=headers, params=params)#, cookies=cookies)
    # print(response.status_code)
    if response.ok:
        print('request success!!!')
        for record in response.json().get('data'):
            product_id.append({'id': str(record.get('id'))})
    else: 
        print(response.status_code)
    time.sleep(random.randrange(3, 10))

par_id = pd.DataFrame(product_id)
par_id.to_csv('D:/tiki crawl/smartphone/Data/par_id.csv', index=False)