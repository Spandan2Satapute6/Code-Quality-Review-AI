from flask_jwt_extended import create_access_token

from app.extensions.database import db
from app.models.user import User


class AuthService:

    @staticmethod
    def register(name, email, password):

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return None, "User already exists"

        user = User(
            name=name,
            email=email,
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user, None

    @staticmethod
    def login(email, password):

        user = User.query.filter_by(email=email).first()

        if not user:
            return None, "Invalid email or password"

        if not user.check_password(password):
            return None, "Invalid email or password"

        access_token = create_access_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
        }, None