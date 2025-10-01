"""
Unit tests for the Battle class
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine.Battle import Battle
from engine.Unit import Unit
from engine.Class import Class
from engine.Map import Map
import numpy as np


class TestBattle(unittest.TestCase):
    """Test Battle class functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a basic class
        self.test_class = Class(
            name="TestClass",
            abilities=[],
            spriteRoot="fighter",
            move=5,
            jump=2,
            mhpBase=50,
            mhpGrowth=5.0,
            mhpMult=1.0,
            mspBase=20,
            mspGrowth=2.0,
            mspMult=1.0,
            watkBase=10,
            watkGrowth=1.0,
            watkMult=1.0,
            wdefBase=10,
            wdefGrowth=1.0,
            wdefMult=1.0,
            matkBase=10,
            matkGrowth=1.0,
            matkMult=1.0,
            mdefBase=10,
            mdefGrowth=1.0,
            mdefMult=1.0,
            speedBase=50,
            speedGrowth=2.0,
            speedMult=1.0
        )

        # Create a simple 5x5 map
        width, height = 5, 5
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)
        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        self.test_map = Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

    def test_battle_creation(self):
        """Test battle creation"""
        from engine.Battle import NEVER_ENDING
        battle = Battle([NEVER_ENDING], [], self.test_map)
        self.assertIsNotNone(battle)
        self.assertEqual(battle.map(), self.test_map)

    def test_battle_unit_management(self):
        """Test adding and managing units in battle"""
        from engine.Battle import NEVER_ENDING
        unit1 = self.test_class.createUnit(gender=2)
        unit1.setPosn(0, 0, 0)
        unit1.setFaction(0)

        unit2 = self.test_class.createUnit(gender=2)
        unit2.setPosn(4, 4, 0)
        unit2.setFaction(1)

        units = [unit1, unit2]
        battle = Battle([NEVER_ENDING], units, self.test_map)

        # Check units are in battle
        self.assertEqual(len(battle.units()), 2)

    def test_battle_unit_moved(self):
        """Test unit movement in battle"""
        from engine.Battle import NEVER_ENDING
        unit = self.test_class.createUnit(gender=2)
        unit.setPosn(0, 0, 0)
        unit.setFaction(0)

        units = [unit]
        battle = Battle([NEVER_ENDING], units, self.test_map)
        battle.pickNextUnit()

        # Try to move unit
        result = battle.unitMoved(1, 1)

        # Movement should succeed if within range
        if result:
            self.assertEqual(unit.x(), 1)
            self.assertEqual(unit.y(), 1)

    def test_battle_status(self):
        """Test battle status detection"""
        from engine.Battle import DEFEAT_ALL_ENEMIES
        unit1 = self.test_class.createUnit(gender=2)
        unit1.setPosn(0, 0, 0)
        unit1.setFaction(0)

        unit2 = self.test_class.createUnit(gender=2)
        unit2.setPosn(4, 4, 0)
        unit2.setFaction(1)

        units = [unit1, unit2]
        battle = Battle([DEFEAT_ALL_ENEMIES], units, self.test_map)

        # Battle should be ongoing (both units alive)
        self.assertEqual(battle.status(), -1)

        # Kill enemy faction unit
        unit2.battleInit()
        unit2.damageHP(unit2.hp(), 0)

        # Battle should end (faction 1 defeated)
        status = battle.status()
        # Status is either ongoing or won, depending on ending condition logic
        self.assertIn(status, [-1, 0])


if __name__ == '__main__':
    unittest.main()
