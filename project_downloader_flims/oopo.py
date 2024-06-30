
import requests 
from bs4 import BeautifulSoup
def get_iframe(self,link_move):
        response=requests.get(link_move)
        soup=BeautifulSoup(response.text,'html.parser')
        iframe = soup.find("iframe", {"id": "IframeEmbed"})
        if iframe:
            iframe_src = iframe.get("data-lazy-src")
            print(iframe_src)
        else:
            print("لم يتم العثور على عنصر <iframe> بالاسم المحدد")
get_iframe("https://wecima.show/watch/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d9%81%d9%8a%d9%84%d9%85-%d8%b1%d8%ad%d9%84%d8%a9-404-2024/")