import bcrypt


class HashService:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("UTF-8"), salt)
        return hashed.decode("UTF-8")

    @staticmethod
    def check_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("UTF-8"), password_hash.encode("UTF-8"))