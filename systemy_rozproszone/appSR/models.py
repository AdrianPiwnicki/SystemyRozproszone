from django.db import models


class Numbers(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return self.value
