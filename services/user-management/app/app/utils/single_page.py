from django.http import HttpResponseRedirect

# Verifie si la requete a bien etait faite coté
# javascript
def is_js_request(request):
	return ((request.headers.get('X-Requested-With') == 'XMLHttpRequest'))

# Crée une redirection pour passer par la single page si 
# nécessaire, retourne None si ce n'est pas le cas.
def single_page_redirection(request):
	if is_js_request(request):
		return None

	url = request.path
	query_params = request.GET.copy()
	# if login_page == True:
	# 	query_params["redirect_url"] = "login/"
	# else:
	query_params["redirect_url"] = url[1:]
	# if "error" in data and login_page == False:
	# 	new_url = f"/login/?{query_params.urlencode()}"
	# else:
	new_url = f"/?{query_params.urlencode()}"
	return HttpResponseRedirect(new_url)