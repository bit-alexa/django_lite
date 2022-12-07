from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) +
                text_type(user.is_active)
        )

def is_current_user(request_user, user_page):
    can_edit = False
    if user_page == request_user:
        can_edit = True
    return can_edit


def send_email(request, user, form):
    current_site = get_current_site(request)
    mail_subject = 'Activation link has been sent to your email id'
    account_activation_token = TokenGenerator()
    message = render_to_string('registration/act_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def is_valid_token(uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return False
    account_activation_token = TokenGenerator()
    if user is not None and account_activation_token.check_token(user, token):
        return user
