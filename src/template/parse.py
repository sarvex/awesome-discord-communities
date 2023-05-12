import json
from pathlib import Path
from . import metadata


class DumpMetadata:
    def __init__(self, path: str):
        self.path = Path(path)

    def user(self) -> dict:
        with open(self.path, encoding='utf-8', mode="r") as f:
            u = json.load(f)
        return u

    def server(self) -> dict:
        s = metadata.DiscordCommunityMetadata(self.user()["invite_code"])
        if des := s.parse_data():
            return des
        raise ValueError("Invalid invite code")


class Content:
    def __init__(self, path):
        self.path = Path(path)
        data = DumpMetadata(self.path)
        self.user = data.user()
        self.server = data.server()

    def community(self) -> dict:
        d = {}
        # TODO: For compatibility reasons. For the future: d = d | x
        d |= self.user
        d["name"] = self.server["name"] if not d["name"] else d["name"]
        d["invite_code"] = self.server["invite_code"]
        return d

    def icon(self) -> dict:
        d = {}
        d |= self.server
        d["name"] = self.community().get("name")
        d.pop("invite_code")
        return d
