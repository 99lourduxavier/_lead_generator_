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
            if tag.has_attr('href'):
                link=tag.attrs['href']
                keys=["about","contact","locations","office"]
                for item in keys:
                    if item in link:
                        contact_links.append(link)
            
        except:
            link=tag.get('href')
            if len(link)!=0:
                keys=["about","contact","locations","office"]
                for item in keys:
                    if item in link:
                        contact_links.append(link)
    contact_links=list(dict.fromkeys(contact_links))
    return contact_links

#list to conains company contact page links
company_contact_links_list=[['Acquia, Inc', 'https://www.acquia.com/about-us/contact'],
['Acquire Media', 'http://acquiremedia.com/contactus/'],
['Acrolinx GmbH', 'https://www.acrolinx.com/contact/'],
['Act-On Software', 'https://act-on.com/contact-us/'],
['Apple, Inc.', 'https://www.apple.com/contact/'],
['Aptara, Inc.', 'https://www.aptaracorp.com/about-aptara/contact-us'],
['Aquafadas', 'https://www.aquafadas.com/contact-us/'],
['Aria Systems, Inc.', 'https://www.ariasystems.com/contact-us/'], 
['Atex', 'https://www.atex.com/atex/contact-us/'],
['Atypon Systems, Inc.', 'https://www.atypon.com/about-us/locations/'],
['Automattic, Inc.', 'https://automattic.com/contact/'],
['Brightcove, Inc.', 'http://brightcove.com/en/contact-us'],
['COGNITIVESCALE', 'http://cognitivescale.com/contact/'],
['Cision US, Inc.', 'https://www.cision.com/us/about/media-kit/'],
['Clarabridge', 'https://www.clarabridge.com/contact/'],
['Cloudera, Inc.', 'http://cloudera.com/about/locations.html'],
['Cloudwords, Inc.', 'https://www.cloudwords.com/contactus'],
['Connotate', 'https://www.import.io/contact-sales/?utm_source=tate&utm_medium=website&utm_term=choose-contact-sales'],
['CoreMedia AG', 'https://www.coremedia.com/en/about/contact'],
['Crafter Software Corp.', 'http://craftersoftware.com/about/contact'],
['Crownpeak Technology', 'http://crownpeak.com/about/contact-us'],
['DNN Corp.', 'https://www.dnnsoftware.com/about/contact-dnn'],
['EBSCO Industries, Inc.', 'http://ebsco.com/about/offices'],
['Ephox', 'https://www.tiny.cloud/contact'],
['Episerver', 'http://episerver.com/contact-us'],
['Evergage, Inc.', 'https://www.evergage.com/contact-us/'],
['Facebook', 'http://facebook.com/about/privacy/update'],
['Hippo B.V.', 'https://www.bloomreach.com/en/about/terms-of-use'],
['Kentico Software', 'http://kentico.com/contact'],
['MadCap Software, Inc.', 'https://www.madcapsoftware.com/contact-us/'],
['NewsCred', 'http://newscred.com/contact'],
['OneSpot', 'https://www.onespot.com/contact/'],
['OpenText Corp.', 'https://www.opentext.com/about/office-locations'],
['ProQuest, LLC', 'http://proquest.com/about/locations'],
['Quark Software, Inc.', 'https://www.quark.com/about/offices/'],
['Realview', 'http://realviewdigital.com/contact-us/'],
['SAP', 'https://www.sap.com/about/legal/impressum.html'],
['SAS Institute, Inc.', 'https://www.sap.com/about/legal/copyright.html'],
['SYSOMOS', 'http://sysomos.com/contact/'],
['Sitecore Corp. AS', 'http://sitecore.net/company/contact-us'],
['Siteworx, LLC', 'https://www.shift7digital.com/about-us/'],
['Sizmek, Inc.', 'https://www.sizmek.com/about/'],
['Skyword, Inc.', 'https://www.skyword.com/contact-us/'],
['Smartling, Inc.', 'http://smartling.com/contact-us'], 
['Splunk, Inc.', 'http://splunk.com/en_us/about-splunk/contact-us.html'],
['Spotify AB', 'https://www.spotify.com/in/about-us/contact/'],
['Syncfusion, Inc.','http://syncfusion.com/company/contact-us'],
['Translations.com (A TransPerfect Co.)', 'http://translations.com/about/global-group'],
['Uberflip', 'https://www.uberflip.com/contact/'],
['Viglink', 'https://www.sovrn.com/contact/'],
['Webtrends', 'https://www.webtrends.com/about-us/contact-us/'],
['Wochit', 'https://www.wochit.com/contact/'],
['ZUMOBI', 'http://zumobi.com/contact/'],
['Zoomin', 'https://www.zoominsoftware.com/contact-us/'],
['welocalize', 'http://welocalize.com/contact/']]   

