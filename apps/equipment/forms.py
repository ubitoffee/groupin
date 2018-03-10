from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class EquipmentForm(forms.Form):
    type = forms.ChoiceField(widget=forms.Select(), choices=([('laptop', _('Laptop')), ('desktop', _('Desktop')), ('모니터', 'monitor')]))
    manufacturer = forms.ChoiceField(widget=forms.Select(), choices=([('samsung', _('Samsung')), ('lg', _('LG')), ('apple', _('Apple'))]))
    model_code = forms.CharField()
    serial_num = forms.CharField()

    owner = forms.ModelChoiceField(widget=forms.Select(), queryset= User.objects.all())
    received_date = forms.DateField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd'}))

    is_rental = forms.BooleanField(required=False)
    rental_date = forms.DateField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd'}))
    return_date = forms.DateField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd'}))

    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(
        Div(
            Div(
                Field('type', css_class='form-control', placeholder='First Name'),
                css_class='form-group has-feedback'
            ),
            Div(
                Field('manufacturer', css_class='form-control', placeholder='Last Name'),
                css_class='form-group has-feedback'
            ),
            Div(
                Field('model_code', css_class='form-control', placeholder='Model Code'),
                css_class='form-group has-feedback'
            ),
            Div(
                Field('serial_num', css_class='form-control', placeholder='Serial Number'),
                css_class='form-group has-feedback'
            ),
            Div(
                Field('owner', css_class='form-control', placeholder='Owner'),
                css_class='form-group has-feedback'
            ),
            Div(
                Field('received_date', css_class='form-control', placeholder='Received Date'),
                css_class='form-group has-feedback'
            ),
            Div(
                Field('is_rental', css_class='form-control checkbox-primary', placeholder='Rental'),
                css_class='form-group has-feedback checkbox'
            ),
            Div(
                Field('rental_date', css_class='form-control', placeholder='Rental Date'),
                css_class='form-group has-feedback'
            ),
            Div(
                Field('return_date', css_class='form-control', placeholder='Return Date'),
                css_class='form-group has-feedback'
            ),
            css_class='box-body'
        ),
        Div(
            Submit(_('Submit'), _('Submit'), css_class='btn btn-primary btn-flat pull-right'),
            css_class='box-footer'
        )
    )
