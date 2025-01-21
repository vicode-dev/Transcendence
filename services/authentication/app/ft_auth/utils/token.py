########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.utils.translation import gettext as _

### Utils ###

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from os import environ

from ft_auth.utils.api_users import get_user, create_user
from ft_auth.utils.user import get_user_by_id

########################################################
###                    Encode                        ###
########################################################

def encode_jwt(user_info, otp_required = False):
	user = get_user(user_info["id"], target="role")
	if user is None:
		create_user(user_info["id"], user_info["login"], "Wild")
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

def encode_link_jwt(user_info):
	header = {
		"alg": "HS256",
  		"typ": "JWT"
	}
	payload = {
		"42_id": user_info["id"],
		"iat":
			datetime.now(timezone.utc),
		"exp":
			(datetime.now(timezone.utc)
			+ timedelta(days=1)),
		"login": user_info["login"],
  		"first_name": user_info["first_name"],
    	"last_name": user_info["last_name"]
	}
	jwt_token = encode(payload, environ['JWT_SECRET_KEY'], algorithm="HS256", headers=header)
	return jwt_token

def decode_jwt(token, session = True):
	try:
		payload = decode(token, environ['JWT_SECRET_KEY'], algorithms=["HS256"])

		if session:
			user = get_user_by_id(payload["id"])
			if user is None:
				return {"error": _("Unknow user")}

		# if user.token_date.replace(tzinfo=timezone.utc) > datetime.fromtimestamp(payload["iat"]).replace(tzinfo=timezone.utc):
		# 	return {"error": _("Token expired")}
		return payload
	except ExpiredSignatureError:
		return {"error": _("Token expired")}
	except InvalidTokenError:
		return {"error": _("Invalid token")}

########################################################
###                    Storage                       ###
########################################################

def save_jwt(response, token, otp_required=False, login_with_42=False):
	response.set_cookie("session", token, samesite='Strict', max_age=86400, httponly=True, secure=True)
	if login_with_42:
		response.set_cookie("update", "session", samesite='Strict', httponly=False, secure=True)
	else:
		response.delete_cookie("update")
	if otp_required:
		response.set_cookie("otp", "required", samesite='Strict')
	else:	
		response.delete_cookie("otp")
	response.delete_cookie("link")

def save_link_jwt(response, token):
	response.set_cookie("link", token, samesite='Strict', max_age=86400, httponly=True, secure=True)
	response.set_cookie("update", "link", samesite='Strict', httponly=False, secure=True)

def delete_jwt(response):
	response.delete_cookie("session")
	response.delete_cookie("otp")
	response.delete_cookie("update")
	response.delete_cookie("link")

def get_jwt_data(request):
	token = request.COOKIES.get("session")
	return decode_jwt(token)

def get_link_jwt_data(request):
	token = request.COOKIES.get("link")
	return decode_jwt(token, session=False)

def generate_jwt(response, user_info, otp_required=False, login_with_42=False):
	token = encode_jwt(user_info, otp_required)
	if token is None:
		return None
	save_jwt(response, token, otp_required, login_with_42)
	return (token)

def generate_link_jwt(response, user_info):
	token = encode_link_jwt(user_info)
	if token is None:
		return None
	save_link_jwt(response, token)
	return (token)