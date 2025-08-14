from datetime import datetime, timezone, timedelta
import jwt

class JWTHandler:

    def __init__(self):
        self.algorithm: str = "RS256"
        self.private_key = self._load_key("./.ssh/app.key")
        self.public_key = self._load_key("./.ssh/app.pub")


    def decode_token(self, token: str) -> dict:
        header: dict = jwt.get_unverified_header(token)
        
        decoded_token: dict = jwt.decode(token, self.public_key, [header['alg']])
        
        return decoded_token

    def generate_token(self, user_id: str, roles: list[str], expiration_minutes: int = 120) -> str:

        expiration: datetime = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)

        payload = {
            "sub":user_id,
            "roles": roles,
            "exp":expiration
        }

        token: str = jwt.encode(payload, self.private_key, self.algorithm)
        return token
        
        
    def _load_key(self, path: str) -> str:
        with open(path) as f:
            key: str = f.read()
        
        return key