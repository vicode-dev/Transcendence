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

from django.urls import path, include
from ft_auth.views.oauth2 import login_with_42
from ft_auth.views.routes import register, login, profil

# from .views import book_list, book_detail, book_get, html_page, html

urlpatterns = [
    #   path('', include("django.contrib.auth.urls")),
	# path('login/', login),
	# path('register/', register),
    path('profil', profil),
    path('42-oauth2', login_with_42)

    # path('books/', book_list, name='book_list'),
    # path('books/<int:pk>/', book_detail, name='book_detail'),
	# path('book_get/<str:user_id>/', book_get, name="book_get"),
	# path('book_html/', html_page, name="html_page"),
	# path('book_html/html', html, name="html"),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