#regex patterns
usa_patterns=[r'[0-9|a-zA-Z]*\s[a-z|A-Z|0-9]*\s[A-Z|a-z|0-9]*\s[A-Z|a-z|0-9]*[,]\s[A-Z]{2}[\s][0-9]{5}',
r'[0-9|A-Z|a-z ]*\n[A-Z|a-z ]*\n\t\t\t\t\t[A-Z|a-z]*[,]\s[A-Z]{2}\s[0-9]{5}',
r'[0-9|A-Z|a-z]*\s[A-Z|a-z|0-9]*\s[A-Z|a-z|0-9]*[, ]\s[A-Z|a-z]*\s[0-9]*\n[A-Z|a-z\s]*[,]\s[A-Z]{2}\s[0-9]{5}',
r'^\s[0-9]{3}\s[a-z|A-Z|0-9\s]*[,]\s[0-9|a-z|A-Z]*\s[a-z|A-Z]*\n[A-Z|a-z\s]*[, ]\s[A-Z]{2}\s[0-9]{5}',
r'^[0-9a-zA-Z ]*[, ]\s[0-9A-Za-z\s]*[, ]\s[a-zA-z\s]*[0-9a-zA-z]{5}\n\bUnited States|USA\b$',
r'^[0-9]{3}[a-z|A-Z\s]*\s[a-z|A-Z]{2}.[A-Z|a-z]*\s[0-9]*[A-z|a-z|0-9]*[,]\s[A-Z]{2}\s[0-9]{5}$',
r'^[a-z|A-Z|0-9]*[,]\s[A-z]{2}\s[0-9]{5}\r\n\bUnited States\b',
r'[0-9]*\s[A-z].\s[a-z|0-9]*\s[A-Z|a-z]*.\n[A-Za-z]*\s[A-z|a-z]*[, ]\s[A-Z]{2}\s[0-9]{5}\n\bUSA\b']

