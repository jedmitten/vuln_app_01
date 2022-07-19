from unicodedata import name
from project import db, create_app, models
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all(app=app)
    print("Initializing admin user...")

    # admin user 
    admin = models.User(
        email="admin@example.com",
        password=generate_password_hash("adminpassword"),
        name="Admin User",
        admin=1
    )

    # standard user named alice@example.com w/ password monkey1
    alice = models.User(
        email="alice@example.com",
        password=generate_password_hash("monkey1"),
        name="Alice",
        admin=0
    )

    db.session.add(admin)
    db.session.add(alice)
    db.session.commit()

    print("DB initialization complete...")
