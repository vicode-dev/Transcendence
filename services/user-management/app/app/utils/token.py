from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from os import environ

from app.utils.api_users import get_user

########################################################
###                    Encode                        ###
########################################################

def encode_jwt(data):
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
			+ timedelta(hours=1)),
		"role": get_user(data["id"], target="role")["role"]
	}

	jwt_token = encode(payload, environ['JWT_SECRET_KEY'], algorithm="HS256", headers=header)
	return jwt_token

def decode_jwt(token):
	try:
		payload = decode(token, environ['JWT_SECRET_KEY'], algorithms=["HS256"])
		
		return payload
	except ExpiredSignatureError:
		return {"error": "Token expiré"}
	except InvalidTokenError:
		return {"error": "Token invalide"}

########################################################
###                    Storage                       ###
########################################################

def save_jwt(response, token):
	response.set_cookie("session", token)

def delete_jwt(response):
	response.delete_cookie("session")

def get_jwt(request):
	return request.COOKIES.get("session")

def get_jwt_data(request):
	token = get_jwt(request)
	return decode_jwt(token)

def generate_jwt(response, data):
	token = encode_jwt(data)
	save_jwt(response, token)
	return (token)