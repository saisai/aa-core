class MongoClient:
    def __init__(self, serverSelectionTimeoutMS: int) -> None:
        ...

    def server_info(self):
        ...

    def __getitem__(self, x: str):
        ...


class Collection:
    ...
