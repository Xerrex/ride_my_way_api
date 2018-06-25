"""Data validating methods are defined here.

They are constructed to work with Flask-Restful.
"""
import datetime

def string_validator(value, name):
    """ Validate a string value

    Method ensures that the string value
    to be validated is a string with characters
    and spaces. Spaces only are not considered strings.

    :param value:
    :param name:
    """
    message = "{} value cannot be empty".format(name)
    if not value or len(value) == 0:
        raise ValueError(message)
    if value.isspace() is True:
        message = "{} value cannot contain spaces or tabs only".format(name)
        raise ValueError(message)
    return value


def email_validator(value):
    """Validate an email

    Check that passed string is an actual email. Email should
    not start with a number and should contain one '@'

    :param value:
    :return:
    """

    # check if empty or is a space
    string_validator(value, 'email')

    # check if '@' in value
    message = "Invalid email address: Must have '@' "
    if '@' not in value:
        raise ValueError(message)

    if value[0].isdigit():
        message = "Invalid email address: Cannot start with digit"
        raise ValueError(message)
    return value


def length_validator(value, name, min_length=8):
    """Validate length of a value

    Passes the value to string validator before
    checking if value meets required length: min_length

    :param value:
        Value to check length
    :param name:
        name of value  to check length
    :param min_length:
        Minimum length the value should
    :return:
    """
    string_validator(value, name)

    if len(value) < min_length:
        message = "{} must contain not less that {} characters".\
            format(name, min_length)
        raise ValueError(message)
    return value

def date_validator(value, name):
    """Validate date 

    Make sure that the date is greater than today

    :param value:
        Value to validate
    :param name:
        Name of value being validated
    
    :return:
    """
    string_validator(value, name)

    current_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    if value < current_date:
        message = "{} must be greater than the current time now: {}".\
            format(name, current_date)
        raise ValueError(message)
    return

