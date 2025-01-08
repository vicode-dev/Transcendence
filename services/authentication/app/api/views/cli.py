########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

### Utils ###

from datetime import datetime, timezone
from api.models import CLI, User
from ft_auth.utils.token import get_jwt_data, decode_jwt, encode_jwt
from api.utils.token import generate_cli_jwt

@csrf_exempt
@require_http_methods(["GET"])
def generate_token(request):
	type = request.GET.get("type")
	if type is None:
		return JsonResponse({
			"error":
					"Invalid request. The \"type\" query parameter is missing. It should be equal to \"persistent\" or \"ephemeral\"."
		})
	if type == "persistent":
		return generate_persistent_token(request)
	elif type == "ephemeral":
		return generate_ephemeral_token(request)
	return JsonResponse({
		"error":
				"Invalid request. The \"type\" query parameter should be equal to \"persistent\" or \"ephemeral\"."
	})

def generate_persistent_token(request):
	data = get_jwt_data(request)
	if "error" in data:
		return JsonResponse({
			"error":
				data["error"]
		})
	cli = CLI.objects.filter(owner_id=data["id"]).first();
	if not cli:
		cli = CLI(owner_id=data["id"]);
		cli.save()
	token = generate_cli_jwt(cli.to_dict(), "persistent")
	return JsonResponse({
			"token":
				token
		})

def get_cli(data):
	try:
		cli = CLI.objects.filter(
	  			id=data["id"]).first()
		iat_datetime = datetime.fromtimestamp(data["iat"], tz=timezone.utc)
		if iat_datetime < cli.token_date:
			return None
		return cli
	except CLI.DoesNotExist:
		return None

def get_user(cli):
	try:
		user = User.objects.filter(
	  			id=cli.owner_id).first()
		return user
	except User.DoesNotExist:
		return None

def generate_ephemeral_token(request):
	authorization = request.META.get('HTTP_AUTHORIZATION')
	if authorization is None:
		return JsonResponse({
			"error":
				"Access forbidden. Authorization header is required."
		})
	data = decode_jwt(authorization)
	if "error" in data:
		return JsonResponse({
			"error":
				data["error"]
		})
	cli = get_cli(data)
	if cli is None:
		return JsonResponse({
			"error":
				"Invalid or expired authorization token."
		})
	user = get_user(cli)
	if user is None:
		return JsonResponse({
			"error":
				"This token isn't linked to any user."
		})
	token = encode_jwt(user.to_dict(), False)
	return JsonResponse({
			"token":
				token
		})