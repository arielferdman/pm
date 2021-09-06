import random
import re
import json
import traceback
from datetime import datetime
from pymongo import MongoClient
from errors import *
import consts
import my_logger


def db_connection():
    conn_str = f"mongodb+srv://{consts.USERNAME}:{consts.PASSWORD}@cluster0.wyznt.mongodb.net/{consts.DB_NAME}?retryWrites=true&w=majority"
    client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    # access the DB named data
    db = client.data
    return db


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)


def valid_name(name):
    regex = r'^[A-Za-z0-9_. ]*$'
    return re.fullmatch(regex, name)


def validate_json(json_data):
    # Check for Email
    if "email" not in json_data.keys():
        raise JsonValidationError(json.dumps(json_data), "No email field")
    # Check if Email is valid
    email = json_data["email"]
    if not valid_email(email):
        raise JsonValidationError(json.dumps(json_data), "Invalid email address")
    # Check if name is valid (only if exists)
    if "name" in json_data.keys():
        name = json_data["name"]
        if not valid_name(name):
            raise JsonValidationError(json.dumps(json_data), "Invalid name")
    # Check if contributor is valid (only if exists)
    if "contributor" in json_data.keys():
        contributor = json_data["contributor"]
        if type(contributor) is not bool: 
            raise JsonValidationError(json.dumps(json_data), "Invalid contributor")


def save_data(db, json_data):
    # First check if Json is valid.
    # If not it will raise LandPageError
    validate_json(json_data)
    email = json_data["email"]
    # Check for duplicate email
    if db.leads.find_one({"email": email}) is not None:
        raise EmailDuplicationError(json.dumps(json_data), "This email address already exists")
    # pull name and contributor
    name = json_data["name"] if "name" in json_data.keys() else ""
    contributor = json_data["contributor"] if "contributor" in json_data.keys() else False
    # get timestamp
    timestamp = datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S")  # TODO - time zone ? israel or utc, but not machine time!

    # insert into db
    lead = {
        "name": name,
        "email": email,
        "timestamp": timestamp,
        "contributor": contributor,
        "test": True #TODO delete in prod
    }
    obj_id = db.leads.insert_one(lead).inserted_id
    return obj_id


def process_data(json_data):
    return json.loads(json_data) #TODO change to json.load in prod.


def run(json_data):
    db = None
    obj_id = None
    try:
        db = db_connection()
        json_string = process_data(json_data)
        obj_id = save_data(db, json_string)
        my_logger.log(db,
                      timestamp=datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S"),
                      code=my_logger.LogCode.d,
                      origin="landing_page",
                      message="successfully inserted a new lead",
                      backstack="run",
                      object_id=obj_id,
                      test=True) #TODO delete in prod. (global varb?)
    except LandPageError as err:
        if db is not None:
            my_logger.log(db,
                          timestamp=datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S"),
                          code=my_logger.LogCode.e,
                          origin="landing_page",
                          message=str(err),
                          backstack="run",
                          traceback=traceback.format_exc(),
                          object_id=obj_id,
                          test=True) #TODO delete inn prod. (global varb?)
    except Exception as err:
            my_logger.log(db,
                          timestamp=datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S"),
                          code=my_logger.LogCode.e,
                          origin="landing_page",
                          message=str(err),
                          backstack="run",
                          traceback=traceback.format_exc(),
                          object_id=obj_id,
                          test=True) #TODO delete inn prod. (global varb?)


def main():

    data = {
        "name": "yehuda",
        "email": "yehuda100" + str(random.randint(1, 6_000_000)) + "@gmail.com",
        "contributor": True,
        "test": True
    }
    j_data = json.dumps(data, indent=4)
    run(j_data)


    

 

if __name__ == '__main__':
    main()
