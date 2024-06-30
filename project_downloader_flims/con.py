import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class GetLinks:
    def __init__(self) -> None:
        self.name_film = None
    
    def read_file(self):
        with open('arbic.json', 'r', encoding='utf-8') as file:
            movie_links = json.load(file)
        return movie_links
    
    def set_movie_name(self):
        self.name_film = input("من فضلك أدخل اسم الفيلم: ")
        return self.name_film

    def search_movie_link(self, movie_dict):
        matches = process.extract(self.name_film, movie_dict.keys(), limit=3, scorer=fuzz.token_set_ratio)
        best_match = None
        for match in matches:
            name, score = match
            if score > 70:
                best_match = name
                break
        if best_match:
            return movie_dict[best_match]
        else:
            return "الفيلم غير موجود في القاموس أو لا يوجد تطابق قريب."

    def get_iframe(self, link_move):
        response = requests.get(link_move)
        soup = BeautifulSoup(response.text, 'html.parser')
        iframe = soup.find("iframe", {"id": "IframeEmbed"})
        if iframe:
            iframe_src = iframe.get("data-lazy-src")
            return iframe_src
        else:
            print("لم يتم العثور على عنصر <iframe> بالاسم المحدد")
            return None

    def get_link_from_network(self, url_work):


        # إعداد متصفح كروم مع Selenium
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # تشغيل المتصفح في الوضع غير المرئي
        options.add_argument("--disable-gpu")  # تعطيل GPU
        options.add_argument("--no-sandbox")  # تعطيل sandbox
        options.add_argument("--disable-dev-shm-usage")  # تعطيل dev/shm usage

        # تمكين logging performance للحصول على أحداث الشبكة
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        # إعداد خدمة المتصفح
        service = Service(ChromeDriverManager().install())

        # تشغيل المتصفح
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)  # زيادة مهلة تحميل الصفحة

        # قائمة لتخزين الطلبات
        requests = []

        # فتح الصفحة المستهدفة
        url = url_work
        driver.get(url)

        # انتظار تحميل الصفحة
        time.sleep(10)

        # تنفيذ إجراء بالنقر على الزر
        try:
            driver.find_element(By.CSS_SELECTOR, "getResultsBtn").click()
        except:
            pass

        # انتظار بعض الوقت لالتقاط الطلبات
        time.sleep(15)

        # جلب جميع السجلات
        logs = driver.get_log('performance')

        # فلترة الطلبات
        for log in logs:
            log_json = json.loads(log['message'])['message']
            if log_json['method'] == 'Network.requestWillBeSent':
                request = log_json['params']['request']
                requests.append({
                'url': request['url'],
                'method': request['method'],
                'type': request.get('type', 'N/A')
            })
                
        mb4=''
        # طباعة تفاصيل الطلبات
        for request in requests:
            print(f"URL: {request['url']}")
            print(f"Method: {request['method']}")
            print(f"Type: {request['type']}")
            print()
            if request['url'][-3:]=='mp4':
                mb4=request['url']

        # إغلاق المتصفح
        driver.quit()

        return mb4

    def download_movie(self, movie_name, link):
        headers = {
            "Accept": "video/webm,video/ogg,video/;q=0.9,application/ogg;q=0.7,audio/;q=0.6,/;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd, identity",
            "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "gthcdnx24m-20.erea12.shop:82",
            "Priority": "u=4",
            "Range": "bytes=0-",
            "Referer": "https://wecima.show/",
            "Sec-Fetch-Dest": "video",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
        }

        response = requests.get(link, headers=headers, stream=True)

        with open(f"{movie_name}.mp4", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                print("loading")

        print(f"Finished downloading. Status code: {response.status_code}")


# إنشاء كائن من الكلاس GetLinks
obj = GetLinks()

# قراءة البيانات من الملف
read_file = obj.read_file()

# تعيين اسم الفيلم من المستخدم
enter_name = obj.set_movie_name()

# البحث عن الفيلم وعرض الرابط
search = obj.search_movie_link(read_file)

# الحصول على رابط iframe
get_fr = obj.get_iframe(search)

if get_fr:
    # الحصول على الروابط من الشبكة
    get_net = obj.get_link_from_network(get_fr)

    if get_net:
        # تحميل الفيلم
        obj.download_movie(enter_name, get_net[-1]['url'])
