from uuid import uuid4

from flask_jwt_extended import create_access_token

from app.extensions.database import db
from app.models.user import User

# Temporary in-memory reset token storage
# Later we'll replace this with database + email.
reset_tokens = {}


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

    @staticmethod
    def forgot_password(email):

        user = User.query.filter_by(email=email).first()

        if not user:
            return None, "User not found"

        token = str(uuid4())

        reset_tokens[token] = user.id

        return token, None

    @staticmethod
    def reset_password(token, new_password):

        if token not in reset_tokens:
            return "Invalid or expired token"

        user_id = reset_tokens[token]

        user = User.query.get(user_id)

        if not user:
            return "User not found"

        user.set_password(new_password)

        db.session.commit()

        del reset_tokens[token]

        return None