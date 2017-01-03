from object import Object, Vec2
from unit import Unit, Worker, Solider, Scout

class Building(Object):
    def __init__(self, blocking=False, name=None, team=None, texture=None, damage=0, health = 0, sightRadius=0, range=0, moveDistance=0, position=Vec2(0, 0)):
        super(Building, self).__init__(blocking=blocking, name=name, team=team, texture=texture, damage=damage, health=health, sightRadius=sightRadius, range=range, moveDistance=moveDistance, position=position)
        self.allUnits = []
        self.currentUnits = []
        self.waypoint = None

    def spawn(self, id):
        if id >= len(self.currentUnits) || id < 0:
            raise ValueError(self.name + " doesn't have a unit with id: " + str(id))

        loc = self.position + 10
        if self.waypoint:
            loc = self.waypoint

        Unit.spawnedUnits.append(self.currentUnits[id](loc, self.team))

class Base(Building):
    def __init__(self, position=Vec2(0,0), team=None):
        super(Base, self).__init__(blocking=True, name="Base", team=team, texture="buildings/base.png", damage=2, health=200, sightRadius=20, range=13, moveDistance=0, position=position)
        self.allUnits = [Worker]
        self.currentUnits = [Worker]

class Barracks(Building):
    def __init__(self, position=Vec2(0,0), team=None):
        super(Barracks, self).__init__(blocking=True, name="Barracks", team=team, texture="buildings/barracks.png", damage=0, health=100, sightRadius=13, range=0, moveDistance=0, position=position)
        #super(self.__class__, self).__init__(True, name, team, texture, damage, health, sightRadius, range, moveDistance, position)
        self.allUnits = [Solider]
        self.currentUnits = [Solider]

        
