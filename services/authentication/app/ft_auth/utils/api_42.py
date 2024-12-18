import requests
from os import environ

def get_42_user_access(code):
	url = "https://api.intra.42.fr/oauth/token"

	data = {
		"grant_type": "authorization_code",
		"client_id": environ.get("CLIENT_42_ID"),
		"client_secret": environ.get("CLIENT_42_SECRET"),
		"code": code,
		"redirect_uri": f"https://{environ.get("DOMAIN_NAME")}/42-oauth2/"
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

def get_42_url():
    return f"https://api.intra.42.fr/oauth/authorize?client_id={environ.get("CLIENT_42_ID")}&redirect_uri=https%3A%2F%2F{environ.get("DOMAIN_NAME")}%2F42-oauth2%2F&response_type=code"

def get_context(context = None):
    if context is None:
        return {
			"domain_name": get_42_url()
		}
    context["domain_name"] = get_42_url()
    return context