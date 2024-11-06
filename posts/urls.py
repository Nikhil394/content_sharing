from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('posts/', views.view_posts, name='view_posts'),
    path('',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('posts/create_post',views.create_post,name='create_post'),
    path('logout/',views.user_logout,name='logout'),
    path('user_posts/',views.user_posts,name="user_posts"),
    path('delete_post/<pk>/', views.delete_post, name='delete_post'),
    path('edit_post/<pk>/', views.edit_post, name='edit_post'),
    path('delete_account/', views.delete_account, name='delete_account'),
    
]