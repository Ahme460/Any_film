import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests
from bs4 import BeautifulSoup

def read_file(self):
    with open('arbic.json', 'r', encoding='utf-8') as file:

        movie_links = json.load(file)
    return movie_links


def search_movie_link(movie_dict, movie_name):

    matches = process.extract(movie_name, movie_dict.keys(), limit=3, scorer=fuzz.token_set_ratio)
    best_match = None
    for match in matches:
        name, score = match
        if score > 70:
            best_match = name
            break
    
    # إذا تم العثور على تطابق جيد، إرجاع الرابط
    if best_match:
        return  movie_dict[best_match]
    else:
        return "الفيلم غير موجود في القاموس أو لا يوجد تطابق قريب."

# طلب اسم الفيلم من المستخدم
user_input = input("من فضلك أدخل اسم الفيلم: ")

# البحث وعرض الرابط
result = search_movie_link(self.read_file(), user_input)
print(result)








def links_download():
    url= result
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


#############
        #############
        ###############
        ############3
        