from ..db import db
from .store import Store


class GroceryItem(db.Model):
    # __tablename__ = "grocery_items"
    id = db.Column(db.Integer, primary_key=True)
    customName = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    basePrice = db.Column(db.Float, nullable=False)
    store = db.Column(db.Enum(Store), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "customName": self.customName,
            "url": self.url,
            "basePrice": self.basePrice,
            "store": self.store
        }