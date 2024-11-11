from ft_auth.models import User

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

def create_42_user():
	return 

def create_classic_user():
	return

