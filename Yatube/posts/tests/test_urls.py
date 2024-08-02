from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    """Проверка доступности главной станицы"""

    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        print(StaticURLTests.__doc__)
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Nobody')
        cls.group = Group.objects.create(
            title='Test',
            slug='Test-slug',
            description='Test description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test post'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_url_redirect_anonymous_on_login(self):
        """Страница создания поста перенаправит
        неавторизованного пользователя на страницу входа"""

        response = self.guest_client.get('/post/new/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/post/new/')
        )

    def test_urls_uses_correct_template(self):
        """URL адреса используют соответствующий шаблон"""
        print(self.test_urls_uses_correct_template.__doc__)

        templates_url_names = {
            'posts/index.html': '/',
            'posts/all_groups.html': '/groups/all/',
            'posts/profile.html': '/Nobody/',
            'posts/group_list.html': '/group/Test-slug/',
            'posts/post_detail.html': '/post/1/',
            'posts/profile.html': '/my/profile/',
            'posts/create_post.html': '/post/new/',
        }

        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_edit_url_open_author(self):
        """Проверка доступности страницы редактирования поста только автору"""
        print(self.test_edit_url_open_author.__doc__)

        response = self.authorized_client.get('post/1/edit/')

        if self.user.username == self.post.author:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)

        response = self.guest_client.get('post/1/edit/')

        if self.user.username == self.post.author:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)
