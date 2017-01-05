from building import Building, Base, Barracks

class Player:
    def __init__(self, name=None, game=None, team=None):
        self.name = name
        self.game = game
        self.team = team
        self.resources = {"gold": 0 }
        self.allBuildings = [Base, Barracks]
        self.currentBuildings = [Base, None]

    def spawnBuilding(self, id, position):
        if id >= len(self.currentBuildings) or id < 0:
            raise ValueError(str(id) + " out of possible id range.")
        if self.currentBuildings[id] == None:
            raise ValueError("No building unlocked with id: " + str(id))
    
        building = self.currentBuildings[id](position, self)
        Building.spawnedBuildings.append(building)
        return building

    def unlockBuilding(self, id):
        if id >= len(self.allBuildings) or id < 0:
            raise ValueError(str(id) + " is not a valid building id")
        self.currentBuildings[id] = self.allBuildings[id]

