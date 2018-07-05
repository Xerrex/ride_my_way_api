"""Defines tests for validator methods"""

from unittest import TestCase, main
from datetime import datetime, timedelta
from app.validators import string_validator, email_validator, \
                            length_validator,action_validator, \
                            date_validator

class TestValidors(TestCase):
    
    def test_string_validator(self):
        """Test String validator"""
        value = ""
        self.assertRaises(ValueError, email_validator, value)
        self.assertRaisesRegex(ValueError, 
                                'field value cannot be empty', 
                                string_validator, value, 'field')

        value = "       "
        self.assertRaisesRegex(ValueError, 'field value cannot contain spaces or tabs only',
                               string_validator, value, 'field')
    
    def test_email_validator(self):
        """Test Email validator"""

        value = "alex@dev.com"
        self.assertEqual(email_validator(value), value)
        
        value = "alexdev.com"
        self.assertRaises(ValueError, email_validator, value)
        self.assertRaisesRegex(ValueError,
                "Invalid email address: Must have '@' " ,
                email_validator, value)

        value = "1234alex@dev.com"
        self.assertRaisesRegex(ValueError, 
                "Invalid email address: Cannot start with digit",
                email_validator, value)

        self.assertRaises(ValueError, email_validator, value)


    def test_length_validator(self):
        """Test Length validor"""
        value = "12345678"
        self.assertEqual(length_validator(value, "password"), value)
        
        value = "123"
        self.assertRaises(ValueError, length_validator, 
                            value, 'password', 5)
        self.assertRaisesRegex(ValueError, 
                "password must contain not less that 5 characters",
                length_validator, value, 'password', 5)
    
    def test_date_validator(self):
        """Test Date validator"""

        currentdate = datetime.now() + timedelta(days=1)
        value = "{}".format(currentdate.strftime("%d-%m-%Y %H:%M"))
        self.assertEqual(date_validator(value,"eta"), value)

        currentdate = datetime.now() - timedelta(days=1)
        value = "{}".format(currentdate.strftime("%d-%m-%Y %H:%M"))
        self.assertRaises(ValueError, date_validator, value, 'eta')
        self.assertRaisesRegex(ValueError, 
                "eta must be greater than the current time now: {}".\
            format(datetime.now().strftime("%d-%m-%Y %H:%M")),
                date_validator, value, 'eta')


    def test_action_validator(self):
        """Test Action validator"""
        value = "accepted"
        self.assertEqual(action_validator(value, "action"), "accepted")

        value="rejected"
        self.assertEqual(action_validator(value, "action"), "rejected")

        value = "come on"
        self.assertRaises(ValueError, action_validator, value, 'action')
        self.assertRaisesRegex(ValueError, 
                "action must be either 'rejected' or 'accepted'",
                action_validator, value, 'action')


if __name__ == "__main__":
    main(verbosity=2)