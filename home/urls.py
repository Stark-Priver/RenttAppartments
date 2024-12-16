from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('mainpage/<str:user_uid>/<str:username>/', views.MainpageSignedIn, name='mainpage'),
    path('list/', views.listPropety, name='list_propetry'),
    path('login/', views.GoToLogIn, name='login'),
    path('register/', views.GoToRegister, name='register'),
    path('loged/', views.LogInSubmit, name='login_submit'),
    path('registered/', views.RegisterSubmit, name='register_submit'),
    path('gotopost/<str:user_uid>/<str:username>/', views.GoToPost, name='go-to-post'),
    path('details/<str:user_uid>/<str:username>/<str:apt_Id>', views.GoToDetailsAppartment, name='details')
]