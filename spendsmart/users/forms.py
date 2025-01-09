from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    username.widget.attrs.update({'class': 'input_field', 'id': 'username_inp', 'autocomplete': 'off'})
    password.widget.attrs.update({'class': 'input_field', 'id': 'password_inp', 'autocomplete': 'off', 'type': 'password'})


class RegisterForm(LoginForm):
    email = forms.EmailField(max_length=254)

    email.widget.attrs.update({'class': 'input_field', 'id': 'email_inp', 'autocomplete': 'off'})


class EditFieldForm(forms.Form):
    field = forms.CharField(max_length=100)

    field.widget.attrs.update({'autocomplete': 'off'})


class PasswordEditForm(EditFieldForm):
    field = forms.CharField(max_length=100)
    field.widget.attrs.update({'autocomplete': 'off', 'type': 'password'})


# class EditFieldForm(forms.Form):
#     def __init__(self, max_len):
#         super().__init__()
 
#     field = forms.CharField(max_length=max_length)
