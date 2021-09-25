from django.test import TestCase
from .models import Post, Category
from usersapp.models import BlogUser
# faker - простые данные, например случайное имя
from faker import Faker
# FactoryBoy - данные для конкретной модели django
# mixer - полностью создать fake модель
from mixer.backend.django import mixer


# Create your tests here.
class PostTestCase(TestCase):

    def setUp(self):
        category = Category.objects.create(name='test_category')
        user = BlogUser.objects.create_user(username='test_user', email='test@test.com', password='leo1234567')
        self.post = Post.objects.create(name='test_post', text='some', user=user, category=category)

        self.post_str = Post.objects.create(name='test_post_str', text='some', user=user, category=category)

    def test_has_image(self):
        self.assertFalse(self.post.has_image())

    def test_some_method(self):
        post = Post.objects.get(name='test_post')
        self.assertFalse(post.some_method() == 'some method')

    def test_str(self):
        self.assertEqual(str(self.post_str), 'test_post_str, category: test_category')


class PostTestCaseFaker(TestCase):

    def setUp(self):
        faker = Faker()
        category = Category.objects.create(name=faker.name())
        user = BlogUser.objects.create_user(username=faker.name(), email='test@test.com', password='leo1234567')
        self.post = Post.objects.create(name=faker.name(), text=faker.name(), user=user, category=category)

        print(self.post.name)
        print(category.name)

        category = Category.objects.create(name='test_category')
        self.post_str = Post.objects.create(name='test_post_str', text='some', user=user, category=category)

    def test_has_image(self):
        self.assertFalse(self.post.has_image())

    def test_some_method(self):
        self.assertFalse(self.post.some_method() == 'some method')

    def test_str(self):
        self.assertEqual(str(self.post_str), 'test_post_str, category: test_category')


class PostTestCaseMixer(TestCase):

    def setUp(self):
        self.post = mixer.blend(Post)

        # print('mixer-name:', self.post.name)
        # print('mixer-category', self.post.category)
        # print('mixer-category-type', type(self.post.category))
        # print('mixer-user-email', self.post.user.email)
        # Как создать картинку с mixer?

        # Хороший вариант
        # category = mixer.blend(Category, name='test_category')
        # self.post_str = mixer.blend(Post, name='test_post_str', category=category)

        # Короткая запись
        self.post_str = mixer.blend(Post, name='test_post_str', category__name='test_category')

    def test_has_image(self):
        self.assertFalse(self.post.has_image())

    def test_some_method(self):
        self.assertFalse(self.post.some_method() == 'some method')

    def test_str(self):
        self.assertEqual(str(self.post_str), 'test_post_str, category: test_category')