"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from views import *

# from .views import book_list, book_detail, book_get, html_page, html

urlpatterns = [
      path('', include("django.contrib.auth.urls")),
    	path('register/', views.),
    # path('books/', book_list, name='book_list'),
    # path('books/<int:pk>/', book_detail, name='book_detail'),
	# path('book_get/<str:user_id>/', book_get, name="book_get"),
	# path('book_html/', html_page, name="html_page"),
	# path('book_html/html', html, name="html"),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
