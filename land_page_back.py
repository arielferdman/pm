import random
import re
import json
from datetime import datetime
from pymongo import MongoClient
import consts
import my_logger


class LandPageException(Exception):
    pass


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return str(self.expression + "!!!" + self.message)


def db_connection():
    print("db_connection")
    conn_str = f"mongodb+srv://{consts.USERNAME}:{consts.PASSWORD}@cluster0.wyznt.mongodb.net/{consts.DB_NAME}?retryWrites=true&w=majority"
    client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    # access the DB named data
    db = client.data
    return db


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)


def valid_name(name):
    regex = r'\b^[A-Za-z0-9 ]+\b'
    return re.fullmatch(regex, name)


# def get_data():
#    json_file = None #TODO get the json file from the front end and return python dict.
#    json_data = json.loads(json_file) #TODO change to json.load when geting a json file
#    return json_data


def validate_json(json_data):
    print("validate_json")
    # Check for Email
    if "email" not in json_data.keys():
        raise InputError(json.dumps(json_data), "No email field")  # TODO bild exception class - EmailNotFound
    # Check if Email is valid
    email = json_data["email"]
    if not valid_email(email):
        raise InputError(json.dumps(json_data), "Invalid email address")  # TODO InvalidEmail
    # Check if name is valid (only if exists)
    if "name" in json_data.keys():
        name = json_data["name"]
        if not valid_name(name):
            raise InputError(json.dumps(json_data), "Invalid name")  # TODO Invalid Name
    # Check if  is valid (only if exists)
    if "contributor" in json_data.keys():
        contributor = json_data["contributor"]
        if type(contributor) is not bool:
            raise InputError(json.dumps(json_data), "Invalid contributor")  # TODO Invalid Name
    return True


def save_data(db, json_data):
    print("save_data")
    # First check if Json is valid.
    # If not it will raise LandPageException
    validate_json(json_data)
    # Json data is valid!
    print("valid json!")
    email = json_data["email"]
    # Check for duplicate email
    if db.leads.find_one({"email": email}) is not None:
        raise InputError(json.dumps(json_data), "EmailDuplication")  #TODO EmailDuplication
        # ("Email address is already exists in the database")

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
        "test": True
    }
    obj_id = db.leads.insert_one(lead).inserted_id
    return obj_id


def process_data(json_data):
    return json.loads(json_data)


def run(json_data):
    print("run")
    db = None
    obj_id = None
    try:
        db = db_connection()
        json_string = process_data(json_data)
        obj_id = save_data(db, json_string)
        print("saved data! ", obj_id)
        my_logger.log(db,
                      timestamp=datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S"),
                      code=my_logger.LogCode.d,
                      origin="landing_page",
                      message="successfully inserted a new lead",
                      backstack="run",
                      object_id=obj_id,
                      test=True)
    except InputError as err:
        if db is not None:
            my_logger.log(db,
                          timestamp=datetime.now().strftime(r"%d/%m/%Y, %H:%M:%S"),
                          code=my_logger.LogCode.e,
                          origin="landing_page",
                          message=err.__str__(),
                          backstack="run",
                          object_id=obj_id,
                          test=True)
        print("InputError: " + err.__str__())
    except Exception as err:
        # TODO what to do in this case???
        print("EXCEPTION: " + err.__str__())
    print("end run")


def main():
    print("main")
    data = {
        "name": "Eli Hirsch",
        "email": "eli.b.hirsch" + str(random.randint(1, 6_000_000)) + "@gmail.com",
        "contributor": True,
        "test": True
    }
    j_data = json.dumps(data, indent=4)
    run(j_data)
    print("end main")


if __name__ == '__main__':
    main()
