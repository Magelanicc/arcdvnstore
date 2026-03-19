"""
URL configuration for arcdvn_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import admin_dashboard, admin_manage_games, admin_transactions
from core import views

urlpatterns = [
    path('', views.home_user, name='home-user'),
    path('login/', views.login_admin, name='login-admin'),
    path('logout/', views.logout_admin, name='logout-admin'),
    path('admin/', admin.site.urls),
    path('admin-custom/', admin_dashboard, name='admin-dashboard'),
    path('admin-custom/games/', admin_manage_games, name='admin-games'),
    path('admin-custom/transactions/', admin_transactions, name='admin-transactions'),
    path('delete-game/<int:game_id>/', views.delete_game, name='delete-game'),
    path('order/<slug:slug>/', views.game_detail, name='game-detail'),
    path('', admin_dashboard), 
    path('api/pay-check/<str:invoice_id>/', views.api_check_payment, name='api-pay-check'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)