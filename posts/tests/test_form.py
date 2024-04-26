import unittest
from flask import Flask
from flask_testing import TestCase
from posts.form import RegisterForm, LoginForm, UpdateAccountForm, PostForm


class TestForms(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_register_form(self):
        form = RegisterForm()
        self.assertFalse(form.validate())

        form.username.data = 'testuser'
        form.email.data = 'test@example.com'
        form.password.data = 'password'
        form.confirm_password.data = 'password'
        self.assertTrue(form.validate())

    def test_login_form(self):
        form = LoginForm()
        self.assertFalse(form.validate())

        form.email.data = 'test@example.com'
        form.password.data = 'password'
        self.assertTrue(form.validate())

    def test_update_account_form(self):
        form = UpdateAccountForm()
        self.assertFalse(form.validate())

        form.username.data = 'testuser'
        form.email.data = 'test@example.com'
        self.assertTrue(form.validate())

    def test_post_form(self):
        form = PostForm()
        self.assertFalse(form.validate())

        form.title.data = 'Test Post'
        form.content.data = 'This is a test post'
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
