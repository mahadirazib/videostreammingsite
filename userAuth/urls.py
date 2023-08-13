from django.urls import path
from . import views

app_name = 'userAuth'


urlpatterns = [
    path('', views.loginFunction, name='loginFunction'),
    path('logout/', views.logoutFunction, name='logoutFunction'),
    path('registration/', views.registrationFunction, name='registrationFunction'),
    path('edit/', views.editFunction, name='editFunction'),
]
