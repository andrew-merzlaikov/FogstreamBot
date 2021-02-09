from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)

    first_name.null = True
    last_name.null = True
    username.null = True

    def __str__(self):
        return "{username}".format(username=self.username)