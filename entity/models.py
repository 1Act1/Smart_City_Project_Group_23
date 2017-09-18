from django.db import models

# Create your models here.
class Entity(models.Model):
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 300)
    address = models.CharField(max_length = 100)
    photolink = models.CharField(max_length = 200, default = 'https://aotw-pd.s3.amazonaws.com/media-vimeo/70533052.jpg')
    
    
    positive_review = models.IntegerField(default = 0)
    negative_review = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.id) + ' ' + self.name 
