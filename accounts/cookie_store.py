"""Load and save session cookies per account."""


class CookieStore:
    def __init__(self, base_path: str = "./data/cookies") -> None:
        self.base_path = base_path
