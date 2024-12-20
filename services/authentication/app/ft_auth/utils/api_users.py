import requests

def get_user(user_id, target=None):
	url = f"http://user-management:8000/api/player/{user_id}/"

	if target != None:
		url = url + target
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
	except:
		print("ERROR")
		if target is not None:
			return None
		return {"error":"Connection failed, come back later."}

def create_user(user_id, first_name, last_name):
	url = f"http://user-management:8000/api/player?playerId={user_id}&username={first_name}%20{last_name}"
	# headers = {
    #     "Authorization": "Bearer " + access_token
    # }
	try:
		response = requests.get(url)
		response.raise_for_status()
		return True
	except:
	 	return False