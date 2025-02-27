
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRagistrationApiView.as_view(), name='registar'),
    path('login/', views.UserloginApiview.as_view(), name='login'),
    path('logout/', views.Userlogoutview.as_view(), name='logout'),
    path('active/<uid64>/<token>/', views.activate, name="active"),
    path('change_password/', views.PasswordChangeView.as_view(), name="changepassword")
]