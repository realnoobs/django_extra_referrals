import hashlib
from urllib import parse
from django.db import models
from django.utils import translation
from django.contrib.auth.models import AbstractUser

_ = translation.ugettext_lazy


class User(AbstractUser):
    avatar_size = 72
    avatar_default = 'mp'  # "https://www.example.com/default.jpg"
    is_referral = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    def avatar(self):
        gravatar_host = "https://www.gravatar.com/avatar/"
        gravatar_url = gravatar_host + hashlib.md5(str(self.email.lower()).encode('utf-8')).hexdigest() + "?"
        gravatar_url += parse.urlencode({
            's': str(self.avatar_size), 'f': 'y', 'd': self.avatar_default
        })
        return gravatar_url


class Donation(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.fullname


class Withdraw(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.fullname
