from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	login = models.CharField(max_length=32)
	password = models.CharField(max_length=100, null=True)
	ft_picture = models.CharField(max_length=100, null=True)
	ft_id = models.IntegerField(default=0)

	def __str__(self):
		return self.login
	def to_dict(self):
		return {
			"id": self.id,
			"login": self.login,
			"ft_picture": self.ft_picture,
			"ft_id": self.ft_id,
		}