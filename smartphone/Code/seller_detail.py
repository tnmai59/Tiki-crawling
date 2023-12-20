from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

data = pd.read_csv('D:/tiki crawl/smartphone/Data/seller_unique.csv')
sids = data['seller_id'].to_list()
s_name = data['seller_name'].to_list()
surls = data['seller_url'].to_list()
store_info_url = []

for surl in surls:
    new_url = surl + '?t=storeInfo'
    store_info_url.append(new_url)

final = []

for i in range(len(store_info_url)):
    driver = webdriver.Chrome(service=Service('D:/tiki crawl/smartphone/Code/chromedriver.exe'))
    driver.get(store_info_url[i])
    elem = driver.find_element("xpath", "//*")
    source_code = elem.get_attribute("outerHTML")
    time.sleep(60)
    soup = BeautifulSoup(source_code, 'html.parser')

    label_list = []
    label = soup.find_all('span', class_="StoreInfo__InfoLabel-sc-1un24du-4 jpeWpY")
    for l in range(1, len(label), 2):
        key = label[l].get_text()
        label_list.append(key)
    print(f"Label: {label_list}")

    val_list = []
    value = soup.find_all('span', class_="StoreInfo__InfoValue-sc-1un24du-5 GxEKI")
    for v in range(len(value)):
        val = value[v].get_text()
        val_list.append(val)
    print(f"Value: {val_list}")

    info = dict()
    info['seller_id'] = sids[i]
    info['seller_name'] = s_name[i]
    info['seller_url'] = surls[i]
    for c in range(len(label_list)):
        key, val = label_list[c], val_list[c]
        info[key] = val
    
    print(f"Success {sids[i]}")
    final.append(info)
    driver.quit()

final_df = pd.DataFrame(final)
final_df.to_csv('D:/tiki crawl/smartphone/Data/seller_details.csv', index=False, encoding='utf-8-sig')

    