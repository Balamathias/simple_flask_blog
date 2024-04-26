import unittest
from flask import url_for
from flask_testing import TestCase

from posts.models import User, Post
from posts import app, db


class TestRoutes(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.client.get(url_for('home'))
        self.assert200(response)

    def test_post_detail_route(self):
        post = Post(title='Test Post', content='This is a test post')
        db.session.add(post)
        db.session.commit()
        response = self.client.get(url_for('post_detail', post_id=post.id))
        self.assert200(response)

    def test_register_route(self):
        response = self.client.get(url_for('register'))
        self.assert200(response)

    def test_login_route(self):
        response = self.client.get(url_for('login'))
        self.assert200(response)

    def test_logout_route(self):
        response = self.client.get(url_for('logout'))
        self.assertRedirects(response, url_for('home'))

    def test_account_route(self):
        response = self.client.get(url_for('account'))
        self.assert200(response)

    def test_create_post_route(self):
        response = self.client.get(url_for('create_post'))
        self.assert200(response)

    def test_update_post_route(self):
        post = Post(title='Test Post', content='This is a test post')
        db.session.add(post)
        db.session.commit()
        response = self.client.get(url_for('update_post', post_id=post.id))
        self.assert200(response)

    def test_search_route(self):
        response = self.client.get(url_for('search'))
        self.assert200(response)

    def test_forgot_password_route(self):
        response = self.client.get(url_for('forgot_password'))
        self.assert200(response)

if __name__ == '__main__':
    unittest.main()
