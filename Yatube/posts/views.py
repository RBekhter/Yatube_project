from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from .forms import PostCreateForm


@login_required
def index(request):
    title = 'Последние обновления на сайте'
    posts = Post.objects.order_by('-pub_date')[:10]
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date'[:10])
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Записи сообщества {group.slug}'
    context = {
        'title': title,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def groups(request):
    title = 'Список групп'
    groups = Group.objects.all()
    context = {
        'title': title,
        'groups': groups,
    }
    return render(request, 'posts/all_groups.html', context)


def profile(request, username: str):
    posts = Post.objects.filter(author__username=username).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    sum_of_posts = len(posts)
    context = {
        'username': username,
        'posts': posts,
        'sum': sum_of_posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    postid = Post.objects.get(id=post_id)
    author = postid.author
    all_posts = Post.objects.filter(author=author)
    sum_of_posts = len(all_posts)
    print(request.user.username)
    print(author)
    context = {
        'postid': postid,
        'sum': sum_of_posts

    }
    return render(request, 'posts/post_detail.html', context)


def author_posts(request, author_id):
    posts = Post.objects.filter(author_id=author_id)

    context = {
        'posts': posts,
    }
    return render(request, 'posts/author_posts.html', context)


def post_create(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save()
            return redirect('posts:profile', request.user.username)
    form = PostCreateForm()
    return render(request, 'posts/create_post.html',
                  {'form': form, 'groups': groups})


def post_edit(request, post_id):
    groups = Group.objects.all()
    is_edit = True
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        form = PostCreateForm(instance=post)
        if form.is_valid():
            post.save()
            form.save()
            return redirect('posts:profile', request.user.username)
    #return render(request, 'posts/create_post.html',
     #             {'form': form, 'as_edit': as_edit, 'groups': groups})
    
    post = Post.objects.get(pk=post_id)
    form = PostCreateForm(instance=post)
    context = {
        'form': form,
        'is_edit': is_edit,
        'groups': groups
    }
    return render(request, 'posts/create_post.html', context)


#class PostCreate(CreateView):
 #   form_class = PostForm
 #   template_name = 'posts/create_post.html'
 #   success_url = 'profile/<str:username>'
