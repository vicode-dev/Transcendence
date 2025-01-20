"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_auth.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from api.views.routes import generate_token, \
	request_qr_code, validate_otp_code, check_otp_state, \
    disable_otp, request_user

urlpatterns = [
	path('api/cli/token/', generate_token),
	path('api/otp/qr-code/', request_qr_code),
	path('api/otp/validate/', validate_otp_code),
	path('api/otp/enabled/', check_otp_state),
	path('api/otp/disable/', disable_otp),
	path('api/user/<int:userId>/', request_user)
]
