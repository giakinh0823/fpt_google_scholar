from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
    
        user = sociallogin.user
        print(user)
        print(user.email)
        if user.id:
            return
        if not user.email:
            return

        try:
            user = User.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
  