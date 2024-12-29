from django.db import models
from pyotp import random_base32

class User(models.Model):
	id = models.AutoField(primary_key=True)
	login = models.CharField(max_length=19)
	password = models.CharField(max_length=100, null=True)
	ft_id = models.IntegerField(default=0)
	token_date = models.DateTimeField(auto_now=True)
 
	def __str__(self):
		return self.login
	def to_dict(self):
		return {
			"id": self.id,
			"login": self.login,
			"ft_id": self.ft_id,
			"token_date": self.token_date
		}

class CLI(models.Model):
	id = models.AutoField(primary_key=True)
	owner_id = models.IntegerField(default=0)
	token_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.login
	def to_dict(self):
		return {
			"id": self.id,
			"owner_id": self.owner_id,
			"token_date": self.token_date
		}

class OTP(models.Model):
	owner_id = models.IntegerField(default=0)
	secret = models.CharField(max_length=32, default=random_base32, blank=True)
	validated = models.BooleanField(default=False)

	def __str__(self):
		return self.login
	def to_dict(self):
		return {
			"id": self.id,
			"owner_id": self.owner_id,
			"token_date": self.token_date
		}