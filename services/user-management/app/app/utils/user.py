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
	return hashed.hexdigest()

########################################################
###                    Login                         ###
########################################################

def user_login(login, password):
	try:
		user = User.objects.filter(
	  		login=login, password=hash_password(password)).first()
	  		# login=login, password=password).first()
		return user
	except User.DoesNotExist:
		return None

########################################################
###                    Gettors                       ###
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
		user = User.objects.filter(login=login).first()
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
###                    Checkers                      ###
########################################################

def isAlphabet(text, accept_spaces=False):
	for char in text:
		if not char.isalpha() \
      	or (char == " " and accept_spaces == True):
			return False
	return True


def check_user(login, first_name, last_name, password):
	if login is None \
		or first_name is None \
		or last_name is None \
		or password is None:
		return "One or more required fields are empty"

	length = len(login)
	if length == 0:
		return "Your login name isn't an option!"
	if length < 4 or length > 19:
		return "Login size must be between 8 and 19 characters."

	length = len(password)
	if length == 0:
		return "Your password isn't an option!"
	if length < 8 or length > 32:
		return "Password size must be between 8 and 32 characters."

	length = len(first_name)
	if length == 0:
		return "Your first name isn't an option!"
	length = len(first_name) + 1 + len(last_name) 
	if length == 0:
		return "Your first name isn't an option!"
	if length < 8 or length > 32:
		return "Combination of fisrt name and last name must be between 8 and 32 characters."

	if not isAlphabet(login):
		return "Login must contains only alphabetic characters."
	if not isAlphabet(first_name, accept_spaces=True) \
    	or not isAlphabet(last_name, accept_spaces=True):
		return "First and last names must contain only alphabetic characters and spaces."

	if User.objects.filter(login=login).exists():
		return "Login already exists."
	return None

########################################################
###                    Registor                      ###
########################################################

def getLogin(request):
	login = request.POST.get('login')
	if login is None:
		return None
	return login.strip()

def removeMultipleSpaces(name):
	final_name = ""
	space = False
	for char in name:
		if char == ' ':
			if space is False:
				space = True
				final_name = final_name + char
		else:
			space = False
			final_name = final_name + char
	return final_name

def parseName(name):
	if name is None:
		return None
	name = name.strip()
	return removeMultipleSpaces(name)
	
def getFirstName(request):
	name = request.POST.get('first_name')
	return parseName(name)

def getLastName(request):
	name = request.POST.get('last_name')
	return parseName(name)

def create_42_user(user_42):
	user = User(
		ft_id = user_42["id"],
		login=user_42["login"],
		ft_picture = user_42["image"]["link"]
	)
	user.save()
	user = get_user_by_42_id(user_42["id"])
	create_user(user.id, user_42["first_name"], user_42["last_name"])
	return user

def create_classic_user(login, first_name, last_name, password):
	# user = User.objects.filter(login=login).first()
	# if User is not None:
	# 	return user
	user = User(
		login=login,
		password = hash_password(password)
	)
	user.save()
	user = get_user_by_login(login)
	create_user(user.id, first_name, last_name)
	return user

def delete_user(login):
	user = get_user_by_login(login)
	user.delete()