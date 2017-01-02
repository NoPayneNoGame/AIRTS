class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

class Object(object):
    def __init__(self, blocking=False, name=None, team=None, texture=None, 
            damage=0, health = 0, sightRadius=0, attackDist=0, moveDistance=0, position=Vec2(0, 0)):
        self.blocking = blocking
        self.name = name
        self.team = team
        self.texture = texture
        self.damage = damage
        self.health = health
        self.sightRadius = sightRadius
        self.moveDistance = moveDistance
        self.position = position
        self.attackDist = attackDist

        self.canMove = moveDistance > 0

        print "INFO: Spawning {} at {}".format(self.name, self.position)

    def takeDamage(self, damage):
        if(self.health > 0):
            self.health -= damage;
        else:
            print self.name + " is already dead."


