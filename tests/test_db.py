import os

os.environ["TESTING"] = "true"

import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jame@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        timeline_posts = list(TimelinePost.select().order_by(TimelinePost.created_at.desc()))
        assert len(timeline_posts) == 2
        assert timeline_posts[0].name == second_post.name
        assert timeline_posts[0].email == second_post.email
        assert timeline_posts[0].content == second_post.content
        assert timeline_posts[1].name == first_post.name
        assert timeline_posts[1].email == first_post.email
        assert timeline_posts[1].content == first_post.content
