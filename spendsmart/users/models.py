from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)


class Profile(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, unique=True, null=True)
    last_name = models.CharField(max_length=30, unique=True, null=True)
    birthday_date = models.DateField(null=True)
    desc = models.TextField(max_length=200, null=True)