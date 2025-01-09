import requests

def get_42_user_access(code):
	url = "https://api.intra.42.fr/oauth/token"

	data = {
		"grant_type": "authorization_code",
		"client_id": "u-s4t2ud-d994d34fee9548150795820d0569584f13de3c53f31275bffaf05b5860c6cf9f",
		"client_secret": "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",
		"code": code,
		"redirect_uri": "http://localhost:8000/42-oauth2"
	}

	headers = {
        "Content-Type": "application/vnd.api+json"
    }

	response = requests.post(url, json=data)#, headers=headers)
	response.raise_for_status()

	return response.json()

def get_42_user(access_token):
	url = "https://api.intra.42.fr/v2/me"

	headers = {
        "Authorization": "Bearer " + access_token
    }

	response = requests.get(url, headers=headers)
	return response.json()