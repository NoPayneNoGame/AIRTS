from object import Vec2

class Resource(object):
    def __init__(self, name=None, amount=0, position=Vec2(0, 0)):
        self.amount = amount
        self.position = position
        self.name = name
        self.blocking = True


class GoldResource(Resource):
    def __init__(self, amount=0, position=Vec2(0, 0)):
        super(GoldResource, self).__init__("gold", amount, position)

