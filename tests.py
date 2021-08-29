import random
from land_page_back import save_data, db_connection


ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',\
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',\
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',\
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

NUMBERS = [',', '_', '.', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def email_gen():
    mail = ''
    if random.random() > 0.97:
        return mail
    for i in range(random.randint(0, 17)):
        mail += random.choice(ALPHABET + NUMBERS)
    if random.random() > 0.05:
        mail += "@"
    mail += random.choice(["gmail", "walla", "yahoo", "outlook"])
    if random.random() > 0.05:
        mail += random.choice([".com", ".co.il", ".ru", ".uk"])

    return mail

"""
def check_email(emails):
    for email in emails:
        print("{:<30} {}".format(email, bool(valid_email(email))))
"""


def json_gen():
    json_string = {}
    if random.random() > 0.95:
        return json_string
    if random.random() < 0.2:
        json_string["name"] = ''.join([random.choice(ALPHABET) for i in range(random.randint(0, 10))])
    if random.random() < 0.1:
        return json_string
    json_string["email"] = email_gen()
    return json_string

def check_db(count):
    db = db_connection()

    for i in range(count):
        json_data = json_gen()
        try:
            save_data(db, json_data)
        except Exception as ex:
            print("{:<50} {}".format(str(json_data), ex))
        else:
            print(json_data)


def print_db():
    db = db_connection()
    data = db.users.find()
    for i in data:
        print(i)


def delete_db():
    db = db_connection()
    db.users.delete_many({})


def main():

    check_db(5000)

    print_db()

    delete_db()




if __name__ == '__main__':
    main()