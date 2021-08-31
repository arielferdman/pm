import re
import json
from datetime import datetime
from pymongo import MongoClient
from Exceptions import *
import consts  

def db_connection():
    #! here we assume that we already heva a working db and collection named users!
    #TODO create secure environment variables or oder way to store secret info

    conn_str = f"mongodb+srv://{consts.USERNAME}:{consts.PASSWORD}@cluster0.wyznt.mongodb.net/{consts.DB_NAME}?retryWrites=true&w=majority"
    client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    # access to the DB named data
    db = client.data
    return db


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)


def get_data():
    json_file = None #TODO get the json file from the front end and return python dict.
    json_data = json.loads(json_file) #TODO change to json.load when geting a json file
    return json_data


def save_data(db, json_data):
    if not "email" in json_data.keys():
        raise Exception("Email field not exists") #TODO bild exception class - EmailNotFound
    
    email = json_data["email"]
    if not valid_email(email):
        raise Exception("Invalid email address") #TODO InvalidEmail

    if db.users.find_one({"email": email}) != None:
        raise Exception("Email address is already exists in the database") #TODO EmailDuplication

    name = json_data["name"] #! validation, build another func for json_validation 
    contributor = json_data["contributor"] #! validation, default value - False
    timestamp = datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S") #TODO - time zone ? israel or utc, but not machine time!
    db.users.insert_one({"name": name, "email": email, "timestamp": timestamp, "contributor": contributor})


def main():
    db = db_connection()
    
    #json_data = get_data()

    #save_data(db, json_data) #TODO! Exceptions without try-catch!
    try:
        x = db.users.insert_one({"name": "yehuda", "email": "yehuda@hfe.org", "timestamp": datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S")})
        #raise EmailDuplicationError()
        #raise JsonValidationError('"name" field is required.')
        #raise LandPageException("test")
    except Exception as ex:
        print(type(ex).__name__, "=>", ex)
    else:
        print(x.inserted_id)

if __name__ == '__main__':
    main()