from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.urls import path, reverse_lazy

from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
         name='password_change_done'),

    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             success_url=reverse_lazy('users:password_reset_done')
         ),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done2.html'),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]
