import requests

def get_user(user_id, target=None):
	url = f"http://user-management:8000/api/player/{user_id}/"

	if target != None:
		url = url + target
	# try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
	# except ConnectionError:
	# 	return {"error":"connection failed"}