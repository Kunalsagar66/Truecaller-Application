from django.db import models
from account.models import Account
# Create your models here.

class Contact (models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone_number = models.IntegerField()
    is_spam = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Spam (models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    phone_number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.phone_number)