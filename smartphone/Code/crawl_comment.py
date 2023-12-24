import requests
import time
import random
import pandas as pd 
from tqdm import tqdm

cookies = {
    '_trackity': '9afd044c-9cae-3009-9c0d-412a7f6ff1c0',
    '_gcl_au': '1.1.371960065.1697628678',
     '_fbp': 'fb.1.1697628677871.635905542',
     '_hjSessionUser_522327': 'eyJpZCI6IjcxNDAyZDQyLTQ1ZmMtNWE2MS1hYzI2LTlhMjQyODFjZWUyOCIsImNyZWF0ZWQiOjE2OTc2Mjg2Nzc5NTMsImV4aXN0aW5nIjp0cnVlfQ==',
    '_ga': 'GA1.1.861403677.1696602514', 
    '_ga_GSD4ETCY1D': 'GS1.1.1697703823.6.0.1697703824.59.0.0',
    '_ga_NKX31X43RV': 'GS1.1.1697703823.6.0.1697703824.59.0.0', 
    'TOKENS' : '{%22customer_id%22:10898384%2C%22access_token%22:%22eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMDg5ODM4NCIsImlhdCI6MTcwMjk2MjEyOSwiZXhwIjoxNzAzMDQ4NTI5LCJpc3MiOiJodHRwczovL3Rpa2kudm4iLCJjdXN0b21lcl9pZCI6IjEwODk4Mzg0IiwiZW1haWwiOiJtYWl0aGlldTA1MDkwMy5tZnJAZ21haWwuY29tIiwiY2xpZW50X2lkIjoidGlraS1zc28iLCJuYW1lIjoiMTA4OTgzODQiLCJzY29wZSI6InNzbyJ9.znsfx7lVggUetee7tQHcqW5ficgYXd_KRHsSBl6vSIB0SdQ-L5vvyqilS2BMPlsiG8DeLWr1QpkkIskc39mjVv9DSAABXqCj4i3qj_2pnAbbpHO39ngHVRV0-5lN65sSP5bcnL2-mPFZ7FNd8IDJ_szdKVo0rtsbu9naN2Dc86RrNn45X-BukMNcBslJVMhl3paYBjUVKqw-XEJz11U0-mct0M4AKQl5_azWwU87uF-MWzliN9lLgEFlJiYR4J32GXMZZ2lYinjClo8W698P67nX4AUoIwQ-uvp8zqe_r9ae31ecC1uSDljKBowNtsrBC5AZ8uwPoeE0xSdXQIvpoz7XgRqnGzOVw4PPTc-cQP6bxQw95ycRlIfnCi2ccC7oFLgOYHhfyUH7XeBUuAwlHIcnNc7wHohmpmU4_CK8xGWiv413BaJlFgjYCjY284GeOH5nHmSXcTCbTDaL_WmLNN17zEIHM6qLpnFAnfeyBVJUixjcZ4NYWK3M3cwyYIgNOrt1qL7XGBhlnRnmN4tiSwURZO-k5D4LMog6VP0ep1Nb7YIPKYMBengfgXi1XODzmive47wQrShPBDOhvrNOr8nRqkHUuYyDdnZg66O8RNFaN34827lSET_XfQWcC29PUsZRRuYGkTsTJtPfv0GsKFEVOVXtLPFtu9c68HdShOM%22%2C%22token_type%22:%22bearer%22%2C%22refresh_token%22:%22TKIAfQW9ZehV79SMYQWSPmwjzZl_n4K5A9fqmnENTSc1napqk5ZA8bzihkOdb8YVIrw2Td3kkeElCqnnEdSy%22%2C%22expires_in%22:86400%2C%22expires_at%22:1703048529356}; TIKI_ACCESS_TOKEN=eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMDg5ODM4NCIsImlhdCI6MTcwMjk2MjEyOSwiZXhwIjoxNzAzMDQ4NTI5LCJpc3MiOiJodHRwczovL3Rpa2kudm4iLCJjdXN0b21lcl9pZCI6IjEwODk4Mzg0IiwiZW1haWwiOiJtYWl0aGlldTA1MDkwMy5tZnJAZ21haWwuY29tIiwiY2xpZW50X2lkIjoidGlraS1zc28iLCJuYW1lIjoiMTA4OTgzODQiLCJzY29wZSI6InNzbyJ9.znsfx7lVggUetee7tQHcqW5ficgYXd_KRHsSBl6vSIB0SdQ-L5vvyqilS2BMPlsiG8DeLWr1QpkkIskc39mjVv9DSAABXqCj4i3qj_2pnAbbpHO39ngHVRV0-5lN65sSP5bcnL2-mPFZ7FNd8IDJ_szdKVo0rtsbu9naN2Dc86RrNn45X-BukMNcBslJVMhl3paYBjUVKqw-XEJz11U0-mct0M4AKQl5_azWwU87uF-MWzliN9lLgEFlJiYR4J32GXMZZ2lYinjClo8W698P67nX4AUoIwQ-uvp8zqe_r9ae31ecC1uSDljKBowNtsrBC5AZ8uwPoeE0xSdXQIvpoz7XgRqnGzOVw4PPTc-cQP6bxQw95ycRlIfnCi2ccC7oFLgOYHhfyUH7XeBUuAwlHIcnNc7wHohmpmU4_CK8xGWiv413BaJlFgjYCjY284GeOH5nHmSXcTCbTDaL_WmLNN17zEIHM6qLpnFAnfeyBVJUixjcZ4NYWK3M3cwyYIgNOrt1qL7XGBhlnRnmN4tiSwURZO-k5D4LMog6VP0ep1Nb7YIPKYMBengfgXi1XODzmive47wQrShPBDOhvrNOr8nRqkHUuYyDdnZg66O8RNFaN34827lSET_XfQWcC29PUsZRRuYGkTsTJtPfv0GsKFEVOVXtLPFtu9c68HdShOM',
    'TIKI_USER': 'RJd4zCNM1FEcNBIR30J07jg0OjP24U6RdxsP6bFCCMkCUnVDHMbf%2Fo%2Bq3UyGz0RaK%2FBvU3wt1dZC',
    'bnpl_whitelist_info': '{%22content%22:%22Mua%20tr%C6%B0%E1%BB%9Bc%20tr%E1%BA%A3%20sau%22%2C%22is_enabled%22:true%2C%22icon%22:%22https://salt.tikicdn.com/ts/tmp/95/15/2d/4b3d64b220f55f42885c86ac439d6d62.png%22%2C%22deep_link%22:%22https://tiki.vn/mua-truoc-tra-sau/dang-ky?src=account_page%22}',
    'TIKI_RECOMMENDATION': 'b23098c3427cfcdbefb6ea910a017470',
    '_tuid': '10898384',
    'delivery_zone': 'Vk4wMzQwMjIwMTI=',
    'tiki_client_id': '861403677.1696602514',
    'TKSESSID': 'f790a1bc204398208df0c00c5098c91c', 
    'amp_99d374': 'W1zm2BXGrZtpOv-TK_uQUL.MTA4OTgzODQ=..1hi2n4e4a.1hi2n4lrc.97.cn.lu',
    '_hjIncludedInSessionSample_522327': '0', 
    '_hjSession_522327': 'eyJpZCI6ImUzZmUyMTFiLWFlZjgtNDEyZS1hZTM2LTI3MmYzZWFkYWQ5MSIsImMiOjE3MDMwNDU5MTI1NzksInMiOjAsInIiOjAsInNiIjowfQ==', 
    '_hjAbsoluteSessionInProgress': '0',
    'cto_bundle': 'bg7hIV93eFloMW9QenFxcTcyZWU2ekFhYnFQbiUyQiUyQmtHVU01Ym5pVHF5UU85aEhEZUVpVVBPUldNRjNoUllJU285NCUyQkM3STQxRjJOZFV4Y2dKWnpPdEdxSVQlMkZPY1VQWUZwRUMxb0JBbSUyQkw1cFJzcEVURWR2TmFKSG9nNDdPNlIlMkJVeE9YWFFPVWhKUGNoYlhDcmpRUDdIbnFHSVUxNVRqWFNQTWUlMkZ2WW93aXkyVyUyRnZldHRXWFdxNmhkJTJCNVJ0Mnc0SDA2dTNEazFaVVJ0cDVIQXhOVnZqZnVTcW1nJTNEJTNE',
    '_ga_S9GLR1RQFJ': 'GS1.1.1703045187.9.1.1703045944.21.0.0'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en,vi-VN;q=0.9,vi;q=0.8,en-US;q=0.7,fr-FR;q=0.6,fr;q=0.5',
    'Referer': 'https://tiki.vn/apple-iphone-15-p271966786.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_similar-products_UNK_similar-products-v1_202312180600_MD_batched_PID.271966790&itm_medium=CPC&itm_source=tiki-reco&spid=271966790',
    'Connection': 'keep-alive',
    'TE': 'Trailers'
}

