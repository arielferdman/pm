import re
import json
from datetime import datetime


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

def get_email(data):
    json_data = json.loads(data) #TODO change to json.load when geting a json file
    if not "email" in json_data.keys():
        return False #TODO! ex? no email 
    email = json_data["email"]
    if not valid_email(email):
        return False #TODO! ex? invalid email
    else:
        return True # retorn email adress


#TODO
#obj = {"email": email, "time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
#obj.save in MongoDB

print(datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S"))

