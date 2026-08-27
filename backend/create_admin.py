from app import app, db, User

with app.app_context():

    user = User.query.filter(
        db.or_(
            User.username == "admin",
            User.email == "admin@gmail.com"
        )
    ).first()

    if user:
        user.username = "admin"
        user.email = "admin@gmail.com"
        user.full_name = "Administrator"
        user.role = "admin"
        user.is_active = True
        user.set_password("admin@123")
    else:
        user = User(
            username="admin",
            email="admin@gmail.com",
            full_name="Administrator",
            role="admin",
            is_active=True
        )

        user.set_password("admin@123")
        db.session.add(user)

    db.session.commit()

    print("Admin account ready!")