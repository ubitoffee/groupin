from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail.message import EmailMessage
from django.core.validators import validate_email
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from apps.accounts.password_forms import PasswordResetRequestForm, PasswordChangeForm
from groupin import settings

from django.utils.translation import ugettext as _


def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def password_reset_request(request):

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data['email_or_username']

            if validate_email_address(data) is True:
                users = User.objects.filter(email=data)
            else:
                users = User.objects.filter(username=data)

            if users.exists():
                for user in users:
                    current_site = get_current_site(request)
                    subject = (_('%s Password Reset') % current_site.name)
                    message = render_to_string(
                        'accounts/password_reset/password_reset_email.html',
                        {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': PasswordResetTokenGenerator().make_token(user)
                        }
                    )

                    email = EmailMessage(subject, message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
                    email.send()

            context = {
                'body_class': 'account-page'
            }

            return render(request, 'accounts/password_reset/password_reset_waiting.html', context)
        else:
            context = {
                'form': form,
                'body_class': 'account-page'
            }

            return render(request, 'accounts/password_reset/password_reset_request.html', context)

    else:
        form = PasswordResetRequestForm()
        context = {
            'form': form,
            'body_class': 'account-page'
        }

        return render(request, 'accounts/password_reset/password_reset_request.html', context)


def password_reset_confirm(request, **kwargs):

    uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
    token = kwargs['token']

    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):

        if request.method == "POST":
            form = PasswordChangeForm(request.POST)

            if form.is_valid():
                new_password = form.cleaned_data["new_password2"]
                user.set_password(new_password)
                user.save()

                context = {
                    'body_class': 'account-page',
                    'expired': False
                }
                return render(request, 'accounts/password_reset/password_reset_complete.html', context)

            else:
                context = {
                    'form': form,
                    'body_class': 'account-page'
                }

                return render(request, 'accounts/password_reset/password_reset_confirm.html', context)
        else:
            context = {
                'form': PasswordChangeForm(),
                'body_class': 'account-page'
            }

            return render(request, 'accounts/password_reset/password_reset_confirm.html', context)

    else:
        context = {
            'body_class': 'account-page',
            'expired': True
        }
        return render(request, 'accounts/password_reset/password_reset_complete.html', context)
