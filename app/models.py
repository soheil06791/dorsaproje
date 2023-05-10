from django.db import models

# Create your models here.


class DataModel(models.Model):
    a = models.IntegerField()
    b = models.IntegerField()

    def __str__(self):
        return str(self.a + self.b)


class BlockIp(models.Model):
    ip = models.CharField(max_length=16, unique=True)




