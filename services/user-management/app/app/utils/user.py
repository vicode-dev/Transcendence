from hashlib import md5
from os import environ
from ft_auth.models import User
from ft_auth.utils.api_users import create_user

########################################################
###                    Hash                          ###
########################################################

def hash_password(password):
	altered_password = password+environ['SALT']
	hashed = md5(altered_password.encode())
	print(hashed.hexdigest())
	return hashed.hexdigest()

########################################################
###                    Login                         ###
########################################################

def user_login(login, password):
	try:
		user = User.objects.get(
	  		login=login, password=hash_password(password))
		return user
	except User.DoesNotExist:
		return None

########################################################
###                    Getters                       ###
########################################################

def get_user_by_id(id):
	try:
		user = User.objects.get(id=id)
		# print(user)
		return user
	except User.DoesNotExist:
		return None
	
def get_user_by_42_id(ft_id):
	try:
		user = User.objects.get(ft_id=ft_id)
		# print(user)
		return user
	except User.DoesNotExist:
		return None

def get_user_by_login(login):
	try:
		user = User.objects.get(login=login)
		return user
	except User.DoesNotExist:
		return None

def get_user_by_login(login):
	try:
		user = User.objects.get(login=login)
		return user
	except User.DoesNotExist:
		return None

def get_user_id_by_42_id(ft_id):
	try:
		user = User.objects.only('id').get(ft_id=ft_id)
		print(user.id)
		return user.id
	except User.DoesNotExist:
		return None

def get_user_id_by_login(login):
	try:
		user = User.objects.only('id').get(login=login)
		print(user.id)
		return user.id
	except User.DoesNotExist:
		return None

########################################################
###                    Exists                        ###
########################################################

def	user_login_exists(login):
	return User.objects.filter(login=login).exists()

def	user_name(first_name, last_name):
	return User.objects.filter(first_name=first_name, last_name=last_name).exists()

########################################################
###                    Registor                      ###
########################################################

def create_42_user(user_42):
	user = User(
		ft_id = user_42["id"],
		login=user_42["login"],
		first_name = user_42["first_name"],
		last_name = user_42["last_name"],
		ft_picture = user_42["image"]["link"]
	)
	user.save()
	user = get_user_by_42_id(user_42["id"])
	create_user(user.id, user.first_name, user.last_name)
	return user

def create_classic_user(login, first_name, last_name, password):
	user = User(
		login=login,
		first_name = first_name,
		last_name = last_name
	)
	user.save()
	user = get_user_by_login(login)
	create_user(user.id, user.first_name, user.last_name)
	return user

