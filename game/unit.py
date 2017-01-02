from Object import Object, Vec2

class Unit(Object):
    pass


class Worker(Unit):
    def __init__(self, team=None, position=Vec2(0,0)):
        super(self.__class__, self).__init__(blocking=False, name="Worker", team=team, texture="units/worker.png", damage=3, health=15, sightRadius=10, attackDist=1, moveDistance=1, position=position)

class Solider(Unit):
    def __init__(self, team=None, position=Vec2(0,0)):
        super(self.__class__, self).__init__(blocking=False, name="Solider", team=team, texture="units/solider.png", damage=8, health=30, sightRadius=10, attackDist=1, moveDistance=1.1, position=position)

class Scout(Unit):
    def __init__(self, team=None, position=Vec2(0,0)):
        super(self.__class__,self).__init__(blocking=False, name="Scout", team=team, texture="units/scout.png", damage=5, health=25, sightRadius=15, attackDist=1.2, moveDistance=1.6, position=position)
