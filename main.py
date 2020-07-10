import re
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

#1
#function to get webpage
def get_webpage(url):
    try:
        # parsing html and getting clear text from it
        req = Request(str(url), headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        get_webpage_text(html)
        return html   
    except:
        msg="none"
        return msg

#2        
#function to get text from html page        
def get_webpage_text(html):
        #html = urllib.request.urlopen(str(url))
        soup = BeautifulSoup(html, features="lxml")
        data = soup.findAll(text=True)
        #to filter visible element from html using re-match
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True
        result = filter(visible, data)
        list_to_str = ' '.join([str(element) for element in list(result)])
        print(list_to_str)
        return list_to_str

#main function        
def lead_main():     
    url="http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"   
    get_webpage(url)
lead_main()        