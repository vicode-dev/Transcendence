from django.shortcuts import render, redirect
from django.contrib import messages
from pyotp import TOTP
from ft_auth.utils.otp_2fa import OTPForm
from ft_auth.utils.token import get_jwt_data

def verify_otp(request):
    data = get_jwt_data(request)
    if data == None or "error" in data:
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            user = request.user
            totp = TOTP(user.otp_secret)

            if totp.verify(otp_code):
                # Authentification réussie
                messages.success(request, "Vérification réussie !")
                return redirect('home')
            else:
                messages.error(request, "Code invalide. Réessayez.")

    else:
        form = OTPForm()
    return (generate_qr_code())
    return render(request, 'verify_otp.html', {'form': form})