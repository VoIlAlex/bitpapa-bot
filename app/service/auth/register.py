from db.models.users import User
from service.auth.hash import HashService


class RegisterService:
    @staticmethod
    async def register_user(username: str, password: str, get_on_exists: bool = False) -> User:
        password_hash = HashService.hash_password(password)
        user = await User.get_by_username(username)
        if user:
            if get_on_exists:
                return user
        return await User.create(username, password_hash)

    @staticmethod
    async def change_password(username: str, password: str):
        password_hash = HashService.hash_password(password)
        user = await User.get_by_username(username)
        if not user:
            raise RuntimeError("User does not exist.")
        await user.change_password(password_hash)
