from django.db import models

# Create your models here.

class Short_url(models.Model):
    shortdata = models.CharField(max_length = 100)
    longdata = models.CharField(max_length = 100)

    def __str__(self):
        return self.shortdata