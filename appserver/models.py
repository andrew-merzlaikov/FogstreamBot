from django.db import models


class UserTelegram(models.Model):
    """
    Stores a single user entry, related to :model:`use.User`
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)

    first_name.null = True
    last_name.null = True
    username.null = True

    def __str__(self):
        """ Representation the User """
       
        return "{first_name} {last_name} {username} ".format(
                                                            username=self.username,
                                                            first_name=self.first_name,
                                                            last_name=self.last_name)

