from object import Object, Vec2
from unit import Unit, Worker, Solider, Scout

class Building(Object):
    def __init__(self, blocking=False, name=None, player=None, texture=None, damage=0, health = 0, sightRadius=0, range=0, moveDistance=0, position=Vec2(0, 0)):
        super(Building, self).__init__(blocking=blocking, name=name, player=player, texture=texture, damage=damage, health=health, sightRadius=sightRadius, range=range, moveDistance=moveDistance, position=position)
        self.allUnits = []
        self.currentUnits = []
        self.waypoint = None
        self.player.buildings.append(self)

    def spawnUnit(self, id):
        if id >= len(self.currentUnits) or id < 0:
            raise ValueError(self.name + " doesn't have a unit with id: " + str(id))
        
        if self.currentUnits[id] == None:
            raise ValueError(self.name + " doesn't have id: " + str(id) + " unit unlocked.")
    
        loc = self.position + 10
        if self.waypoint:
            loc = self.waypoint

        unit = self.currentUnits[id](loc, self.player)
        #Unit.spawnedUnits.append(unit)
        return unit

    def unlockUnit(self, id):
        if id >= len(self.allUnits) or id < 0:
            raise ValueError(self.name + " doesn't have a unit with id: " + str(id))
        self.currentUnits[id] = self.allUnits[id]


class Base(Building):
    def __init__(self, position=Vec2(0,0), player=None):
        super(Base, self).__init__(blocking=True, name="Base", player=player, texture="buildings/base.png", damage=2, health=200, sightRadius=20, range=13, moveDistance=0, position=position)
        self.allUnits = [Worker]
        self.currentUnits = [Worker]

class Barracks(Building):
    def __init__(self, position=Vec2(0,0), player=None):
        super(Barracks, self).__init__(blocking=True, name="Barracks", player=player, texture="buildings/barracks.png", damage=0, health=100, sightRadius=13, range=0, moveDistance=0, position=position)
        #super(self.__class__, self).__init__(True, name, player, texture, damage, health, sightRadius, range, moveDistance, position)
        self.allUnits = [Solider, Scout]
        self.currentUnits = [Solider, None]

        
