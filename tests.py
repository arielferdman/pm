import random
import json
from land_page_back import valid_email, save_data, db_connection

        
def email_gen(count):
    for i in range(count):
        mail = ''
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',\
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',\
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',\
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',\
            '_', '.', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(random.randint(0, 17)):
            mail += random.choice(alphabet)
        mail += "@"
        mail += random.choice(["gmail", "walla", "yahoo", "outlook"])
        mail += random.choice([".com", ".co.il", ".ru", ".uk"])

        yield mail


def check_email(emails):
    for email in emails:
        print("{:<28} {}".format(email, bool(valid_email(email))))

def check_db():
    db = db_connection()

    json_data = json.loads("""
    {
        "name": "yehuda",
        "email": "yehuda@hfe.org"
    }
    """)

    save_data(db, json_data)


def print_db():
    db = db_connection()
    data = db.users.find()
    for i in data:
        print(i)



def main():

    check_email(email_gen(500))
    
    check_db()

    print_db()




if __name__ == '__main__':
    main()