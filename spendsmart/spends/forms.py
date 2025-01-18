from django import forms
from .models import Categories

class AddSpendForm(forms.Form):
    description = forms.CharField(max_length=50)
    amount = forms.CharField(max_length=15)
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), required=False)
    date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2025, 2026))
    )

    description.widget.attrs.update({'autocomplete': 'off'})
    amount.widget.attrs.update({'autocomplete': 'off'})
    category.widget.attrs.update({'autocomplete': 'off'})


class CreateCategoryForm(forms.Form):
    name = forms.CharField(max_length=25)

    name.widget.attrs.update({'autocomplete': 'off'})


class EditSpendForm(AddSpendForm):
    def __init__(self, previous_data):
        super().__init__()
        for field_name, field_data in previous_data.items():
            self.fields[field_name].widget.attrs.update({'value': field_data})
            try:
                if int(field_data):
                    print(int(field_data))
                    self.fields[field_name].widget.attrs.update({'selected': ''})
            except:
                continue

        