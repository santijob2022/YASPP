import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

pixela_endpoint = "https://pixe.la/v1/users/"
graph_id = "tamalesgraph1"
username_pixela = os.environ['username_pixela']
user_token_pixela = os.environ['user_token_pixela']

################### GET TIME IN REQUIRED FORMAT ###################
def time_getter(year=0,month=0,day=0):
    """
        Receives the date or get the now date in the format required by pixela: yyyyMMdd
        Note: Error handling needs to be added, possibly better to wait until the GUI version 
    """
    if year ==0 and month == 0 and day==0:
        return datetime.now().strftime("%Y%m%d")
    elif year !=0 and month != 0 and day!=0:
        return datetime(year=year,month=month,day=day).strftime("%Y%m%d")
    else:
        print("Error: There is a mistake in the date formatt") 

################### DELETE A PIXEL ###################
def delete_pixel():
    del_pixel_endpoint = f"{username_pixela}/graphs/{graph_id}/{time_getter()}"
    pixela_putpixel_endpoint = pixela_endpoint + del_pixel_endpoint    

    headers = {
        "X-USER-TOKEN":f"{user_token_pixela}"
    }

    res = requests.delete(url=pixela_putpixel_endpoint,headers=headers)
    print(res.text)

################### UPDATE A PIXEL ###################
def update_pixel():
    putpixel_endpoint = f"{username_pixela}/graphs/{graph_id}/{time_getter()}"
    pixela_putpixel_endpoint = pixela_endpoint + putpixel_endpoint
    
    new_pixel_params ={        
        "quantity":"25", 
        "optionalData":'{\"total\":\"50\"}'
        #'{"quantity":"7","optionalData":"{\"key\":\"value\"}"}'
    }

    headers = {
        "X-USER-TOKEN":f"{user_token_pixela}"
    }
    res = requests.put(url=pixela_putpixel_endpoint,json=new_pixel_params,headers=headers)
    print(res.text)

################### ADD A PIXEL ###################
def add_pixel():
    """
        Note 1: time_getter function has optional parameters, right now is automatically taking today's date.
                Remember to adequate it to the user requirement when building the GUI.
        Note 2: Add warning if the pixel already exists, remember the API automatically erases previous info.
    """
    pixela_addpixel_endpoint = pixela_endpoint+f"{username_pixela}/graphs/tamalesgraph1"
    
    addpixel_params ={
        "date":f"{time_getter()}", #yyyyMMdd
        "quantity":"25",
        "optionalData":'{\"total\":\"50\"}'
        #{"date":"20180915","quantity":"5","optionalData":"{\"key\":\"value\"}"}'
    }

    headers = {
        "X-USER-TOKEN":f"{user_token_pixela}"
    }
    res = requests.post(url=pixela_addpixel_endpoint,json=addpixel_params,headers=headers)
    print(res.text)
    # {"message":"Success.","isSuccess":true}

################### CREATE GRAPH ###################
def create_graph():
    pixela_graph_endpoint = pixela_endpoint+f"{username_pixela}/graphs"
    
    graph_params = {
        "id":f"{graph_id}",
        "name":"Tamales Sells",
        "unit":"Tamales",
        "type":"int",
        "color":"ajisai",
    }

    headers = {
        "X-USER-TOKEN":f"{user_token_pixela}"
    }

    res = requests.post(url=pixela_graph_endpoint,json=graph_params, headers=headers)
    print(res.text)    
    # {"message":"Success.","isSuccess":true}

################### CREATE USER ###################
def create_pixela_user():        

    user_params = {
        "token":user_token_pixela, 
        "username":f'{username_pixela}', "agreeTermsOfService":"yes", 
        "notMinor":"yes", "thanksCode":"ThisIsThanksCode"
        }
    # {"message":"Success. Let's visit https://pixe.la/@a-know , it is your profile page!","isSuccess":true}

    res = requests.post(url=pixela_endpoint, json=user_params)
    print(res.text)

################### Main ###################
#create_pixela_user()
#create_graph()
#add_pixel()
#update_pixel()
#delete_pixel()
