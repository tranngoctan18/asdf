import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase

from sqlalchemy.exc import IntegrityError

from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('justatest', 'test@test.com', 'asdf')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('justatest', 'test@test.com', 'asdf')
        duplicate_user = User(
            username='justatest',
            email='test@test2.com',
            password='asdf'
        )
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        # self.assertRaises(
        #     IntegrityError,
        #     db.session.commit  # expressions run in try/
        # )

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'test@test.com', 'adsf')
        duplicate_user = User(
            username='justanothertest',
            email='test@test.com',
            password='asdf'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = User(
            username='justatest',
            email='test@test.com',
            password='asdf'
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user('justatest', 'test@test.com', 'greaterthaneight')
        user_two = add_user('justatest2', 'test@test2.com', 'greaterthaneight')
        self.assertNotEqual(user_one.password, user_two.password)


if __name__ == '__main__':
    unittest.main()
