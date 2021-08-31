import random
import json
from land_page_back import run, db_connection


ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',\
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',\
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',\
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

NUMBERS = [',', '_', '.', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def email_gen():
    mail = ''
    if random.random() > 0.97:
        return mail
    for _ in range(random.randint(0, 17)):
        mail += random.choice(ALPHABET + NUMBERS)
    if random.random() > 0.05:
        mail += "@"
    mail += random.choice(["gmail", "walla", "yahoo", "outlook"])
    if random.random() > 0.05:
        mail += random.choice([".com", ".co.il", ".ru", ".uk"])

    return mail


def json_gen():
    json_string = {}
    if random.random() > 0.97:
        return json_string
    if random.random() > 0.2:
        json_string["name"] = ''.join([random.choice(ALPHABET) for _ in range(random.randint(0, 10,))])
    if random.random() < 0.05:
        return json_string
    json_string["email"] = email_gen()
    if random.random() > 0.89:
        json_string["contributor"] = True
    elif random.random() < 0.4:
        json_string["contributor"] = False
    return json_string

def check_db(count):
    db = db_connection()

    for i in range(count):
        json_data = json_gen()
        try:
            run(json.dumps(json_data))
        except Exception as ex:
            print("{:<50} {}".format(str(json_data), ex))
        else:
            print(json_data)


def print_db():
    db = db_connection()
    data = db.leads.find()
    for i in data:
        print(i)


def delete_db():
    db = db_connection()
    db.leads.delete_many({"test": True})
    #db.logs.delete_many({"test": True})


def main():

    check_db(25)
    print_db()
    delete_db()



if __name__ == '__main__':
    main()