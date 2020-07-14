import urllib.request
import re
from bs4 import BeautifulSoup
import logging
import json
import csv




#url for webpage
url="http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"


#1
#function to get webpage
def get_webpage(url:str)->str:
    try:
        #html = urllib.request.urlopen(str(url))
        response = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        html = urllib.request.urlopen(response)
        html_bytes = html.read()
        html_page= html_bytes.decode("utf8")
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
def get_contact_page_link(html : str )-> list:
    contact_links=[]
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.find_all('a'):
        try:
            link=tag.attrs['href']
            name=tag.text
            keys=["Contact","Offices","about","contact","support"]
            for item in keys:
                if item in name:
                    contact_links.append(link)    
        except:
            link=tag.get('href')
            name=tag.text
            keys=["Contact","Offices","about","contact","support"]
            for item in keys:
                if item in name:
                    contact_links.append(link)
        
    contact_links=list(dict.fromkeys(contact_links))
    return contact_links
    

#5
#function to get address from wepbage text as list
def get_location(text:str)->list:
    location_list=[]
    #using module get_usa_location to get address list
    address_list=get_usa_address(text)
    #remove repeating address
    location_list=[item for item in address_list if item not in location_list]
    return location_list

#helper function for get_location
def get_usa_address(text):
    usa_address=[]
    usa_patterns=[r'[0-9|a-zA-Z]*\s[a-z|A-Z|0-9]*\s[A-Z|a-z|0-9]*\s[A-Z|a-z|0-9]*[,]\s[A-Z]{2}[\s][0-9]{5}',r'[0-9|A-Z|a-z ]*\n[A-Z|a-z ]*\n\t\t\t\t\t[A-Z|a-z]*[,]\s[A-Z]{2}\s[0-9]{5}',r'[0-9|A-Z|a-z]*\s[A-Z|a-z|0-9]*\s[A-Z|a-z|0-9]*[, ]\s[A-Z|a-z]*\s[0-9]*\n[A-Z|a-z\s]*[,]\s[A-Z]{2}\s[0-9]{5}',r'^\s[0-9]{3}\s[a-z|A-Z|0-9\s]*[,]\s[0-9|a-z|A-Z]*\s[a-z|A-Z]*\n[A-Z|a-z\s]*[, ]\s[A-Z]{2}\s[0-9]{5}',r'^[0-9a-zA-Z ]*[, ]\s[0-9A-Za-z\s]*[, ]\s[a-zA-z\s]*[0-9a-zA-z]{5}\n\bUnited States|USA\b$',r'^[0-9]{3}[a-z|A-Z\s]*\s[a-z|A-Z]{2}.[A-Z|a-z]*\s[0-9]*[A-z|a-z|0-9]*[,]\s[A-Z]{2}\s[0-9]{5}$']
    for pattern in usa_patterns:
        re_find = re.findall(pattern,text.strip(), flags = re.MULTILINE)
        for item in re_find:
            item= re.sub(r'[^\x00-\x7f]',' ', item)
            item= re.sub(r'\n|\t|\r',' ', item)
            if len(item)>4:
                usa_address.append(item)
    usa_address=list(dict.fromkeys(usa_address))
    return usa_address    



#save location into json file
def save_to_json(filename : str ,json_dict : dict)-> None:
    with open(filename, "w") as file_obj:
        #write all the data in json
        file_obj.write(json.dumps(json_dict, sort_keys=False, indent=2, separators=(',', ': ')))
        print("\nusa company address details save into \"company_adderss.json\" Successfully..! \nPlease Check it...!\n ")
    return None
      
      
       
#convert location from json to csv file
def json_to_csv_file(json_filename  : str ,csv_filename : str)-> None:  
    # Opening JSON file and loading the data 
    with open(json_filename) as json_file: 
        data =json.load(json_file)
        
         # writing to csv file  
        with open(csv_filename, 'w') as csvfile: 

            # field names  
            fields = ["Company","Addresses"]  
       
            # creating a csv writer object  
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(fields) 
            for item in data:
                add=" | ".join(data[item])
                keys=[item,add]
                # writing data rows  
                writer.writerow(keys)
            print("convert \"comapny_address.json\" into \"company_address.csv\" Successfully..! \nPlease Check it...! \n")
    return None
 
      
            
             
if __name__ == '__main__':
    #Create and configure logger
    log_file_name="no_contact_company.log"
    logging.basicConfig(filename=log_file_name,format='%(asctime)s %(message)s',filemode='w')
    #Creating an object 
    logger=logging.getLogger()
    #Setting the threshold of logger to DEBUG 
    logger.setLevel(logging.DEBUG) 
    logger.info("companies that has no contact details:")    


    #starts from here
    url = "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"
    #getting html content
    html= get_webpage(url)
    print("html content of The Top 100 Companies in the Digital Content Industry: The 2016-2017 EContent 100")
    # print(html)
    print("\n\n")

    #getting company list
    company_name_with_url=get_list(html)
    print("100 company names with its url:\n\n")
    #print list contain company and their url
    print(company_name_with_url)
    print("\n\n")
    print("length of company list : ",len(company_name_with_url))
    print("\n\n")
    
    list_of_all__contact_links=[]
    #check with first ten companies in the list of companies
    for company in company_name_with_url[:10]:
        list_of_contact_links=[]
        url=company[1]
        html=get_webpage(url)
        if html==None:
            print("could not get contact page for :"+company[0]+"\n")
            pass
        else:
            #getting contact list of each company 
            contact_page_list=get_contact_page_link(html)
            if len(contact_page_list):
                print("got contact page links for :"+company[0]+"\n")
                for item in contact_page_list:
                    if item.startswith('/'):
                        list_of_contact_links.append(company[1]+item)
                    else:
                        list_of_contact_links.append(item)
                list_of_all__contact_links.append([company[0],list_of_contact_links])
            else:
                print("no contact page found for "+company[0]+"\n")
                logger.setLevel(logging.DEBUG)
                logger.info("NO CONTACT DETAILS")
                logger.info(company[0])
            
    print("list of  company with its contact url: ")
    print("\n\n")
    #print company contact list
    print(list_of_all__contact_links)
    print("\n\n")
    print("No. of company has contact list : ",len(list_of_all__contact_links))
    print("\n\n")
    
    list_of_no_address=[]
    com_name_with_address_dict={}
    for item in list_of_all__contact_links:
        company_name=item[0]
        company_Contact_url=item[1][0]
        #getting contact url html 
        page_html=get_webpage(company_Contact_url)
        if page_html==None:
            list_of_no_address.append(company_name)
            pass
        else:
            #getting contact url text
            page_text=get_webpage_text(page_html)
            #getting location_list
            location_list=get_location(page_text)
            if len(location_list):
                com_name_with_address_dict.update({company_name:location_list})
                print("Company name:",company_name)
                print("Addresses:\n",location_list)
                print("\n")
            else:
                list_of_no_address.append(company_name)

    
    print("\nCompany with address:\n")
    print(com_name_with_address_dict)
    print("\ncompanies not have address:\n ")
    print(list_of_no_address)
    logger.info("NO ADDRESS DETAILS")
    #company has no adress store in log file
    for name in list_of_no_address:
        logger.setLevel(logging.DEBUG)
        logger.info(name)
      
    filename="usa_company_address.json"
    save_to_json(filename,com_name_with_address_dict)
    json_to_csv_file(filename,"usa_company_address.csv")
    print("Company may not have contact page and adress details stored in Log file.\nPlease Check in \"Company_details.log\" ")
