from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, Comment, Follow, User
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import get_user_model
#from django.views.generic.edit import CreateView
from .forms import PostCreateForm, CommentForm
from django.http import HttpResponse
from django.views.decorators.cache import cache_page


#@cache_page(60 * 0.3, key_prefix='index')
def index(request):
    title = 'Последние обновления на сайте'
    keyword = request.GET.get("q", None)
    if keyword:
        post_list = Post.objects.select_related(
            'author', 'group').filter(text__contains=keyword)
    else:
        post_list = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
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
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author__username=username).order_by('-pub_date')
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

    if not request.user.is_anonymous:
        following = Follow.objects.filter(user=request.user,
                                          author=author).exists()
        context['following'] = following

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    postid = Post.objects.get(id=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post_id)
    print(comments)
    author = postid.author
    all_posts = Post.objects.filter(author=author)
    sum_of_posts = len(all_posts)
    print(request.user.username)
    print(author)
    context = {
        'postid': postid,
        'sum': sum_of_posts,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


def author_posts(request, author_id):
    posts = Post.objects.filter(author_id=author_id)

    context = {
        'posts': posts,
    }
    return render(request, 'posts/author_posts.html', context)


@login_required
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
            #return redirect('posts:post_detail', post.post_id)
    form = PostCreateForm()
    return render(request, 'posts/create_post.html',
                  {'form': form, 'groups': groups})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return HttpResponse('Редактировать пост может только его авторр')

    form = PostCreateForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        #print(post.image)
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    title = 'Избранные публикации'
    post_list = Post.objects.filter(
        author__following__user=request.user).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/index.html', context)


@login_required
def profile_follow(request, username):
    follow_author = get_object_or_404(User, username=username)
    if request.user != follow_author:
        Follow.objects.get_or_create(user=request.user, author=follow_author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    unfollow_from_author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user).filter(
        author=unfollow_from_author).delete()
    return redirect('posts:profile', username=username)


#def postt_edit_old(request, post_id):
 #   groups = Group.objects.all()
 #   is_edit = True
  #  if request.method == 'POST':
  #      post = Post.objects.get(pk=post_id)
  #      form = PostCreateForm(instance=post)
  #      print(post.author)
   #     print(request.user.username)
   #     if str(post.author) == request.user.username:
  #          if form.is_valid():
   #             post.save()
   #             form.save()
   #             return redirect('posts:profile', request.user.username)
   #     else:
  #          return HttpResponse('Редактировать пост может только его автор')

   # post = Post.objects.get(pk=post_id)
   # print(post.author)
   # print(request.user.username)
    #if str(post.author) == request.user.username:
     #   #post = Post.objects.get(pk=post_id)
     #   form = PostCreateForm(instance=post)
     #   context = {
     #       'form': form,
     #       'is_edit': is_edit,
     #       'groups': groups
     #   }
     #   return render(request, 'posts/create_post.html', context)
  #  else:
  #      return HttpResponse('Редактировать пост может только его автор')




#class PostCreate(CreateView):
 #   form_class = PostForm
 #   template_name = 'posts/create_post.html'
 #   success_url = 'profile/<str:username>'
