"""
    The programe executes each 5 minutes to detect if the ISS is near you and if there
    is still sunlight to see it, if so, it sends a message to your email.
    This works only if the sunrise is between 12:00 AM to 12:00 PM
    and the sunset is between 12:00 PM to 12:00 AM

    The sunrise-sunset API is “Powered by SunriseSunset.io“.
"""

import requests
import smtplib
from datetime import datetime
import time

# Approximate Location. Center of Mexico.
MY_LAT = 20.60985 
MY_LNG = -100.3626


################## SEND EMAIL ALERT ##################
def send_email():

    """ Send notification to see the ISS. """

    my_email = "add_email"
    password = "add_email_password"
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as connection:
    # yahoo -> smtp.mail.yahoo.com # hotmail -> smtp.live.com        
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs=my_email,
            msg=f"Subject:Look up!!!\n\nYou may have a chance to see the ISS!!"
            )

################## CHECKS IF THERE IS SUNLIGHT ##################
def is_there_sunlight():
    """ 
    The function assumes the sunrise is between 12:00 AM to 12:00 PM
    and the sunset is between 12:00 PM to 12:00 AM    
    """
    sunlight_time = sunrise_sunset_API_CALL()
    hour_12f = get_hour_AM_PM()

    if hour_12f[1] == "AM":
        if int(hour_12f[0]) >= int(sunlight_time["sunrise"][0].split(":")[0]):
            return 1
    elif hour_12f[1] == "PM":
        if int(hour_12f[0]) <= int(sunlight_time["sunset"][0].split(":")[0]):
            return 1
    else:
        return 0   


################## GET CURRENT TIME 24 HOURS FORMAT ##################
def get_hour_AM_PM():

    """ Returns current hour and if it is AM PM"""

    now = datetime.now()
    # 24-hour format
    # print(now.strftime('%Y/%m/%d %H:%M:%S'))
    # 12-hour format
    # print(now.strftime('%Y/%m/%d %I:%M:%S'))
    return now.strftime('%I-%p').split("-")


################## IS THE ISS NEAR MY LOCATION? ##################
def is_ISS_near():

    """ Checks if the ISS is near my current location """

    position = iss_API_CALL()
    if abs(position["iss_lat"]-MY_LAT) <= 5 and abs(position["iss_lng"]-MY_LNG) <=5:
        return 1
    else:
        return 0

################## ISS API ##################
def iss_API_CALL():

    """ Gets the current ISS position """

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    iss_lng = float(response.json()["iss_position"]["longitude"])
    iss_lat = float(response.json()["iss_position"]["latitude"])
    position = {
        "iss_lng" : iss_lng,
        "iss_lat" : iss_lat,
    }
    return position

################## SUNRISE-SUNSET API ##################
def sunrise_sunset_API_CALL():

    """ Gets the hours we can see sunlight """

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "date": datetime.now().date(),
        "formatted": 0,
    }
    #response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response = requests.get("https://api.sunrisesunset.io/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    sunlight = {
        "sunrise": sunrise.split(),
        "sunset" : sunset.split(),
    }    
    return sunlight
    
################ MAIN ################

while True:
    time.sleep(300)
    if is_ISS_near() and is_there_sunlight():
        send_email()


############################################################

