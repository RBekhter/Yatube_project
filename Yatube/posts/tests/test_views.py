from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Nobody')
        Group.objects.create(
            title='test',
            slug='test_slug',
            description='test description'
        )
        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""

        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/profile.html': (
                reverse('posts:profile',
                        kwargs={'username': self.user.username})
                ),
            'posts/all_groups.html': reverse('posts:all_groups'),
            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': 'test_slug'})
                ),
            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': self.post.id})
                ),
            'posts/author_posts.html': (
                reverse('posts:author_posts',
                        kwargs={'author_id': self.user.id})
                ),
            'posts/create_post.html': reverse('posts:post_create'),
            'posts/create_post.html': (
                reverse('posts:post_edit', kwargs={'post_id': self.post.id})
                ),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом"""

        response = (self.authorized_client.
                    get(reverse('posts:post_detail',
                                kwargs={'post_id': self.post.id})))
        
        self.assertEqual(response.context.get('post').text, 'Test text')
        self.assertEqual(
            response.context.get('post').author, self.user
            )
