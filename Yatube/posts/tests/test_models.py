from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, Comment


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Nobody')
        cls.group = Group.objects.create(
            title='Test group',
            slug='Test_slug',
            description='Test description'
        )
        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user
        )
        cls.comment = Comment.objects.create(
            text='Test comment',
            author=cls.user,
            post=cls.post
        )

    def test_models_have_correct_object_names(self):
        """Проверка, что у моделей корректно работает __str__"""

        print(f'{self.test_models_have_correct_object_names.__doc__}')

        post = PostModelTest.post
        group = PostModelTest.group
        comment = PostModelTest.comment

        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

        expected_object_group_name = group.title
        self.assertEqual(expected_object_group_name, str(group))
        
        expected_object_comment_text = comment.text
        self.assertEqual(expected_object_comment_text, str(comment))
