from app import app
from models import db, connect_db, Cupcake
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
db.create_all()

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        Cupcake.query.delete()

        self.client = app.test_client()

        self.cupcake = Cupcake(
            flavor='testing', size='small', rating=10)
        db.session.add(self.cupcake)
        db.session.commit()

    def test_show_cupcake(self):
        """/cupcakes should show all cupcakes"""
        response = self.client.get("/cupcakes")
        response_data = response.json['cupcakes']
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, [{
                                    "flavor": "testing",
                                    "id": self.cupcake.id,
                                    "image": "https://tinyurl.com/truffle-cupcake",
                                    "rating": 10.0,
                                    "size": "small"
                                    }])

    def test_add_cupcake(self):
        """/cupcakes should add a new cupcake"""

        response = self.client.post(
            "/cupcakes", json={
                "flavor": "testing",
                "size": "small",
                "rating": 10,
                "image": ""
            })
        response_data = response.json['cupcake']
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {
                                    "flavor": "testing",
                                    "id": response_data['id'],
                                    "image": "https://tinyurl.com/truffle-cupcake",
                                    "rating": 10.0,
                                    "size": "small"
                                    })

    def test_update_cupcake(self):
        """/cupcakes/<id> should update a cupcake"""

        response = self.client.patch(
           f"/cupcakes/{self.cupcake.id}", json={
                "flavor": "testing2",
                "size": "large",
                "rating": 8,
                "image": ""
            })

        response_data = response.json['cupcake']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {
                                    "flavor": "testing2",
                                    "id": response_data['id'],
                                    "image": None,
                                    "rating": 8.0,
                                    "size": "large"
                                    })
       
    def test_delete_cupcake(self):
        """/cupcakes/<id> should delete a cupcake"""

        response = self.client.delete(f"/cupcakes/{self.cupcake.id}")
        response_data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {'message': 'deleted'})