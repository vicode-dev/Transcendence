########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.utils.translation import gettext as _

### Utils ###

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from os import environ

from ft_auth.utils.api_users import get_user

########################################################
###                    Encode                        ###
########################################################

def encode_jwt(user_info, otp_required):
	user = get_user(user_info["id"], target="role")
	if user is None:
		return None
	header = {
		"alg": "HS256",
  		"typ": "JWT"
	}
	payload = {
		"id": user_info["id"],
		"iat":
			datetime.now(timezone.utc),
		"exp":
			(datetime.now(timezone.utc)
			+ timedelta(days=1)),
		"role": user["role"]
	}
	if otp_required:
		payload["error"] = "OTP required"
	jwt_token = encode(payload, environ['JWT_SECRET_KEY'], algorithm="HS256", headers=header)
	return jwt_token

def decode_jwt(token):
	try:
		payload = decode(token, environ['JWT_SECRET_KEY'], algorithms=["HS256"])
		
		return payload
	except ExpiredSignatureError:
		return {"error": _("Token expired")}
	except InvalidTokenError:
		return {"error": _("Invalid token")}

########################################################
###                    Storage                       ###
########################################################

def save_jwt(response, token, otp_required=False):
	response.set_cookie("session", token)
	if otp_required:
		response.set_cookie("otp", "required")
	else:	
		response.delete_cookie("otp")

def delete_jwt(response):
	response.delete_cookie("session")

def get_jwt(request):
	return request.COOKIES.get("session")

def get_jwt_data(request):
	token = get_jwt(request)
	return decode_jwt(token)

def generate_jwt(response, user_info, otp_required=False):
	token = encode_jwt(user_info, otp_required)
	if token is None:
		return None
	save_jwt(response, token, otp_required)
	return (token)