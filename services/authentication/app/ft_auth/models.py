from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)  
	login = models.CharField(max_length=32)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	ft_picture = models.CharField(max_length=100)#"https://cdn.intra.42.fr/users/be42245c79dd3e8eb3407c5df494d718/rbarbiot.jpg"
	ft_id = models.IntegerField()

	def __str__(self):
		return self.title

# class User(models.User):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, username, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email
