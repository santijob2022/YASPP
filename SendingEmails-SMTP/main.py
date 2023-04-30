import datetime as dt
import pandas as pd
import smtplib
import random
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(content):
    my_email = os.environ["email"]
    password = os.environ["email_password"]
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as connection:
    # yahoo -> smtp.mail.yahoo.com # hotmail -> smtp.live.com        
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs=my_email,
            msg=f"Subject:Happy Birthday!!!\n\n{content}"
            )

def check_birthday(today_date):
    global total_letters
    df = pd.read_csv("birthdays.csv")    
    for _,row in df.iterrows():
        if row[3] == today_date[1] and row[4] == today_date[0]:
            letter_number=random.randint(1,total_letters)
            with open(f"letter_templates\letter_{letter_number}.txt","r") as file:
                content = file.read()
                if "NAME" in content:                    
                    content = content.replace("[NAME]",row[0])
                #print(content)
                send_email(content)

def get_today_date():
    day = dt.datetime.now().day
    month = dt.datetime.now().month
    return day,month       
############################### Main #######################################

total_letters = 3
check_birthday(get_today_date())







