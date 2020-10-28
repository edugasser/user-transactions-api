from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.id}: {self.name}"
