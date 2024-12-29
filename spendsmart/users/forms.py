from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    username.widget.attrs.update({'class': 'input_field', 'id': 'username_inp', 'autocomplete': 'off'})
    password.widget.attrs.update({'class': 'input_field', 'id': 'password_inp', 'autocomplete': 'off', 'type': 'password'})


class RegisterForm(LoginForm):
    email = forms.CharField(max_length=320)

    email.widget.attrs.update({'class': 'input_field', 'id': 'email_inp', 'autocomplete': 'off'})





