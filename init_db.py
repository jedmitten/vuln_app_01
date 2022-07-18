from unicodedata import name
from project import db, create_app, models
from werkzeug.security import generate_password_hash

db.create_all(app=create_app())
print("Initializing admin user...")

admin = models.User(
    email="admin@example.com",
    password=generate_password_hash("adminpassword"),
    name="Admin User",
    admin=1
)

db.session.add(admin)
db.session.commit()

print("DB initialization complete...")
