import unittest
import json
from app import create_app
from app.db import db
from app.models.grocery_item import GroceryItem, Store

class GroceryAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables and initialize app."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB for testing
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_grocery_item(self):
        """Test creating a new grocery item."""
        payload = {
                "store": "Walmart",
                "customName": "Butter",
                "basePrice": 5.98,
                "url": "https://www.walmart.ca/en/ip/Great-Value-Salted-Butter/6000200237828"
            }
        response = self.client.post("/api/items", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Grocery item created", response.get_json()["message"])

    def test_get_all_grocery_items(self):
        """Test retrieving all grocery items."""
        # Add test data
        with self.app.app_context():
            item = GroceryItem(customName="Apple", url='https://test.com/343345', basePrice=0.5, store=Store.WALMART)
            db.session.add(item)
            db.session.commit()

        response = self.client.get("/api/items")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["customName"], "Apple")

    def test_get_single_grocery_item(self):
        """Test retrieving a single grocery item."""
        # Add test data
        with self.app.app_context():
            item = GroceryItem(customName="Banana", url='https://test.com/343345', basePrice=0.5, store=Store.NOFRILLS)
            db.session.add(item)
            db.session.commit()

        response = self.client.get("/api/items/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["customName"], "Banana")
        self.assertEqual(data["store"], "NoFrills")

    def test_update_grocery_item(self):
        """Test updating an existing grocery item."""
        # Add test data
        with self.app.app_context():
            item = GroceryItem(customName="Orange", url='https://test.com/343345', basePrice=1.0, store=Store.SUPERSTORE)
            db.session.add(item)
            db.session.commit()

        payload = {
            "basePrice": 1.0,
            "store": "Sobeys"
        }
        response = self.client.put("/api/items/1", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Grocery item updated", response.get_json()["message"])

        # Verify the update
        with self.app.app_context():
            updated_item = GroceryItem.query.get(1)
            self.assertEqual(updated_item.basePrice, 1.0)
            self.assertEqual(updated_item.store, Store.SOBEYS)

    def test_delete_grocery_item(self):
        """Test deleting a grocery item."""
        # Add test data
        with self.app.app_context():
            item = GroceryItem(customName="Grapes", url='https://test.com/343345', basePrice=0.5, store=Store.NOFRILLS)
            db.session.add(item)
            db.session.commit()

        response = self.client.delete("/api/items/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Item deleted", response.get_json()["message"])

        # Verify the deletion
        with self.app.app_context():
            deleted_item = GroceryItem.query.get(1)
            self.assertIsNone(deleted_item)

    def test_create_grocery_item_invalid_store(self):
        """Test creating a grocery item with an invalid store."""
        payload = {
            "store": "InvalidStore",
            "customName": "Butter",
            "basePrice": 5.98,
            "url": "https://www.walmart.ca/"
            
        }
        response = self.client.post("/api/items", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid store name", response.get_json()["error"])

    def test_get_nonexistent_item(self):
        """Test retrieving an item that doesn't exist."""
        response = self.client.get("/api/items/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Item not found", response.get_json()["error"])

    def test_update_nonexistent_item(self):
        """Test updating an item that doesn't exist."""
        payload = {
            "basePrice": 1.0,
            "store": "Sobeys"
        }
        response = self.client.put("/api/items/999", json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Item not found", response.get_json()["error"])

    def test_delete_nonexistent_item(self):
        """Test deleting an item that doesn't exist."""
        response = self.client.delete("/api/items/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Item not found", response.get_json()["error"])

if __name__ == "__main__":
    unittest.main()
