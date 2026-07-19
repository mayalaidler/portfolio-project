import os

os.environ['TESTING'] = 'true'

import unittest

from app import app, TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        TimelinePost.delete().execute()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Maya Laidler</title>" in html
        assert "Maya Laidler" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        response = self.client.post("/api/timeline_post", data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': "Hello world, I'm John!",
        })
        assert response.status_code == 200
        post = response.get_json()
        assert post['name'] == 'John Doe'
        assert post['email'] == 'john@example.com'
        assert post['content'] == "Hello world, I'm John!"

        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]['name'] == 'John Doe'

        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Timeline" in html

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com",
            "content": "Hello world, I'm John!",
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": "",
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world, I'm John!",
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
