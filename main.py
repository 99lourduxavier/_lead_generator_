import re
import requests
from bs4 import BeautifulSoup
import logging
import spacy
import json
import csv


#url for webpage
url="http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"


#nlp for spacy
nlp =spacy.load('en_core_web_sm') 

#1
#function to get webpage
def get_webpage(url:str)->str:
    try:
        response=requests.get(url)
        html_page=response.text
        return html_page   
    except:
        return None

#2        
#function to get text from html page        
def get_webpage_text(html:str)->str:
    soup = BeautifulSoup(html,"lxml")
    html_page_text=soup.text
    return html_page_text


#3
#function to get company name and url as list
def get_list(page_html)->list:
    soup = BeautifulSoup(page_html,"lxml")
    #to extract text of company name and links using tag and class
    table_data = soup.findAll('a',{'class':'100link'})
    list_of_companies_with_url=[]
    for company in table_data:
        if company.text!="View From The Top Profile":
            list_of_company_with_url=[]
            list_of_company_with_url.append(company.text)
            list_of_company_with_url.append(company.get('href'))
            list_of_companies_with_url.append(list_of_company_with_url)    
    return(list_of_companies_with_url) 

#4
# function to get 'contact' or 'about' internal links from html as list
def get_contact_page(html:str)->list:
    try:
        contact_links=[]
        list_of_companies_with_url=get_list(html)
        links=[]
        internal_contact_list=[]
        list_of_links=[]
        company_contact_links=[]
        for contact_url in list_of_companies_with_url:
            list_of_links.append(contact_url[0])
            links.append(contact_url[1])
        for item in range(0,2):
            response=requests.get(links[item])
            data=response.text
            beauty=BeautifulSoup(data,"lxml")
            link=beauty.findAll('a')
            for contact_link in link:
                if "About" in contact_link.text:
                    url=contact_link.get('href')
                    contact_links.append(links[item]+url)
        for links in contact_links:
            if links not in internal_contact_list:
                internal_contact_list.append(links)
        for links in range(0,2):
            company_contact_links.append([list_of_links[link],internal_contact_list[link]])

    except:
        logging.basicConfig(filename='no_contact_company.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    return company_contact_links
    
   
    

#5
#function to get address from wepbage text as list
def get_location(text:str)->list:
    gets_list_company=[]
    doc=nlp(text)
    for ent in doc.ents:
        if 'GPE' in ent.label_:
            gets_list_company.append(ent.text)
    company_location=[]
    for location in gets_list_company:
        if location not in company_location:
            company_location.append(location)
    return company_location      

def save_to_json(filename : str ,json_dict : dict)-> None:
    with open(filename,"w") as file:
        file.write(json.dumps(json_dict, sort_keys=False, indent=2, separators=(',', ': ')))
      
       

def json_to_csv_file(json_filename  : str ,csv_filename : str)-> None:  
    with open(json_filename) as json_file: 
        address =json.load(json_file)
        company_locations=[]
        for item in address:
            company_locations.append({"company name":item,"location":address[item]})
        fields = ["company name","location"]  
        with open("company_location.csv", 'w') as location_csv_file: 
            writer = csv.DictWriter(location_csv_file, fieldnames = fields)  
            writer.writeheader()  
            writer.writerows(company_locations)       
            
             
#main function        
def lead_main(url):     
    #calling the function to get html page of url   
    html_page=get_webpage(url)
    #print(html_page)

    #calling the function to get text from html pages
    html_page_text=get_webpage_text(html_page)
    #print(html_page_text)

    #calling the function to get company name and url
    list_of_company_with_url=get_list(html_page)
    #print(list_of_company_with_url)
    
    #calling the function to get company 'contact' or 'about' urls
    company_contact_links=get_contact_page(html_page)
    #print(company_contact_links)
    
    #calling the function to get location of company from contact details
    company_location=get_location(html_page_text) 
    print(company_location)
    #calling the function for save location into json file
    filename="location.json"
    json_dict={}
    for item in list_of_company_with_url:
        company_name=item[0]
        company_url=item[1]
        data=get_webpage_text(company_url)
       
        print("\n")
        json_dict[company_name]=company_location
    print(json_dict)
    save_to_json(filename,json_dict)
    print("\nlocation has been successfully saved into json file..!\n")
    
    #calling function convert location from json to csv file
    json_to_csv_file(filename,"company_location.csv")
    print("json file data successfully converted into csv file..!\n")
lead_main(url)        