other_patterns=[r'^[A-Z|a-z]\s[A-Z|a-z ]\n[0-9]\s[A-Z|a-z]\s[A-Z|a-z]\n[A-z|a-z]\s[A-Z|a-z]\s[A-Z]\s[0-9]{5}\s[A-z]*$',
r'[/|0-9|A-z]*[0-9|A-z|,]*\s[A-z|.|a-z|0-9]*[0-9|a-z|.]*[A-z|,|0-9]*\s[A-z|.|-]*[0-9|\s]*[A-z|,]*\s[A-z]*\s[0-9]{5}',
r'^[0-9|A-Z|a-z|,| ]*[-|0-9|.]*\n[A-Z|a-z]*[,]\s[A-Z|0-9]*\s[0-9A-Z]{3}[0-9|]*',
r'[0-9]*\s[0-9]*[a-z]*\s[A-z]*\s[#0-9]*\n[A-z]*\s[A-z]*[,]\s[A-z]{2}\s[0-9]{5}',
r'^[A-z|a-z|0-9]*\s[A-z|0-9|\s]*[A-z|\s|,|.]\s[0-9|A-Z|a-z]*\n[0-9|a-z]*\s[A-Z|a-z|0-9]*[,]\s[A-Z|a-z]*',
r'[0-9]*\s[a-z]*\s[A-Z|a-z]*\s[A-Z|a-z]*[,]\s[A-z]*\s[A-z]*\s[\w]*\s[\w]*\s[0-9][,]\s[0-9]{5}\s[A-z]*',
r'^[0-9]{3}\s[A-z|a-z|]\s[A-Z|a-z|,]\s[A-Z|a-z]\s[0-9|A-Z|a-z,]\s[A-Z]*\s[0-9]{5}',
r'^[A-Z|a-z|][0-9]\s[A-Z|a-z]{5}\s[A-Z|a-z]\s[A-Z|a-z]\s[A-Z|a-z,]\s[A-Z]\s[A-Z|0-9]\s[0-9|A-Z]\s[A-Z|a-z]*$',
r'[A-Z|a-z]\s[A-Z|a-z|0-9]\s[A-Z|a-z]\s[A-Z|a-z]\s#[0-9|A-z|a-z]\s[A-z|a-z,]\s[A-Z]{2}\s[0-9]{5}',
r'^[A-Z|a-z|]\s[A-Z|a-z],\s[A-Z]{3}\n[A-Z|a-z]\s[A-Z|a-z|0-9]\s[A-Z|a-z]\s[A-z|a-z,]\s[0-9][a-z]\s[A-Z|a-z,]\s[A-Z|a-z,]\s[A-Z|a-z]\s[A-Z|a-z,]\s[A-Z]\s|-|[0-9]{5}$',
r'[A-Z|a-z]\s[A-Z|a-z|0-9]\s[A-Z|a-z]\s[A-Z|a-z]\s#[0-9|A-z|a-z]\s[A-z|a-z,]\s[A-Z]{2}\s[0-9]{5}',
r'[A-z]*\s[0-9]{2}[,]\s[A-z]*\s[A-z]{3}[,]\s[A-z]*\s[A-z]{6}[0-9]{3}\s[A-z]*\s[A-z]*[A-z]*[,]\s[A-Z]{3}\s[0-9]{4}']

    
#5
#function to get address from wepbage text as list
def get_location(text : str)-> list:
    #check with usa patterns
    list_of_addresses=[]
    for pattern in usa_patterns:
        find = re.findall(pattern,text.strip(), flags = re.MULTILINE)
        for item in find:
            item= re.sub(r'[^\x00-\x7f]',' ', item)
            item= re.sub(r'\n|\t|\r',' ', item)

            if len(item)>4 and item.isdigit()==False:
                item=" ".join(item.split())
                list_of_addresses.append(item)
    list_of_addresses=list(dict.fromkeys(list_of_addresses))
    if len(list_of_addresses)==0:
    #check with other patterns
        list_of_addresses=[]
        for pattern in other_patterns:
            find = re.findall(pattern,text.strip(), flags = re.MULTILINE)
            for item in find:
                item= re.sub(r'[^\x00-\x7f]',' ', item)
                item= re.sub(r'\n|\t|\r',' ', item)

                if len(item)>4 and item.isdigit()==False:
                    item=" ".join(item.split())
                    list_of_addresses.append(item)
        list_of_addresses=list(dict.fromkeys(list_of_addresses))    
    return list_of_addresses


