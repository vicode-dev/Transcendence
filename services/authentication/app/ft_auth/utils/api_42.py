import requests

def get_42_user_access(code):
	url = "https://api.intra.42.fr/oauth/token"

	data = {
		"grant_type": "authorization_code",
		"client_id": "u-s4t2ud-d994d34fee9548150795820d0569584f13de3c53f31275bffaf05b5860c6cf9f",
		"client_secret": "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",
		"code": code,
		"redirect_uri": "https://transcendence.vicode.dev/42-oauth2/"
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