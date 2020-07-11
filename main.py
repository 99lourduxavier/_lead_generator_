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

#re for zip
zip_re = re.compile('^[0-9]{5}(?:-[0-9]{4})?$')

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
    response=requests.get(url)
    html=response.text
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
def get_contact_page_link(html : str )-> list:
    list_of_contact_page_links=[]
    links=[]
    list_of_company_with_url=get_list(html)
    for items in list_of_company_with_url[:2]:
        try:
            company_name=items[0]
            company_url=items[1]
            page_html=get_webpage(company_url)
            soup = BeautifulSoup(page_html, "lxml")
            contacts_link=soup.findAll('a')
            patterns=["about"]
            for item in contacts_link:
                for items in patterns:
                    if re.search(items,item.get('href')):
                        if item.get('href').startswith('http'):
                            list_of_contact_page_links.append([company_name,item.get('href')])
                        else:
                            list_of_contact_page_links.append([company_name,company_url+item.get('href')])
        except:
            logging.basicConfig(filename='no_contact_company.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
            logginh.info(company_name)
    [links.append(item) for item in list_of_contact_page_links if item not in links ]
    print(links)
    return links
    

#5
#function to get address from wepbage text as list
def get_location(text:str)->list:
    gets_list_company=[]
    usa_zip=[]
    doc=nlp(text)
    for ent in doc.ents:
        if 'GPE' in ent.label_:
            gets_list_company.append(ent.text)
    #remove repeated name 
    company_location= [] 
    [company_location.append(location) for location in gets_list_company if location not in company_location ]
    
    for usa_code in company_location:
        zip_code_match = zip_re.match(usa_code.strip())
        if zip_code_match:
            usa_code.append(usa_code)
            break
        if zip_code_match is None:
            print("Error - no match")
    print(usa_code)
    return usa_code

#save location into json file
def save_to_json(filename : str ,json_dict : dict)-> None:
    with open(filename, "w") as file_obj:
        file_obj.write(json.dumps(json_dict))
      
      
       
#convert location from json to csv file
def json_to_csv_file(json_filename  : str ,csv_filename : str)-> None:  
       # Opening JSON file and loading the data 
# into the variable data 
    with open(json_filename) as json_file: 
        address =json.load(json_file)
        locations=[]
        for item in address:
            locations.append({"company name":item,"location":address[item]})

        # field names  
        fields = ["company name","location"]  
        # writing to csv file  
        with open(csv_filename, 'w') as csvfile: 
             
            writer = csv.DictWriter(csvfile, fieldnames = fields)  
            writer.writeheader()  
            writer.writerows(locations) 
      
            
             
if __name__ == '__main__':
    html_page= get_webpage(url)
    company_list=get_list(html_page)
    print(company_list)
    print("company name and url extracted..!")


   
    # to get list conataining company name and contact url
    list_of_companies_with_url=get_contact_page_link(html_page)

    print(" companyname and contact url list getting sucessfully..!")
    print(list_of_companies_with_url)
    print("\n")
    locations=[]
    filename="location.json"
    company_dict={}
    for company in list_of_companies_with_url:
        name=company[0]
        url=company[1]
        print("URL ",url)
        text=get_webpage_text(url)
        #  print(text)
        location_list=get_location(text)
        locations+=location_list
    company_dict[name]=locations
    print("\n")
    print(company_dict)
    #print(json_dict)
    save_to_json(filename,company_dict)
    print("\nsave to json file successfully..!\n")
    #calling function convert location from json to csv file
    json_to_csv_file(filename,"location.csv")
    print("Json to csv convert sucessfullly..!\n")   
