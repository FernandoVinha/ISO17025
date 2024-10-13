from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import login_view, register_view, logout_view, invite_user_view, home_view

urlpatterns = [
    path('', home_view, name='home'),  # Página inicial
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('invite/', invite_user_view, name='invite_user'),
    path('register/<str:token>/', register_view, name='register'),

    # Rotas para recuperação de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
