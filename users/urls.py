from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#from django.views.generic import TemplateView

urlpatterns = [
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'  # users folder ka path diya
    ), name='password_change'),

    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'  # users folder ka path diya
    ), name='password_change_done'),
]

