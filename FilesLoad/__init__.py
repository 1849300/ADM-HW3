import math
import multiprocessing
import os

import requests
from bs4 import BeautifulSoup


def loadPages(start,end):
    pathUrls="/content/drive/My Drive/ADM-HW3/HW3/links.txt"
    pool=multiprocessing.Pool()
    with open(pathUrls, "r") as f:
        text=f.read().split(sep="\n")
        # It enumerates from 1
        for index,url in enumerate(text,1):
            if index >= start and index < end:
                # It needs the index to localise its dir
                pool.apply(load,args=(index,url))
        pool.close()
        pool.join()
        f.close()



def load(i,url):
    ''' Given a url and the index of the url, it loads the page in the right directory '''
    
    # it finds the right dir
    page="/content/drive/My Drive/ADM-HW3/HW3/pages/page"+str(math.ceil(i/50))
    if not os.path.isdir(page):
        os.mkdir(page)
    try:
        cnt = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    soup = BeautifulSoup(cnt.content, features="lxml")
    # It deletes all the scripts from the page
    for element in soup.findAll('script'):
        element.extract()
    f = open(page+"/article_"+str(i)+".html", "w")
    f.write(soup.prettify())
    f.close()
