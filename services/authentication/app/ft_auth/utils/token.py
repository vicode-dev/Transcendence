from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
import datetime

SECRET_KEY = "TMP_SECRET_KEY_1234"

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
        	datetime.datetime.now(datetime.timezone.utc),
		"exp":
        	(datetime.datetime.now(datetime.timezone.utc)
        	+ datetime.timedelta(minutes=1))
	}

	jwt_token = encode(payload, SECRET_KEY, algorithm="HS256", headers=header)
	return jwt_token

def decode_jwt(token):
	try:
		payload = decode(token, SECRET_KEY, algorithms=["HS256"])
		
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

def get_jwt(request):
	return request.COOKIES.get("session")

def get_jwt_data(request):
    token = get_jwt(request)
    return decode_jwt(token)

def generate_jwt(response, data):
    token = encode_jwt(data)
    save_jwt(response, token)
    return (token);