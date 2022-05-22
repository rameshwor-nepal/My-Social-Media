from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin , name= 'signin'),
    path('signout/', views.signout , name = 'signout'),
    path('setting/', views.settings, name = 'setting'),
    path('upload/', views.upload, name='upload'),
    path('like/', views.liked_by, name = 'like'),
    path('profile/<str:pk>/', views.profile, name = 'profile'),
    
]