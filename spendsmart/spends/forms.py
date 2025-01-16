from django import forms
from .models import Categories

class AddSpendForm(forms.Form):
    description = forms.CharField(max_length=50)
    amount = forms.CharField(max_length=15)
    category = forms.ModelChoiceField(queryset=Categories.objects.all())

    description.widget.attrs.update({'class': 'input_field', 'id': 'desc_inp', 'autocomplete': 'off'})
    amount.widget.attrs.update({'class': 'input_field', 'id': 'amount_inp', 'autocomplete': 'off'})
    category.widget.attrs.update({'class': 'input_field', 'id': 'catg_inp', 'autocomplete': 'off'})


class CreateCategoryForm(forms.Form):
    name = forms.CharField(max_length=25)

    name.widget.attrs.update({'autocomplete': 'off'})

