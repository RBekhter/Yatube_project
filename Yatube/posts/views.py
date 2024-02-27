from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Main page')

def group_list(request):
    return HttpResponse('Groups')

def posts_filter_by_group(request, group_name):
    return HttpResponse(f'Posts about: {group_name}')

#def posts(request, slug):
#   return HttpResponse(f'Post {slug}')
