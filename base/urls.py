from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/<str:pk>', views.profilePage, name='user-profile'),
    path('setting/<str:pk>', views.settingsPage, name="settings"),
    path('update_user/<str:pk>', views.updatePage, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    
    path('delete/<str:pk>', views.deleteMessage, name='delete-message'),
    path('', views.home, name = "home"),
    path('room/<str:pk>/', views.room, name = "room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update/<str:pk>', views.updateRoom, name='update-room'),
    path('delete/<str:pk>', views.deleteRoom, name='delete-room'),

]