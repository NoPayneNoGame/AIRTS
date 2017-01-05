from game.object import Object, Vec2
from game.unit import Unit, Worker, Solider, Scout
from game.building import Building, Base, Barracks
from game.player import Player
from game.resource import Resource, GoldResource

import unittest
import uuid

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
        self.player = Player()
        self.base = Base(Vec2(10, 10), self.player)
    
    def test_base_player(self):
        self.assertIs(self.base.player, self.player)

    def test_base_position_10_10(self):
        self.assertEqual(self.base.position, Vec2(10, 10))

    def test_base_player_default_none(self):
        #base = Base()
        #self.assertIsNone(base.player)
        self.assertRaises(ValueError, Base)

    def test_base_position_default_0_0(self):
        base = Base(player=self.player)
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
        for _ in range(4):
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

    def test_base_spawn_worker_correct_player(self):
        w = self.base.spawnUnit(0)
        self.assertIs(w.player, self.player)


class BarracksTest(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.bar = Barracks(player=self.player)

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


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.gameUUID = uuid.uuid1()
        self.player = Player("Steven", self.gameUUID, "red")

    def test_player_spawnBuilding_base(self):
        base = self.player.spawnBuilding(0, Vec2(23, 12))
        self.assertIsInstance(base, Base)

    def test_player_spawnBuilding_id_too_high(self):
        self.assertRaises(ValueError, self.player.spawnBuilding, 2, Vec2(23, 12))

    def test_player_spawnBuilding_id_negative(self):
        self.assertRaises(ValueError, self.player.spawnBuilding, -1, Vec2(23, 12))

    def test_player_spawnBuilding_barracks_before_unlock(self):
        self.assertRaises(ValueError, self.player.spawnBuilding, 1, Vec2(23, 12))

    def test_player_unlock_barracks(self):
        self.player.unlockBuilding(1)
        self.assertListEqual(self.player.currentBuildings, [Base, Barracks])

    def test_player_unlockBuilding_too_high(self):
        self.assertRaises(ValueError, self.player.unlockBuilding, 2)

    def test_player_unlockBuilding_negative(self):
        self.assertRaises(ValueError, self.player.unlockBuilding, -1)

class WorkerTest(unittest.TestCase):
    def setUp(self):
        self.gold = GoldResource(100, Vec2(5,5))
        self.player = Player()
        self.worker = Worker(Vec2(4, 4), self.player)

    def test_worker_harvest_gold_once(self):
        self.worker.harvest(self.gold)
        self.assertEqual(self.gold.amount, 90)
        self.assertEqual(self.worker.carrying, {"gold": 10 })

    def test_worker_harvest_gold_multiple(self):
        for _ in range(4):
            self.worker.harvest(self.gold)
        self.assertEqual(self.gold.amount, 60)
        self.assertEqual(self.worker.carrying, {"gold": 40 })

    def test_worker_harvest_gold_and_drop_off_with_no_buildings(self):
        for _ in range(4):
            self.worker.harvest(self.gold)
        self.assertRaises(ValueError, self.worker.harvest, self.gold)

    def test_worker_harvest_gold_and_drop_off(self):
        base = Base(player=self.player)
        for _ in range(7):
            self.worker.harvest(self.gold)
        self.assertEqual(self.gold.amount, 30)
        self.assertEqual(self.worker.carrying, {"gold": 20 })
        self.assertEqual(self.player.resources, {"gold": 50 })

    def test_worker_harvest_non_resource(self):
        self.assertRaises(TypeError, self.worker.harvest, 20)
       
    

if __name__ == '__main__':
    unittest.main()
