from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    username.widget.attrs.update({'class': 'input_field', 
                                  'id': 'username_inp', 
                                  'autocomplete': 'off'})
    password.widget.attrs.update({'class': 'input_field', 
                                  'id': 'password_inp',
                                  'autocomplete': 'off', 
                                  'type': 'password'})


class RegisterForm(LoginForm):
    email = forms.EmailField(max_length=254)

    email.widget.attrs.update({'class': 'input_field', 'id': 'email_inp', 'autocomplete': 'off'})


class EditFieldForm(forms.Form):
    def __init__(self, hint, max_len=100):
        super().__init__()
        self.fields['field'].max_length = max_len
        self.fields['field'].widget.attrs.update({'autocomplete': 'off', 'placeholder': hint, 'autofocus': ''})

    field = forms.CharField(max_length=100)


class PasswordEditForm(EditFieldForm):
    def __init__(self):
        super().__init__(max_len=20, hint='Password')

    field = forms.CharField(max_length=100, widget=forms.PasswordInput())


class EmailEditForm(forms.Form):
    def __init__(self):
        super().__init__()
        self.fields['field'].widget.attrs.update({'autocomplete': 'off',
                                                  'placeholder': 'Email',
                                                  'autofocus': ''})

    field = forms.EmailField()


class BirthdayEditForm(forms.Form):
    def __init__(self):
        super().__init__()
        self.fields['field'].widget.attrs.update({'autocomplete': 'off',
                                                  'placeholder': 'Birthday',
                                                  'autofocus': ''})

    field = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1950, 2026))
    )


class DescEditForm(EditFieldForm):
    def __init__(self, hint=None):
        super().__init__(hint='About you')
        if hint != None:
            self.fields['field'].initial = hint
    field = forms.CharField(max_length=200, widget=forms.Textarea)

