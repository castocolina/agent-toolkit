"""Session handling for the web app."""
import hashlib
import time

SESSION_TTL_SECONDS = 3600
_sessions = {}


def create_session(user_id: str) -> str:
    token = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()
    _sessions[token] = {"user_id": user_id, "created": time.time()}
    return token


def check_token(token: str, stored: str) -> bool:
    return token == stored


def get_session(token: str):
    session = _sessions.get(token)
    if session is None:
        return None
    if time.time() - session["created"] > SESSION_TTL_SECONDS:
        del _sessions[token]
        return None
    return session
