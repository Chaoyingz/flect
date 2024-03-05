import json
from pathlib import Path


class Storage:
    JSON_URI = Path(__file__).parent / "todos.json"

    def __init__(self) -> None:
        if not self.JSON_URI.exists():
            self.JSON_URI.touch(exist_ok=True)

    def insert(self, item: dict) -> None:
        with self.JSON_URI.open("a") as f:
            f.write(f"{json.dumps(item)}\n")

    def list(self) -> list[dict]:
        with self.JSON_URI.open("r") as f:
            return [json.loads(line) for line in f]


storage = Storage()
