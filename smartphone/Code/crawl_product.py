import requests
import time
import random
import pandas as pd
import json
import numpy as np

cookies = {'_trackity': '9afd044c-9cae-3009-9c0d-412a7f6ff1c0',
           'TOKENS': '{%22access_token%22:%22mtr6lHNEYZiRW9XJGI4qupQboSCMkO87%22}',
           'TIKI_RECOMMENDATION': '789ad5629a84602eb6470c00ff25ac05',
           '_ga': 'GA1.2.861403677.169',
           '_gid': 'GA1.2.1691243548.1696602',
           'amp_99d374': 'W1zm2BXGrZtpOv-TK_uQUL...1hc2m7o37.1hc2m7qa2.8.b.j',
           'delivery_zone': 'Vk4wMzQwMjQwMTM=',
           'TKSESSID': '0133cfaf4691695aa95374e2ff57fc56'}

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en,vi-VN;q=0.9,vi;q=0.8,en-US;q=0.7,fr-FR;q=0.6,fr;q=0.5',
    # 'Referer': 'https://tiki.vn/apple-iphone-14-pro-max-p197216291.html?',
    'X-Guest-Token': 'mtr6lHNEYZiRW9XJGI4qupQboSCMkO87',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params1 = {
    'platform': 'web',
    'version': '3'
}

df = pd.read_csv('D:/tiki crawl/smartphone/Data/par_id.csv')
pids = df.id.to_list()

result = []
product = []

for pid in pids:
    response = requests.get('https://tiki.vn/api/v2/products/{}'.format(pid), headers=headers1, params=params1, cookies=cookies)
    if response.status_code == 200:
        # jfile = response.json()
        if response.content != None and response.headers["content-type"].strip().startswith("application/json"):
            jfile = json.loads(response.content, strict = False)
        else:
            continue

        # Crawl vòng ngoài
        out_prod = dict()
        out_prod['product_id'] = pid
        out_prod['product_name'] = jfile.get('name')
        out_prod['product_brand'] = jfile.get('brand').get('name')
        if jfile.get('categories') != None:
            out_prod['product_category'] = jfile.get('categories').get('name')
        else:
            out_prod['product_category'] = np.nan
        out_prod['product_url'] = 'https://tiki.vn/' + str(jfile.get('url_key')) + '.html?'
        out_prod['product_rating'] = jfile.get('rating_average')
        if jfile.get('quantity_sold') is not None: 
            out_prod['product_num_sell'] = jfile.get('quantity_sold').get('value')
        out_prod['prod_num_rating'] = jfile.get('review_count')
        if jfile.get('warranty_info') is not None: 
            if len(jfile.get('warranty_info')) > 0:
                out_prod['warranty_period'] = jfile.get('warranty_info')[0].get('value')
        out_prod['return_policy'] = jfile.get('return_and_exchange_policy')
        if jfile.get('current_seller') is not None: 
            out_prod['seller_id'] = jfile.get('current_seller').get('id')
            out_prod['seller_name'] = jfile.get('current_seller').get('name')
            out_prod['seller_url'] = jfile.get('current_seller').get('link')

        specs = jfile.get('specifications')
        if specs is not None:
            for spec in specs:
                if spec.get('name') == 'Content':
                    atts = spec.get('attributes')
                    for att in atts:
                        key = att.get('code')
                        val = att.get('value')
                        out_prod[key] = val
                    break
        product.append(out_prod)

        # Crawl các sản phẩm con
        temp = jfile.get('configurable_products')
        if temp is not None:
            for t in temp:
                d = dict()
                d['product_id'] = pid
                child_id = t.get('id')
                if t.get('option1') is not None: 
                    d['product_color'] = t.get('option1')
                if t.get('option2') is not None:
                    d['product_capacity'] = t.get('option2')
                d['product_price'] = t.get('price')
                d['product_url'] = 'https://tiki.vn/' + str(jfile.get('url_key')) + '.html?spid=' + str(child_id)
                d['product_image'] = t.get('images')
                # d['seller_id'] = jfile.get('current_seller').get('id')
                # d['seller_name'] = jfile.get('current_seller').get('name')
                # d['seller_url'] = jfile.get('current_seller').get('link')
                result.append(d)
            
        # else:
        #     print(f'{pid} is Null')
        #     d = dict()
        #     d['par_id'] = pid
        #     d['product_id'] = jfile.get('id')
        #     d['product_name'] = jfile.get('name')
        #     d['product_price'] = jfile.get('price')
        #     d['product_brand'] = jfile.get('brand').get('name')
        #     if jfile.get('categories') != None:
        #         d['product_category'] = jfile.get('categories').get('name')
        #     else:
        #         d['product_category'] = np.nan
        #     d['product_url'] = 'https://tiki.vn/' + str(jfile.get('url_path'))
        #     d['prod_rating'] = jfile.get('rating_average')
        #     d['prod_num_rating'] = jfile.get('review_count')
        #     d['prod_image'] = jfile.get('images')
        #     d['seller_id'] = jfile.get('current_seller').get('id')
        #     d['seller_name'] = jfile.get('current_seller').get('name')
        #     d['seller_url'] = jfile.get('current_seller').get('link')
        #     print(f'{pid} crawled')
        print(f'Crawled successfully {pid}')
    else:
        print(response.status_code)



output1 = pd.DataFrame(result)
output1[['product_id', 'product_image']].to_csv('D:/tiki crawl/smartphone/Data/images.csv', index=False, encoding='utf-8-sig')
output1.drop(columns='product_image').to_csv('D:/tiki crawl/smartphone/Data/product_details.csv', index=False, encoding='utf-8-sig')

output2 = pd.DataFrame(product)
output2[['seller_id', 'seller_name', 'seller_url']].to_csv('D:/tiki crawl/smartphone/Data/seller.csv', index=False, encoding='utf-8-sig')
output2.drop(columns=['seller_name', 'seller_url']).to_csv('D:/tiki crawl/smartphone/Data/products.csv', index=False, encoding='utf-8-sig')

