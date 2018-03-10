from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('email_or_username', css_class='form-control', placeholder='Email Or Username'),
            HTML('<span class="glyphicon glyphicon-user form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Div(
                HTML('<a href="{% url \'accounts:login\' %}" class="text-center">I remember my password</a>'),
                css_class='col-xs-8'
            ),
            Div(
                Submit('Sign In', 'Sign In', css_class='btn btn-primary btn-block btn-flat'),
                css_class='col-xs-4'
            ),
            css_class='row'
        )
    )

    def clean_email_or_username(self):
        _email_or_username = self.cleaned_data['email_or_username']

        if not(User.objects.filter(username=_email_or_username).exists()
                or User.objects.filter(email=_email_or_username).exists()):
            raise forms.ValidationError(_('This username or email address is not existed.'))

        return _email_or_username


class PasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False

    helper.layout = Layout(
        Div(
            Field('new_password1', css_class='form-control', placeholder='Password'),
            HTML('<span class="glyphicon glyphicon-lock form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Field('new_password2', css_class='form-control', placeholder='Retype Password'),
            HTML('<span class="glyphicon glyphicon-lock form-control-feedback"></span>'),
            css_class='form-group has-feedback'
        ),
        Div(
            Div(
                Submit('Submit', 'Submit', css_class='btn btn-primary btn-block btn-flat')
            ),
            css_class='row'
        )
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_('Password mismatch.'))

        return password2
