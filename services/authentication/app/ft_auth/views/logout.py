########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

### Utils ###

from ft_auth.utils.token import \
    delete_jwt
from ft_auth.utils.single_page import single_page_redirection

@csrf_exempt
@require_http_methods(["GET"])
def logout(request):
	redirection = single_page_redirection(request)
	if redirection != None:
		return redirection
	response = render(request, "/app/ft_auth/templates/logout.html")
	delete_jwt(response)
	return response