#save location into json file
def save_to_json(filename : str ,json_dict : dict)-> None:
    with open(filename, "w") as file_obj:
        #write all the data in json
        file_obj.write(json.dumps(json_dict, sort_keys=False, indent=2, separators=(',', ': ')))
        print("\ncompany address details save into \"company_adderss.json\" Successfully..! \nPlease Check it...!\n ")
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
    error_log_file="no_contact_company.log"
    logging.basicConfig(filename=error_log_file,format='%(asctime)s %(message)s',filemode='w')
    #Creating an object 
    logger=logging.getLogger()
    #Setting the threshold of logger to DEBUG 
    logger.setLevel(logging.DEBUG) 
    logger.info("COMPANIES DOESN'T HAVE CONTACT LINKS :")    


    #starts from here
    url = "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"
    #getting html content
    html= get_webpage(url)
    print("\nhtml content of The Top 100 Companies in the Digital Content Industry: The 2016-2017 EContent 100\n\n")
    # print(html)

    #getting company list
    company_name_with_url=get_list(html)
    print("company names with its url:\n\n")
    #print list contain company and their url
    print(company_name_with_url)
    print("\n\n")
    print("length of company list : ",len(company_name_with_url))
    print("\n\n")
    
    #for contact links
    no_contact_links=[]
    no_html_get=[]
    list_of_all__contact_links=[]
    #check with first ten companies in the list of companies
    for company in company_name_with_url:
        list_of_contact_links=[]
        company_name=company[0]
        company_url=company[1]
        html=get_webpage(company_url)
        if html!=None:
            #getting contact list of each company 
            contact_page=get_contact_page_link(html)
            if len(contact_page):
                print("got contact page links for : "+company[0]+"\n")
                for item in contact_page:
                    if item!= None and item.startswith('/'):
                        list_of_contact_links.append(company[1]+item)
                    else:
                        list_of_contact_links.append(item)
                list_of_all__contact_links.append(list_of_contact_links)
            else:
                logger.setLevel(logging.DEBUG)
                logger.info("NO CONTACT LINKS FOUND")
                logger.info(company_name)
                logger.info(company_url) 
                no_contact_links.append(company_name)  
                
        else:
            no_html_get.append(company_name)      

    print("\n\nCOMPANIES WITH ITS CONTACT URLS :\n")
    print("No.of companies : ",len(list_of_all__contact_links))
    print("\ncompanies list(name with urls...) : \n\n")
    #print company contact list
    print(list_of_all__contact_links)
    print("\n\nCOULDN'T GET HTML CONTENT :\n")
    print("No.of companies : ",len(no_html_get))
    print("\ncompanies list(couldn't get html content...)\n\n")
    #print no html content company names
    print(no_html_get)
    print("\n\nCOMPANIES DOESN'T HAVE CONTACT LINKS :\n")
    print("No.of companies : ",len(no_contact_links))
    print("\ncompanies list(no contact links...) :\n ")
    #print no contact links 
    print(no_contact_links)
    print("\n\n")
 
    #for addresses from contact links
    no_html_get=[]
    com_name_with_address_dict={}
    for item in company_contact_links_list:
        company_name=item[0]
        company_Contact_url=item[1]
        #getting contact url html 
        page_html=get_webpage(company_Contact_url)
        if page_html!=None:
            #getting contact url text
            page_text=get_webpage_text(page_html)
            #getting location_list
            location_list=get_location(page_text)
            com_name_with_address_dict.update({company_name:location_list})
            print("\ncompany name and addresses:\n\n")
            print("Company name:",company_name)
            print("Addresses:\n",location_list)
            print("\n")
        else:
            no_html_get.append(company_name)    

    print("\n\nADDRESS FOUNDED COMPANIES : \n")
    print("No.of companies : ",len(com_name_with_address_dict))
    print("\ncompanies list : \n\n")
    print(com_name_with_address_dict)
    print("\n\nCOULDN'T GET HTML CONTENT :\n")
    print("No.of companies : ",len(no_html_get))
    print("\ncompanies list(couldn't get html content...)\n\n")
    #print no html content company names
    print(no_html_get)
    
    #json file name
    filename="company_address.json"
    save_to_json(filename,com_name_with_address_dict)
    json_to_csv_file(filename,"company_address.csv")
    print("Company may not have contact page and adress details stored in Log file.\nPlease Check in \"no_contact_company.log\" ")