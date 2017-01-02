import uuid

class Game:
    def __init__(self):
        self.id = uuid.uuid1()

    def getId(self):
        return self.id
