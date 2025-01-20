import requests
from os import environ

def get_user(user_id, target=None):
	url = f"http://user-management:8000/api/player/{user_id}/"

	if target != None:
		url = url + target
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
	except:
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

def delete_user(user_id):
	url1 = f"http://user-management:8000/api/player?playerId={user_id}"
	url2 = f"http://authentication:8000/api/user/{user_id}/"

	headers = {
        "Authorization": environ.get("JWT_SECRET_KEY")
    }
	try:
		response = requests.delete(url1)
		response.raise_for_status()
		response = requests.delete(url2, headers=headers)
		response.raise_for_status()
		return True
	except  Exception as e:
	 	return e
 