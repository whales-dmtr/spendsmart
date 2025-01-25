from django.db import models
from users.models import Users

class Categories(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return str(self.name)
    
    def update_category_amount(self):
        category = Categories.objects.get(id=self.id)
        spends = category.spends_set.all()  # all spends with this category
        if len(spends) > 0:
            amount_sum = spends.aggregate(Sum('amount'))['amount__sum']
            self.amount_sum = amount_sum
        else:
            self.amount_sum = 0  

        self.save()


class Spends(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    desc = models.CharField(max_length=50)
    amount = models.CharField(max_length=15)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(to=Categories, on_delete=models.SET_NULL, null=True)






