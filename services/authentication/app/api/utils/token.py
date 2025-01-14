########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.utils.translation import gettext as _

### Utils ###

from jwt import encode
from datetime import datetime, timezone, timedelta
from os import environ

########################################################
###                    Encode                        ###
########################################################

def encode_jwt(data, type):
	header = {
		"alg": "HS256",
  		"typ": "JWT"
	}
	payload = {
		"id": data["id"],
		"iat":
			datetime.now(timezone.utc),
		"exp":
			(datetime.now(timezone.utc)
			+ timedelta(days=15)),
		"type": type
	}
	jwt_token = encode(payload, environ['JWT_SECRET_KEY'], algorithm="HS256", headers=header)
	return jwt_token

########################################################
###                    Storage                       ###
########################################################

def generate_cli_jwt(data, type):
	token = encode_jwt(data, type)
	return (token)