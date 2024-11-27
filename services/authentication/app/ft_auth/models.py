from django.db import models
from pyotp import random_base32

class User(models.Model):
	id = models.AutoField(primary_key=True)
	login = models.CharField(max_length=19)
	password = models.CharField(max_length=100, null=True)
	ft_picture = models.CharField(max_length=100, null=True)
	ft_id = models.IntegerField(default=0)
	otp_secret = models.CharField(max_length=32, default=random_base32, blank=True)

	def __str__(self):
		return self.login
	def to_dict(self):
		return {
			"id": self.id,
			"login": self.login,
			"ft_picture": self.ft_picture,
			"ft_id": self.ft_id,
			"opt_secret": self.otp_secret
		}