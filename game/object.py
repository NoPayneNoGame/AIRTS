class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Vec2(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        else:
            return False
    
    def euclidDist(self, other):
        if not isinstance(other, Vec2):
            raise TypeError("euclidDist must compare two Vec2 objects, trying to compare {} and {}".format(
                    str(type(self)), str(type(other))))
        return abs(self.x - other.x) + abs(self.y - other.y)

    def closestFromList(self, l):
        if not isinstance(l, list):
            raise TypeError("closestFromList requires List")
        if len(l) == 0:
            raise ValueError("List cannot be empty")
        
        d = {}
        for i in l:
            d[self.euclidDist(i)] = i
        return d[min(d.keys())]
            

class Object(object):
    def __init__(self, blocking=False, name=None, player=None, texture=None, 
            damage=0, health = 0, sightRadius=0, range=0, moveDistance=0, position=Vec2(0, 0)):
        if not player:
            raise ValueError(str(self) + " must have a player")
        self.blocking = blocking
        self.name = name
        self.player = player
        self.texture = texture
        self.damage = damage
        self.health = health
        self.sightRadius = sightRadius
        self.moveDistance = moveDistance
        self.position = position
        self.range = range

        self.canMove = moveDistance > 0

        print "INFO: Spawning {} at {}".format(self.name, self.position)

    def takeDamage(self, damage):
        if self.health > 0:
            self.health -= abs(damage);
        else:
            print self.name + " is already dead."

        if self.health < 0:
            self.health = 0


