from django.db import models
from users.models import Users
from django.db.models import Sum

class Categories(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)
    amount_sum = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    def __str__(self):
        return str(self.name)

    # def __repr__(self):
    #     return str(self.name)
    
    def update_category_amount(self):
        category = Categories.objects.get(id=self.id)
        if len(category.spends_set.all()) > 0:
            amount_sum = category.spends_set.all().aggregate(Sum('amount'))['amount__sum']
            self.amount_sum = amount_sum
        else:
            self.amount_sum = 0  

        self.save()


class Spends(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    desc = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(to=Categories, on_delete=models.SET_NULL, null=True)






