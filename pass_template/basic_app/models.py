from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):


# extend class like oONeTOONE instead of inheritance in inheritace we cant add new it will affect Database
    #   user=models.OneToOneField(User)

      user = models.OneToOneField(User, on_delete=models.CASCADE)


    #   additional thing
      portfolio_site=models.URLField(blank=True)

      profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

      def __str__(self):
            return self.user.username


