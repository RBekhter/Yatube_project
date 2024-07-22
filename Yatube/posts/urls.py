from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
    path('groups/all/', views.groups, name='all_groups'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('author/<int:author_id>/', views.author_posts, name='author_posts'),
    path('my/profile/', views.profile, name='my_profile'),
    path('post/new/',
         views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('follow/index/', views.follow_index, name='follow_index'),
    path('<str:username>/follow/', views.profile_follow, name='follow'),
    path('<str:username>/unfollow/', views.profile_unfollow, name='unfollow'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
