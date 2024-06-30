import requests
from bs4 import BeautifulSoup
import os
import json
def load_settings(file_path):
    with open(file_path, 'r') as file:
        settings = json.load(file)
    return settings

def correct_link ():

    file_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    
    # تحميل الإعدادات من الملف
    settings = load_settings(file_path)
    
    # قراءة الرابط من الإعدادات
    url = settings['url']
    #payload = {"s": search_query}
    response = requests.get(url,)# data=payload)
    response.raise_for_status()  # التحقق من نجاح الطلب

    # تحليل صفحة البحث باستخدام BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # العثور على الروابط الصحيحة
   # العثور على ul بعنصر class المطلوب
    download_div = soup.find('div', class_='Download--Wecima--Single')

    if download_div:
        # العثور على ul داخل هذا div
        ul = download_div.find('ul', class_='List--Download--Wecima--Single')
        
        if ul:
            # جلب جميع الروابط داخل هذا ul
            links = ul.find_all('a')
            
            # طباعة الروابط
            for link in links:
                href = link.get('href')
                print(href)
        else:
            print("لم يتم العثور على ul المطلوب.")
    else:
        print("لم يتم العثور على div المطلوب.")






correct_link()
