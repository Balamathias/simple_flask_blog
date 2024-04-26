import unittest
from datetime import datetime
from flask import current_app
from posts import db
from posts.models import User, Post


class TestModels(unittest.TestCase):

    def setUp(self):
        self.user = User(username='testuser', email='test@example.com', password='password')
        self.post = Post(title='Test Post', content='This is a test post', author=self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.password, 'password')
        self.assertEqual(self.user.picture, 'default.jpg')

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.date_posted.date(), datetime.now().date())

    def test_user_post_relationship(self):
        self.assertEqual(self.user.posts, [self.post])
        self.assertEqual(self.post.author, self.user)

if __name__ == '__main__':
    unittest.main()
