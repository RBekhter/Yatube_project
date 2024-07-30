import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Nobody')

    def setUp(self):
        self.post = Post.objects.create(
            text='Test text',
            author=self.user
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_form_create_new_record(self):
        """Отправка валидной формы создания поста создает новую запись в БД"""

        post_count = Post.objects.count()

        small_gif = (
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'text': 'Test text',
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response, reverse(
                'posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(Post.objects.count(), post_count+1)
        self.assertTrue(
            Post.objects.filter(
                text='Test text',
                image='posts/small.gif'
            ).exists()
        )

    def test_edit_post_transform_post(self):
        """При отправке формы редактирования поста происходит
        изменение поста и редирект на страницу просмотра поста"""

        form_data = {
            'text': 'Edit text',
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(self.post.id,)),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id})
        )

        self.assertTrue(
            Post.objects.filter(
                text='Edit text'
            ).exists()
        )
