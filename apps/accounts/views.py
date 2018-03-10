from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from apps.accounts.forms import ModifyForm
from groupin import settings
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():

            # User 생성 후 active False 처리
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.is_active = False
            new_user.save()

            # Send User activation mail
            current_site = get_current_site(request)
            subject = ('Welcome To %s! Confirm Your Email' % current_site.name)
            message = render_to_string(
                'accounts/user_activation/user_activation_email.html',
                {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': PasswordResetTokenGenerator().make_token(new_user)
                }
            )

            email = EmailMessage(subject, message, to=[new_user.email], from_email=settings.EMAIL_HOST_USER)
            email.send()

            # login(request, new_user)
            return render(request, 'accounts/user_activation/user_activation_waiting.html',
                          {'body_class': 'account-page'})

        else:
            return render(request, 'accounts/register.html', {'form': form, 'body_class': 'register-page'})

    else:
        if request.user.is_authenticated():
            return redirect('/')
        else:
            form = UserForm()
            return render(request, 'accounts/register.html', {'form': form, 'body_class': 'register-page'})


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': LoginForm(),
                'failure': True,
                'body_class': 'login-page'
            }
            return render(request, 'accounts/login.html', context)

    else:
        if request.user.is_authenticated():
            return redirect('/')
        else:
            form = LoginForm()
            return render(request, 'accounts/login.html', {'form': form, 'body_class': 'login-page'})


def activate_user(request, **kwargs):

    uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
    token = kwargs['token']

    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()

    return render(request, 'accounts/user_activation/user_activation_complete.html', {'body_class': 'account-page'})


@login_required
def profile(request, username=None):

    context = {}

    if request.method == "POST":
        form = ModifyForm(request.POST)

        if form.is_valid():

            account = request.user.account
            account.rank = form.cleaned_data['rank']
            account.department = form.cleaned_data['department']
            account.team = form.cleaned_data['team']
            account.location = form.cleaned_data['location']
            account.birthday = form.cleaned_data['birthday']
            account.join_date = form.cleaned_data['join_date']
            account.phone_number = form.cleaned_data['phone_number']
            account.about_me = form.cleaned_data['about_me']

            request.user.save()

            context = {
                'name': request.user.get_full_name(),
                'rank': account.rank,
                'department': account.department,
                'team': account.team,
                'location': account.location,
                'birthday': account.birthday,
                'join_date': account.join_date,
                'phone_number': account.phone_number,
                'about_me': account.about_me
            }

        context['form'] = form

    else:

        try:
            user = User.objects.get(username=username)

            context = {
                'name': user.get_full_name(),
                'rank': user.account.rank,
                'department': user.account.department,
                'team': user.account.team,
                'location': user.account.location,
                'birthday': user.account.birthday,
                'join_date': user.account.join_date,
                'phone_number': user.account.phone_number,
                'about_me': user.account.about_me
            }

            if request.user.is_authenticated() and user.username == request.user.username:

                initial = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'rank': user.account.rank,
                    'department': user.account.department,
                    'team': user.account.team,
                    'location': user.account.location,
                    'birthday': user.account.birthday,
                    'join_date': user.account.join_date,
                    'phone_number': user.account.phone_number,
                    'about_me': user.account.about_me
                }

                form = ModifyForm(initial=initial)
                context['form'] = form

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            context = {}

    return render(request, 'accounts/profile.html', context)
