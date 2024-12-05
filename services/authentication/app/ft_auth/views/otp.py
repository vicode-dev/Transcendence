from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from pyotp import TOTP
from ft_auth.utils.otp_2fa import OTPForm, generate_qr_code
from ft_auth.utils.token import get_jwt_data
from django.views.decorators.http import \
    require_http_methods
from ft_auth.utils.user import get_user_by_id

@require_http_methods(["GET", "POST"])
def verify_otp(request):
	data = get_jwt_data(request)
	if data == None or "error" in data:
		return HttpResponseRedirect("/login")
	user = get_user_by_id(data["id"])
	if request.method == 'POST':
		form = OTPForm(request.POST)
		if form.is_valid():
			otp_code = form.cleaned_data['otp_code']
			totp = TOTP(user.otp_secret)
			if totp.verify(otp_code):
				messages.success(request, "Vérification réussie !")
				return redirect('home')
			else:
				messages.error(request, "Code invalide. Réessayez.")
	else:
		form = OTPForm()
	return (generate_qr_code(user))
    # return render(request, 'verify_otp.html', {'form': form})