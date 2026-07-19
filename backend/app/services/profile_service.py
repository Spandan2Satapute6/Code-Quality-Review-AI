from app.extensions.database import db
from app.models.user import User


class ProfileService:

    @staticmethod
    def get_profile(user_id):

        user = User.query.get(user_id)

        if not user:
            return None, "User not found"

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }, None

    @staticmethod
    def update_profile(user_id, name):

        user = User.query.get(user_id)

        if not user:
            return None, "User not found"

        user.name = name

        db.session.commit()

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }, None

    @staticmethod
    def change_password(user_id, old_password, new_password):

        user = User.query.get(user_id)

        if not user:
            return "User not found"

        if not user.check_password(old_password):
            return "Current password is incorrect"

        user.set_password(new_password)

        db.session.commit()

        return None