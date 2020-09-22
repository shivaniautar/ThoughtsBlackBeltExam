from django.db import models
from datetime import datetime, timedelta
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        elif User.objects.filter(email=postData['email']):
            errors['email'] = "That email is already registered."
        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters."
        elif postData['password'] != postData['pw_confirm']:
            errors['password'] = "Password does not match confirmation."
        # if len(postData['title'])<3:
        #     errors['title'] = "Title must be greater than three characters long."
        # if len(postData['location'])<3:
        #     errors['location'] = "Location must be greater than three characters long."
        # if len(postData['description'])<3:
        #     errors['description'] = "Description must be greater than three characters long."

        return errors

class ThoughtManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['thoughtName'])<5:
            errors['thoughtName'] = "Title must be at least 5 characters long."
        # if len(postData['description'])<1:
        #     errors['description'] = "Description must be provided!."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Thought(models.Model):
    thoughtName = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    # granted_status = models.CharField(max_length = 255, default="not_granted")
    # user_liked = models.ManyToManyField(User, related_name="likes")
    #RELATIONSHIPS#
    users_who_like = models.ManyToManyField(User, related_name = "likes")
    # date_granted = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ThoughtManager()