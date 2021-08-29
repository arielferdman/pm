import re
import json
from datetime import datetime
from pymongo import MongoClient
import consts


def db_connection():

    #TODO create secure environment variables or oder way to store secret info

    conn_str = f"mongodb+srv://{consts.USERNAME}:{consts.PASSWORD}@cluster0.wyznt.mongodb.net/{consts.DB_NAME}?retryWrites=true&w=majority"
    client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    db = client.test
    return db


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

def get_data():

    json_file = None #TODO get the json file from the front end and return python dict

    json_data = json.loads(json_file) #TODO change to json.load when geting a json file
    return json_data

def save_data(db, data):
    if not "email" in data.keys():
        raise Exception("Email field not exists") #? Do you have better exception for this one?
    
    email = data["email"]
    if not valid_email(email):
        raise Exception("Unvalid email address") #? And do you have better exception for this one?

    if db.users.find_one({"email": email}) != None:
        raise Exception("Email address is already exists in the database") #? And for this one?

    timestamp = datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S") #TODO - time zone ? israel or utc, but not machine time!
    #? do we need to use _id field for each user and if so how to generate it
    #? but if we dont mongo add something like - '_id': ObjectId('612b6386ca405a7a4b7a1591')

    db.users.insert_one({"email": email, "timestamp": timestamp})


def main():
    db = db_connection()
    
    #data = get_data()
    #save_data(db, data)


if __name__ == '__main__':
    main()