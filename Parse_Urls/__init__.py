import multiprocessing
import requests
from bs4 import BeautifulSoup
import re



def write_url():
    # It creates a links.txt file where there are all the links
    f = open("links.txt", "w")
    pool=multiprocessing.Pool()
    ListUrls=pool.map(func,range(0,20000,50))
    text = "".join(ListUrls)
    f.write(text)
    f.close()


def func(x):
    # It finds all the links in each page
    text = ""
    url = "https://myanimelist.net/topanime.php?limit={}"
    try:
        cnt = requests.get(url.format(x))
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    soup = BeautifulSoup(cnt.content, features="lxml")
    result = soup.findAll(attrs={'id': re.compile('#area'), "class": 'hoverinfo_trigger fl-l ml12 mr8'})
    for res in result:
        full_link = res.get("href")
        text = text+full_link+"\n"
    return text


def check_len(text):
    # It checks the len of the text
    set2=set()
    Text_list=text.split("\n")
    for string in Text_list:
        set2.add(string)
    return len(set2)






