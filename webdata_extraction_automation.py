import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

no_pages =4
user_data = {'username': 'sravani','password': 'visualpath@_123'}
output_file_path = 'file2.csv'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
url_headers =['login','logout','enquiryusersnew','enquiryusersnew_page']
parse_fields = ['Ser No','User Name','Email Id','Location','Phone Number','user choosen Course','Message','Date','Enquiry Submitted From','View']

def html_parse(enquiry_response):
    global parse_fields
    parse_result,field_data_dict =[],{}
    
    doc = BeautifulSoup(enquiry_response,"html.parser")
    tags = doc.find_all("tr")

    for x1 in tags:
        tags1 = x1.find_all("td")
        x2 = 0
        for x in tags1:
            field_data_dict[parse_fields[x2]] = str(x.string)
            x2 += 1
        parse_result.append(field_data_dict.copy())    
    return parse_result

def urls(process):
    urls_dict = {'login' : 'https://www.visualpath.in/visualpathadmin/index.php',
                 'logout' : 'https://www.visualpath.in/visualpathadmin/logout.php',
                 'enquiryusersnew' : 'https://www.visualpath.in/visualpathadmin/enquiryusersnew.php',
                 'enquiryusersnew_page':'https://www.visualpath.in/visualpathadmin/enquiryusersnew.php?page_no='}
    
    return urls_dict.get(process)

def get_page_nos(enquiry_response,no_pages):
    pages=[]
    doc = BeautifulSoup(enquiry_response,"html.parser")

    p1 = doc.strong.string
    p2 = p1.split()

    for x1 in range(no_pages):
        pages.append(int(p2[-1]) - x1)
    return pages

def save_csv(enquiry_data,file_path):
    df1 = pd.DataFrame(enquiry_data)
    df1.dropna()
    df1.drop(['Message', 'Enquiry Submitted From','View'], axis = 1,inplace = True)
    df1.to_csv(file_path,index=False)
    print('Task Completed')
    
def error_response(res_no):
    response_dict = {'1':'Login Failed',
                     '2':'Enquiry request failed',
                     '3':'Logout Failed'}
    
    print(response_dict.get(str(res_no)))
    
def main():
    global url_headers,user_data,headers,no_pages,file_path
    pages,enquiry_result = [],[]
    try:
        with requests.Session() as s:
            login_request = s.post(urls(url_headers[0]), data=user_data,headers = headers) #Login request
            if(login_request.status_code == 200):
                enquiry_request = s.get(urls(url_headers[2]),headers = headers) #Enquiry request

                if(enquiry_request.status_code == 200):
                    pages = get_page_nos(enquiry_request.text,no_pages) 
                    #Get page by info
                    for page in reversed(pages):
                        enquiry_page_request = s.get(urls(url_headers[3]) + str(page),headers = headers) #Enquiry page request
                        if(enquiry_page_request.status_code == 200): enquiry_result += html_parse(enquiry_page_request.text)

                    if(len(enquiry_result) !=0): save_csv(enquiry_result,output_file_path)

                    logout_request = s.get(urls(url_headers[1]),headers = headers) #Logout request
                    if(logout_request.status_code != 200): error_response(3)
                    
                else: error_response(2)                  
            else: error_response(1)          
    finally:
        print('')

if __name__ == "__main__":
    main()
