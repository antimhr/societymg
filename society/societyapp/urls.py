from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path('verify/', views.otp, name='verify'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('guest_dashboard/', views.guest_dashboard, name='guest_dashboard'),
    path('add_news/', views.add_news, name='add_news'),
    path('rent/', views.rent, name='rent'),
    path('buy/', views.buy, name='buy'),
    path('message/', views.message, name='message'),
    path('resident/', views.resident, name='resident'),
    path('visitors/', views.visitors, name='visitors'),
    path("complain/", views.complain, name="complain"),
    path("complain/", views.complain_user, name="complain_user"),

    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="societyapp/reset_password.html"),
         name="reset_password"),
    path("reset_password_sent/",
         auth_views.PasswordResetDoneView.as_view(template_name="societyapp/password_reset_sent.html"),
         name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="societyapp/password_reset_form.html"),
         name="password_reset_confirm"),
    path("reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="societyapp/password_reset_complete.html"),
         name="password_reset_complete"),
]
