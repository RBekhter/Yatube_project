from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from ..models import Group, Post


User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Test',
            slug='Test-slug',
            description='Test description',
        )
        Post.objects.create(
            author=cls.user,
            text='Test post'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Noname')
        self.autorized_client = Client()
        self.autorized_client.force_login(self.user)

    def test_new_url_redirect_anonymous_on_login(self):
        """Страница создания поста перенаправит
        неавторизованного пользователя на страницу входа"""
        response = self.guest_client.get('/post/new/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/post/new/')
        )

    def test_new_url_uses_correct_template(self):
        """Страница создания поста использует соответствующий шаблон"""
        response = self.autorized_client.get('/post/new/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_groups_url_uses_correct_template(self):
        response = self.guest_client.get('/groups/all/')
        self.assertTemplateUsed(response, 'posts/all_groups.html')

    def test_urls_uses_correct_template(self):
        """URL адрес использует соответствующий шаблон"""
        templates_url_names = {
            '/{self.user.username}/': 'posts/profile.html',
            '/groups/all/': 'posts/all_groups.html',
            '/group/Test-slug/': 'posts/group_list.html',
            '/post/1/': 'posts/post_detail.html',
            #'/author/{self.user.pk}/': 'posts/author_posts',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.autorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_edit_url_open_athor(self):
        response = self.autorized_client.get('post/1/edit/')
        a = Post.objects.get(id=1)
        print(a)
        print(self.user.username)
        print(a.author)
        self.assertEqual(response.status_code, 404)

