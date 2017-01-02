from Object import Object, Vec2

class Building(Object):
    pass


class Base(Building):
    def __init__(self, team=None, position=Vec2(0,0)):
        super(self.__class__, self).__init__(blocking=True, name="Base", team=team, texture="buildings/base.png", damage=2, health=200, sightRadius=20, attackDist=13, moveDistance=0, position=position)

class Barracks(Building):
    def __init__(self, team=None, position=Vec2(0,0)):
        super(self.__class__, self).__init__(blocking=True, name="Barracks", team=team, texture="buildings/barracks.png", damage=0, health=100, sightRadius=13, attackDist=0, moveDistance=0, position=position)


        
