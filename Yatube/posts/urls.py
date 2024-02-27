from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('groups/', views.group_list),
    path('groups/<slug:group_name>/', views.posts_filter_by_group)
]