params = {
    'sort': 'score|desc,id|desc,stars|all',
    'page': '1',
    'limit': '5',
    'include': 'comments,contribute_info,attribute_vote_summary'
}

df = pd.read_csv('D:/tiki crawl/smartphone/Data/par_id.csv')
pids = df.id.to_list()

def comment_parser(json):
    d = dict()
    d['product_id'] = json.get('product_id')
    d['title'] = json.get('title')
    d['content'] = json.get('content')
    d['thank_count'] = json.get('thank_count')
    d['customer_id']  = json.get('customer_id')
    d['rating'] = json.get('rating')
    d['created_at'] = json.get('created_at')
    d['customer_name'] = json.get('created_by').get('name')
    d['purchased_at'] = json.get('created_by').get('purchased_at')
    if json.get('timeline') is not None:
        d['delivery_date'] = json.get('timeline').get('delivery_date')
        d['review_created_date'] = json.get('timeline').get('review_created_date')
    return d


df_id = pd.read_csv('D:/tiki crawl/smartphone/Data/par_id.csv')
p_ids = df_id.id.to_list()
result = []
for pid in tqdm(p_ids, total=len(p_ids)):
    params['product_id'] = pid
    print('Crawl comment for product {}'.format(pid))
    for i in range(10):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/reviews', headers=headers, params=params, cookies=cookies)
        if response.status_code == 200:
            print('Crawl comment page {} success!!!'.format(i))
            for comment in response.json().get('data'):
                result.append(comment_parser(comment))
df_comment = pd.DataFrame(result)
df_comment.to_csv('comments_data.csv', index=False, encoding='utf-8-sig')