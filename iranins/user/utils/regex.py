import re


def check_phone(phone):
    check = re.search(r"^(\+98|0)?9\d{9}$", phone)
    return check


def check_email(email):
    check = re.search(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email)
    return check
