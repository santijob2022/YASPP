import requests
from dotenv import load_dotenv
import os
import datetime
load_dotenv()

def user_input():
    #return input("What exercise did you do today?: ")
    return "1 hour of Barbell lifting"

###################################### Nutrionix API ######################################
class Nutrionix():
    def __init__(self,user_request,WEIGHT_KG = 60,HEIGHT_CM = 160,AGE=33) -> None:            
        self.ID=os.environ['ID']
        self.API=os.environ['API']
        # This parameters are not mandatory, but can be added if a user form is going to be created
        self.GENDER = 'Male'
        self.WEIGHT_KG = WEIGHT_KG
        self.HEIGHT_CM = HEIGHT_CM
        self.AGE = AGE
        self.url = 'https://trackapi.nutritionix.com'
        self.endpoint = '/v2/natural/exercise'
        self.user_request = user_request
        self.params=None
        self.headers=None
        self.params = {
            "query": f'{user_request}',
            "gender": self.GENDER,
            "weight_kg": self.WEIGHT_KG,
            "height_cm": self.HEIGHT_CM,
            "age": self.AGE,
        }
        self.headers = {
            'x-app-id':self.ID,
            'x-app-key':self.API,    
        }    

    def api_post(self):
        response = requests.post(url=self.url+self.endpoint,json=self.params,headers=self.headers)
        return response.json()
    
###################################### SHEETY API ######################################
class Sheety():
    def __init__(self,nutritionix) -> None:     
        self.nutritionix=nutritionix  
        self.GENDER = 'Male'
        self.url = f'{os.environ["SHEETY"]}'
        self.params = None
        
    def post_Sheety(self):
        for exercise in self.nutritionix.api_post()["exercises"]:
            self.params = {           
                "workout": {
                    "date": datetime.datetime.now().strftime("%d/%m/%Y"),
	                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "exercise":exercise['name'].title(),
                    "duration":exercise["duration_min"],
                    "calories":exercise["nf_calories"],
                    }            
            }
            #print(self.params)
            headers = {'Authorization': os.environ['BEARER_AUTH']}
            response = requests.post(url=self.url,json=self.params,headers=headers)
            print("Rows were successfully added!: ",response.status_code)

######################### START THE PROGRAM #########################
Nutritionix_API=Nutrionix( user_input() )
Sheety(Nutritionix_API).post_Sheety()





