from django.db import models
from account.models import Account

# Create your models here.
class Message(models.Model):
    senderid = models.IntegerField()
    receiverid = models.IntegerField()
    message = models.CharField(max_length = 500)
    deliver_date = models.DateField(auto_now_add=True)
    deliver_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return str(self.senderid) + "-->" + str(self.receiverid) + ": " + self.message
