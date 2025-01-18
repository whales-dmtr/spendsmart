from django.db import models
from users.models import Users

class Categories(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

class Spends(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    desc = models.CharField(max_length=50)
    amount = models.CharField(max_length=15)
    date = models.DateField()
    category = models.ForeignKey(to=Categories, on_delete=models.SET_NULL, null=True)






