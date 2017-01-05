from object import Object, Vec2
from resource import Resource

class Action(Object):
    possibleActions = ["move",     # Vec2 
                       "harvest",  # Resource
                       "attack",   # Object (Enemy Unit or Building)
                       "build",    # Building
                       "interact", # Building (drop off things)
                      ]
    def __init__(self, name, item):
        if name not in Action.possibleActions:
            raise ValueError(name + " is not a possible action.")
        self.name = name
        self.item = item

class Unit(Object):    
    def __init__(self, *args, **kwargs):
        super(Unit, self).__init__(*args, **kwargs)
        self.player.units.append(self)
        self.queuedActions = [ ]


class Worker(Unit):
    def __init__(self, position=Vec2(0,0), player=None, harvestAmount=10, totalCarry=50):
        super(Worker, self).__init__(blocking=False, name="Worker", player=player, texture="units/worker.png", damage=3, health=15, sightRadius=10, range=1, moveDistance=1, position=position)
        self.carrying = {"gold": 0 }
        self.harvestAmount = harvestAmount
        self.totalCarry = totalCarry

    def harvest(self, resource):
        if not isinstance(resource, Resource):
            raise TypeError(str(type(resource)) + " can not be harvested.")  

        if self.position.euclidDist(resource.position) > self.range:
            self.queuedActions.append(Action("move", resource.position))
        self.queuedActions.append(Action("harvest", resource))

        self._harvest(resource) #temp

    def _harvest(self, resource):
        """Worker will harvest the specified resource and add to personal inventory, until full"""
        if not isinstance(resource, Resource):
            raise TypeError(str(type(resource)) + " can not be harvested.")  
            
        if resource.amount <= 0:
            self.dropOffResources()

        self.carrying[resource.name] += self.harvestAmount
        resource.amount -= self.harvestAmount

        if sum(self.carrying.itervalues()) >= self.totalCarry:
            self.dropOffResources()
            

    def dropOffResources(self):
        if not self.player:
            raise ValueError(str(self) + " does not have a player")

        possibleB = [i.position for i in self.player.buildings if i.name in ["Base"]]
        if len(possibleB) == 0:
            raise ValueError("No buildings available to deposit resources")

        b = self.position.closestFromList(possibleB)

        self.queuedActions.append(Action("interact", b) )
        
        self._dropOffResources() #temp

    def _dropOffResources(self):
        """Worker will return to the nearest dropoff point and deposit"""
        for k in self.carrying.keys():
            self.player.resources[k] += self.carrying[k]
            self.carrying[k] = 0
        
        

class Solider(Unit):
    def __init__(self, position=Vec2(0,0), player=None):
        super(Solider, self).__init__(blocking=False, name="Solider", player=player, texture="units/solider.png", damage=8, health=30, sightRadius=10, range=1, moveDistance=1.1, position=position)

class Scout(Unit):
    def __init__(self, position=Vec2(0,0), player=None):
        super(Scout, self).__init__(blocking=False, name="Scout", player=player, texture="units/scout.png", damage=5, health=25, sightRadius=15, range=1.2, moveDistance=1.6, position=position)
