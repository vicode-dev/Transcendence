from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	login = models.CharField(max_length=32)
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	password = models.CharField(max_length=100, null=True)
	ft_picture = models.CharField(max_length=100, null=True)
	ft_id = models.IntegerField(default=0)
 	#"https://cdn.intra.42.fr/users/be42245c79dd3e8eb3407c5df494d718/rbarbiot.jpg"
	#token = models.CharField(max_length=100)
	def __str__(self):
		return self.login
	def to_dict(self):
		return {
			"id": self.id,
			"login": self.login,
			"first_name": self.first_name,
			"last_name": self.last_name,
			"ft_picture": self.ft_picture,
			"ft_id": self.ft_id,
		}