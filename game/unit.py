from object import Object, Vec2
from resource import Resource

class Unit(Object):
    spawnedUnits = []
    pass


class Worker(Unit):
    def __init__(self, position=Vec2(0,0), player=None, harvestAmount=10, totalCarry=50):
        super(self.__class__, self).__init__(blocking=False, name="Worker", player=player, texture="units/worker.png", damage=3, health=15, sightRadius=10, range=1, moveDistance=1, position=position)
        self.carrying = { }
        self.harvestAmount = harvestAmount
        self.totalCarry = totalCarry

    def harvest(self, resource):
        """Worker will harvest the specified resource and add to personal inventory, until full"""
        if isinstance(resource, Resource):
            if resource.amount <= 0:
                return
            self.carrying[resource.name] += self.harvestAmount
            resource.amount -= self.harvestAmount
        else:
            raise TypeError(str(type(resource)) + " can not be harvested.")  

        if sum(self.carrying.itervalues()) >= self.totalCarry:
            dropOffResources()

    def dropOffResources(self):
        """Worker will return to the nearest dropoff point and deposit"""
        for k in self.carrying.keys():
            self.player.resources[k] += self.carrying[k]
        self.carrying = {}
        
        

class Solider(Unit):
    def __init__(self, position=Vec2(0,0), player=None):
        super(self.__class__, self).__init__(blocking=False, name="Solider", player=player, texture="units/solider.png", damage=8, health=30, sightRadius=10, range=1, moveDistance=1.1, position=position)

class Scout(Unit):
    def __init__(self, position=Vec2(0,0), player=None):
        super(self.__class__,self).__init__(blocking=False, name="Scout", player=player, texture="units/scout.png", damage=5, health=25, sightRadius=15, range=1.2, moveDistance=1.6, position=position)
