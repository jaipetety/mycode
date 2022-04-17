import requests

user_data = {'user_name': 'Visualpath123','login': 'login','user_psw': 'Visualpath123'}
details_file_path = 'Details.txt'
numbers_file_path = 'sms_numbers.txt'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
url_headers =['login','logout','reportcontrol','delrep_page','dashborad','send']

def urls(process):
    urls_dict = {'login' : 'http://smsjipra.in/login.php',
                 'logout' : 'http://smsjipra.in/logout.php',
                 'reportcontrol' : 'http://smsjipra.in/include/reportController.php',
                 'delrep_page':'http://smsjipra.in/Dashboard.php?page=delivery-report',
                 'dashborad' : 'http://smsjipra.in/Dashboard.php',
                 'send':'http://smsjipra.in/sending.php'}
    
    return urls_dict.get(process)

def send_confirmation():
    send_input = raw_input('Do you want to send message ? Y/N : ')
    if(send_input in ['Y','y']):
        print('\nMessage being sent')
        return 1
    else:
        print('\nMessage not sent')
        return 0     

def message_build(file_path):
    
    response,demo_link,detail,sno = [],'','',2

    course = ['TIBCO BW 6X AND CE','Ax(D365) Functional(Finance and T&L)','AZURE ADMIN','Fullstack Development and React Js','AWS','']
    trainer = ['Abhishek','Satya','Ravi Kumar','Keshav','Pavan','']

    demo_text = ' Online Demo by Visualpath '
    link_text = 'Link to join: '
    ph_text = ' Ph:9704455959'

    with open(file_path,"r") as file:
        details_data = file.read()
        details_list = details_data.split('\n')
        demo_link,detail,sno = details_list[0],details_list[1],int(x1[2])

        print(details_list)

    message = course[sno] + demo_text + detail + ' By ' + trainer[sno] + '. ' + link_text + demo_link + ph_text
              
    msg_count = str(len(message)) +'  Character, 1 SMS'

    print('\n'+ message + '\n')

    response.append(message)
    response.append(msg_count)
    
    return response

   
def error_response(res_no):
    response_dict = {'1':'Login Failed',
                     '2':'SMS Sending failed',
                     '3':'Logout Failed'}
    
    print(response_dict.get(str(res_no)))
    
def main():
    global user_data,headers,numbers_file_path,details_file_path
    try:
        with open(numbers_file_path,"r") as file:
            numbers = file.read()

        response = message_build(details_file_path)

        api_post_params = {'type':'sendSMSsave','checkroutetype': '1','send_type': 'Quick Send','is_schedule':'','senderid_name':'VIPATH','scheduleDateTime':'',
               'az_routeid':'4<$$>Transtrnew','sid': '11513<$>VIPATH<$>','numbers': numbers,'templates': '6579','message': response[0],
               'txtMessageCount': response[1] ,'original_url': ''}
        send_flag = send_confirmation()

        if(send_flag == 1):
            with requests.Session() as s:
                login_request = s.post(urls(url_headers[0]), data= user_data,headers = headers) #Login request
                if(login_request.status_code == 200):
                    send_request = s.post(urls(url_headers[5]),data = api_post_params,headers = headers) #Send request
                    if(send_request.status_code == 200):
                        print('Sms Sent Successfully')                   
                        logout_request = s.get(urls(url_headers[1]),headers = headers) #Logout request
                        if(logout_request.status_code != 200): error_response(3)                    
                    else: error_response(2)                  
                else: error_response(1)          
    finally:
        print('')

if __name__ == "__main__":
    main()
