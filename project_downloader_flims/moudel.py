
def delate_part_of_linK(link):
    x = list(link)
    elemnt = "&"
    if elemnt in x:
        num = x.index(elemnt)
        num2 = num + 1
        if x[num2] != "E":
            for i in range(4):
                del x[num2]
    dir_link = ''.join(x)
    return dir_link




def good_search():
    import requests
    from bs4 import BeautifulSoup
    import urllib.parse


    payload = "تاج"
    params = {
        "q": payload
    }
    
    url = 'https://www.google.co.in/?'
    query_string = urllib.parse.urlencode(params)
    full_url = url + query_string
    
    response = requests.get(full_url)
    print(response.status_code)
    
    source = BeautifulSoup(response.text, "lxml")
    source2 = source.find_all("span", class_="iAIpCb PZPZlf")
    print(source)
    pass # Reform and development underway for this function






