from django.db import models

# Create your models here.
class Account(models.Model):
    account_type = models.CharField(max_length = 20)
    username = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100, default = 'NULL')
    password = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 30)
    email_address = models.CharField(max_length = 50)
    residential_address = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.id) + ' ' + self.username
