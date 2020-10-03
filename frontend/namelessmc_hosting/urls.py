"""namelessmc_hosting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from users import views as users
from users.views import WebsiteListView, WebsiteDetailView, WebsiteCreateView, WebsiteUpdateView, WebsiteDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('register/', users.register, name='register'),
    path('account/', users.account, name='account'),
    path('websites/', WebsiteListView.as_view(), name='websites'),
    path('website/<int:pk>/', WebsiteDetailView.as_view(), name='website-detail'),
    path('website/new/', WebsiteCreateView.as_view(), name='website-new'),
    path('website/<int:pk>/edit/', WebsiteUpdateView.as_view(), name='website-update'),
    path('website/<int:pk>/delete/', WebsiteDeleteView.as_view(), name='website-delete'),
    path('website/<int:pk>/db-pass-regen/', users.website_db_pass_regen, name='website-db-pass-regen'),
    path('login/', auth.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path('payment_complete', TemplateView.as_view(), name='payment-complete'),
    path('payment_cancelled', TemplateView.as_view(), name='payment-cancelled'),
]
