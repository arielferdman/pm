import random
from email import valid_email, get_email

        

for i in range(500):
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

    print(mail, '\t', valid_email(mail))

#############################

json_string = """
{
    "name": "yehuda",
    "email": "xiuw@dlhd.cdkv"
}
"""

print(get_email(json_string))