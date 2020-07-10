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
         #html = urllib.request.urlopen(str(url))
        html = urlopen(req).read()
        get_webpage_text(html)
        get_list(html)
        get_contact_page_link(html)
        return html   
    except:
        msg="none"
        return msg

#2        
#function to get text from html page        
def get_webpage_text(html):
        soup = BeautifulSoup(html, features="lxml")
        #to extract all text
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
        return list_to_str

#3
#function to get company name and url 
def get_list(page_html):
    soup = BeautifulSoup(page_html, features="lxml")
    #to extract text of company name and links using tag and class
    table_data = soup.findAll('a',{'class':'100link'})
    list_of_companies=[]
    for company in table_data:
        if company.text!="View From The Top Profile":
            list_of_company_with_url=[]
            list_of_company_with_url.append(company.text)
            list_of_company_with_url.append(company.get('href'))
            list_of_companies.append(list_of_company_with_url)
    return(list_of_companies) 

#main function        
def lead_main():     
    url="http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"   
    get_webpage(url)
lead_main()        