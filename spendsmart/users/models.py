from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=320)



