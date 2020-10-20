import os

import mysql.connector
import requests
from app.generator import Converter


def to_greeklish(msg):
    return Converter(max_expansions=2).convert(msg)[-1]


def get_from_internet(number):
    data = requests.get('https://www.11888.gr/search/reverse/?phone=' + number).json()
    try:
        name_dict = data['data']['wp'][0]['name']
        name = f"{name_dict['last'] or ''} {name_dict['middle'] or ''} {name_dict['first'] or ''}"
        return to_greeklish(name)
    except:
        pass
    try:
        name_dict = data['data']['wp']['name']
        name = f"{name_dict['last'] or ''} {name_dict['middle'] or ''} {name_dict['first'] or ''}"
        return to_greeklish(name)
    except:
        pass


def get_from_db(number):
    try:
        sql_accounts = f'SELECT * FROM account_phones where phone like "%{number}%"'
        sql_contacts = f'SELECT * FROM contact_phones where phone like "%{number}%"'

        mysql_db = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST') or "192.168.111.98",
            port=os.environ.get('MYSQL_PORT') or 3311,
            user=os.environ.get('MYSQL_USER') or "yetiforce",
            password=os.environ.get('MYSQL_PASSWORD') or "yetiforce",
            database=os.environ.get('MYSQL_DATABASE') or "yetiforce"
        )

        db_cursor = mysql_db.cursor()
        db_cursor.execute(sql_accounts)
        for (name, phone) in db_cursor.fetchall():
            return to_greeklish(name)

        db_cursor.execute(sql_contacts)
        for (name, phone) in db_cursor.fetchall():
            return to_greeklish(name)
    except:
        pass


def get_name_phone(number):
    """Order of lookup: CRM Accounts, CRM Contacts, OTE 11888

    :param number: the phone number
    :return:Tuple of: name or None, True if the number is register on CRM
    """
    name = get_from_db(number)
    if name:
        return name, True
    name = get_from_internet(number)
    if name:
        return name, False
    return None, False
