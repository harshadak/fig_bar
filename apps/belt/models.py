from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')
PASS_REGEX = re.compile(r'.*[A-Z].*[0-9]')

class RegistrationManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['f_name']) < 3:
            errors["fname"] = "Name should be at least 3 characters"
        if len(postData['u_name']) < 3:
            errors["lname"] = "Username should be at least 3 characters"
        if NAME_REGEX.search(postData['f_name']):
            errors["fname_numb"] = "Name cannot contain any numbers"
        # Might not need this validation
        # if NAME_REGEX.search(postData['u_name']):
        #     errors["lname_numb"] = "Last name cannot contain any numbers"
        
        if len(postData['user_email']) < 3:
            errors["email_len"] = "Email is required"
        if len(postData['user_email']) > 0 and not EMAIL_REGEX.match(postData['user_email']):
            errors["email_format"] = "Please enter a valid email"
        try:
            user_record = User.objects.get(user_name = postData['u_name'])
            errors["username_exist"] = "Username already exists"
        except:
            pass

        
        if len(postData['pass']) < 8:
            errors["pass_len"] = "Password is required and must be at least 8 characters"
        if len(postData['pass']) > 0 and not PASS_REGEX.search(postData["pass"]):
            errors["pass_format"] = "Password must have a number and an uppercase letter"
    
        if postData["pass"] != postData["confirm_password"]:
            errors["pass_confirm"] = "Password and Password Confirmation should match"
        
        return errors



    def login_validator(self, postData):
        errors = {}
        try:
            user_record = User.objects.get(email = postData['user_email'])
            if not bcrypt.checkpw(postData['pass'].encode(), user_record.password.encode()):
                errors["pass_invalid"] = "Wrong Password"
        except:
            errors["username_not"] = "Sorry! We couldn't find this record. Please register with us."

        return errors

    def quote_validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 3:
            errors["quotedby_name"] = "The 'Quoted by' field should contain more than 3 characters"
        if len(postData['message']) < 10:
            errors["message_name"] = "The 'message' field should contain more than 10 characters"
        if len(postData['quoted_by'] or postData['message']) == 0:
            errors["trip_empty"] = "Please enter all the fields"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RegistrationManager()

class Quote(models.Model):
    quoted_by = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    added_by = models.ForeignKey(User, related_name = "added_quote")
    fav_quotes = models.ManyToManyField(User, related_name = "quotesadded")
    objects = RegistrationManager()