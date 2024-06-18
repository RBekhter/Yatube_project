from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Test',
            slug='Test slug',
            description='Test description',
        )
        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        post = PostModelTest.post
        group = PostModelTest.group
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))
        expected_object_group_name = group.title
        self.assertEqual(expected_object_group_name, str(group))


