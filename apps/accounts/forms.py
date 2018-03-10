from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from phonenumber_field.formfields import PhoneNumberField

from .models import Account


class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('username', css_class='form-control', placeholder='User'),
            HTML('<span class="glyphicon glyphicon-user form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('password', css_class='form-control', placeholder='Password'),
            HTML('<span class="glyphicon glyphicon-lock form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('first_name', css_class='form-control', placeholder='First Name'),
            HTML('<span class="glyphicon glyphicon-user form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('last_name', css_class='form-control', placeholder='Last Name'),
            HTML('<span class="glyphicon glyphicon-user form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('email', css_class='form-control', placeholder='Email'),
            HTML('<span class="glyphicon glyphicon-envelope form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Div(
                HTML('<a href="{% url \'accounts:login\' %}" class="text-center">I already have a membership</a>'),
                css_class='col-xs-8'
            ),
            Div(
                Submit('Register', 'Register', css_class='btn btn-primary btn-block btn-flat'),
                css_class='col-xs-4'
            ),
            css_class='row'
        )
    )

    def clean_username(self):
        _username = self.cleaned_data['username']

        if User.objects.filter(username=_username).exists():
            raise forms.ValidationError(_("This username has already existed."))
        return _username

    def clean_email(self):
        _email = self.cleaned_data['email']

        if User.objects.filter(email=_email).exists():
            raise forms.ValidationError(_("This email address has already existed."))
        return _email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('username', css_class='form-control', placeholder='User'),
            HTML('<span class="glyphicon glyphicon-user form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('password', css_class='form-control', placeholder='Password'),
            HTML('<span class="glyphicon glyphicon-lock form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(

            Div(
                Div(
                    HTML('<label><input type="checkbox"> Remember Me </label>'),
                    css_class='checkbox icheck'
                ),
                css_class='col-xs-8'
            ),
            Div(
                Submit('Sign In', 'Sign In', css_class='btn btn-primary btn-block btn-flat'),
                css_class='col-xs-4'
            ),
            css_class='row'
        )
    )


class ModifyForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    rank = forms.ChoiceField(widget=forms.Select(), choices=([('사원', '사원'), ('주임', '주임'), ('대리', '대리')]))
    department = forms.ChoiceField(widget=forms.Select(), choices=([('IT비즈니스', 'IT비즈니스'), ('디지털마케팅', '디지털마케팅'), ('경영지원', '경영지원')]))
    team = forms.CharField()
    location = forms.CharField(required=False)
    birthday = forms.DateField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd'}))
    join_date = forms.DateField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd'}))
    phone_number = PhoneNumberField(required=False)
    about_me = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols' : 20}))

    password = forms.CharField(widget=forms.PasswordInput, required=False)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = True

    helper.layout = Layout(
        Div(
            Field('first_name', css_class='form-control', placeholder='First Name'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('last_name', css_class='form-control', placeholder='Last Name'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('rank', css_class='form-control', placeholder='Rank'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('department', css_class='form-control', placeholder='Department'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('team', css_class='form-control', placeholder='Team'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('location', css_class='form-control', placeholder='Location'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('birthday', css_class='form-control', placeholder='Birthday'),
            css_class='form-group has-feedback date'
        ),
        Div(
            Field('join_date', css_class='form-control', placeholder='Join Date'),
            css_class='form-group has-feedback date'
        ),
        Div(
            Field('phone_number', css_class='form-control', placeholder='Phone Number'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('about_me', css_class='form-control', placeholder='About Me'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('password', css_class='form-control', placeholder='Password'),
            css_class='form-group has-feedback'
        ),
        Div(
            Div(
                Submit('Sign In', 'Sign In', css_class='btn btn-primary btn-block btn-flat')
            ),
            css_class='row'
        )
    )
