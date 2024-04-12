from django.urls import path

from . import views
#from .views import MainView

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
    path('groups/', views.groups, name='all_groups'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('author/<int:author_id>/', views.author_posts, name='author_posts'),
    #path('create/', views.PostCreate.as_view, name='post_create'),
    path('post/new/',
         views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]
