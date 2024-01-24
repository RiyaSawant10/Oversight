"""oversight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.views.generic.base import TemplateView

from oversight import views

urlpatterns = [
    #path('',TemplateView.as_view(template_name='home.html')),
    path('admin/', admin.site.urls),
    path('gradpred/', include('gradpred.urls')),
    path('', views.index,name="home"),
    path('home/', views.index,name="home"),
    path('forums/', views.forums,name="forums"),
    path('pro_ideas', views.pro_ideas,name="pro_ideas"),
    path('notes',views.notes,name="notes"),
    path('contact', views.contact,name="contact"),
    path('saved/',views.saved,name="saved"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]
