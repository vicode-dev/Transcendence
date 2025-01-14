from os import environ

# Sert à générer le token depuis les settings
def resquest_cli_token(request, access_token):
	url = f"https://${environ.get("DOMAIN_NAME")}"

	headers = {
        "Authorization": access_token
    }

	response = request.get(url, headers=headers)
	return response.json()    