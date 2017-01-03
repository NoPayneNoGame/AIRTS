from game.object import Object, Vec2
from game.unit import Unit, Worker, Solider, Scout
from game.building import Building, Base, Barracks

import unittest

class Vec2Test(unittest.TestCase):
    def setUp(self):
        self.v = Vec2(5, 7)
    
    def test_vec2_string(self):
        self.assertEqual(str(self.v), "(5, 7)")

    def test_vec2_repr(self):
        self.assertEqual(repr(self.v), "(5, 7)")

    def test_vec2_add_vec2(self):
        self.assertEqual(Vec2(5, 2) + self.v, Vec2(10, 9))

    def test_vec2_add_vec2_reverse(self):
        self.assertEqual(self.v + Vec2(5, 2), Vec2(10, 9))

    def test_vec2_add_int(self):
        self.assertEqual(self.v + 2, Vec2(7, 9))

    def test_vec2_add_int_reverse(self):
        self.assertEqual(2 + self.v, Vec2(7, 9))

    def test_vec2_add_float(self):
        self.assertRaises(TypeError, lambda: self.v + 2.5)

    def test_vec2_eq_vec2_self(self):
        self.assertEqual(self.v, self.v)

    def test_vec2_eq_vec2(self):
        self.assertEqual(self.v, Vec2(5, 7))

    def test_vec2_eq_vec2_reverse(self):
        self.assertEqual(Vec2(5, 7), self.v)

    def test_vec2_not_eq(self):
        self.assertNotEqual(self.v, Vec2(7, 5))



class BaseTest(unittest.TestCase):
    def setUp(self):
        self.base = Base(Vec2(10, 10), "red")
    
    def test_base_team_red(self):
        self.assertEqual(self.base.team, "red")

    def test_base_position_10_10(self):
        self.assertEqual(self.base.position, Vec2(10, 10))

    def test_base_team_default_none(self):
        base = Base()
        self.assertIsNone(base.team) 

    def test_base_position_default_0_0(self):
        base = Base()
        self.assertEqual(base.position, Vec2(0, 0))

    def test_base_spawnUnit_worker(self):
        w = self.base.spawnUnit(0)
        self.assertIsInstance(w, Worker)

    def test_base_spawnUnit_too_high(self):
        self.assertRaises(ValueError, self.base.spawnUnit, 1)

    def test_base_spawnUnit_negative(self):
        self.assertRaises(ValueError, self.base.spawnUnit, -1)

    def test_base_unlockUnit_nothing_to_unlock(self):
        self.assertRaises(ValueError, self.base.unlockUnit, 1)

    def test_base_can_move(self):
        self.assertFalse(self.base.canMove)

    def test_base_take_damage_small(self):
        self.base.takeDamage(1)
        self.assertEqual(self.base.health, 199)

    def test_base_take_damage_large(self):
        self.base.takeDamage(500)
        self.assertEqual(self.base.health, 0)

    def test_base_take_damage_199(self):
        self.base.takeDamage(199)
        self.assertEqual(self.base.health, 1)

    def test_base_take_damage_multiple_times(self):
        self.base.takeDamage(10)
        self.base.takeDamage(10)
        self.base.takeDamage(10)
        self.base.takeDamage(10)
        self.assertEqual(self.base.health, 160)

    def test_base_take_damage_negative(self):
        self.base.takeDamage(-10)
        self.assertEqual(self.base.health, 190)

    def test_base_set_waypoint(self):
        self.base.waypoint = Vec2(30, 12)
        self.assertEqual(self.base.waypoint, Vec2(30, 12))

    def test_base_spawn_at_waypoint(self):
        self.base.waypoint = Vec2(30, 12)
        w = self.base.spawnUnit(0)
        self.assertEqual(w.position, self.base.waypoint)

    def test_base_spawn_worker_correct_team(self):
        w = self.base.spawnUnit(0)
        self.assertEqual(w.team, "red")

class BarracksTest(unittest.TestCase):
    def setUp(self):
        self.bar = Barracks()

    def test_barracks_spawn_solider(self):
        s = self.bar.spawnUnit(0)
        self.assertIsInstance(s, Solider)

    def test_barracks_spawn_scout_before_unlock(self):
        self.assertRaises(ValueError, self.bar.spawnUnit, 1)

    def test_barracks_unlock_scout(self):
        self.bar.unlockUnit(1)
        self.assertListEqual(self.bar.currentUnits, [Solider, Scout])

    def test_barracks_unlockUnit_too_high(self):
        self.assertRaises(ValueError, self.bar.unlockUnit, 2)

    def test_barracks_unlockUnit_negative(self):
        self.assertRaises(ValueError, self.bar.unlockUnit, -1)

    def test_barracks_spawn_scout(self):
        self.bar.unlockUnit(1)
        s = self.bar.spawnUnit(1)
        self.assertIsInstance(s, Scout)


if __name__ == '__main__':
    unittest.main()
