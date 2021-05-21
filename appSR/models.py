from django.db import models


class Numbers(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return self.value


class UserSystem(models.Model):
    name = models.CharField(max_length=30, null=False)
    hash = models.IntegerField()

    def __str__(self):
        return self.name + "#" + self.hash


class UserNumbers(models.Model):
    userID = models.ForeignKey(UserSystem, on_delete=models.CASCADE)
    value = models.IntegerField()
