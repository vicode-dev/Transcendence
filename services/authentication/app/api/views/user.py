########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponse
from django.utils.translation import gettext as _

### Utils ###

from os import environ
from django.views.decorators.http import \
    require_http_methods
from api.models import User, OTP, CLI

@require_http_methods(["DELETE", "GET"])
def request_user(request, userId):
	if request.headers.get('Authorization') != environ.get("JWT_SECRET_KEY"):
		return HttpResponse(environ.get("JWT_SECRET_KEY"), status=403)
	user = User.objects.filter(id=userId).first()
	if user is not None:
		user.delete()
	otp = OTP.objects.filter(owner_id=userId).first();
	if otp is not None:
		otp.delete()
	cli = CLI.objects.filter(owner_id=userId).first()
	if cli is not None:
		cli.delete()
	return (HttpResponse())
