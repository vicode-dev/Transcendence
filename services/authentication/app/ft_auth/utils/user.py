from ft_auth.models import User


########################################################
###                    Getters                        ###
########################################################

def get_user_by_id(id):
	try:
		user = User.objects.get(id=id)
		print(user)
		return user
	except User.DoesNotExist:
		return None
	
def get_user_by_42_id(ft_id):
	try:
		user = User.objects.get(ft_id=ft_id)
		print(user)
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
###                    Creators                      ###
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
	return (get_user_by_42_id(user_42["id"]))

def create_classic_user(request):
	return
