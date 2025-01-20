from app import create_app
from app.db import db

app = create_app()
app.app_context().push()

if __name__ == "__main__":
  with app.app_context():
        db.create_all()
        app.run(debug=True)