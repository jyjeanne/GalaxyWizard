"""
Unit tests for the Unit class
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine.Unit import Unit
from engine.Class import Class
from engine.Effect import Status


class TestUnit(unittest.TestCase):
    """Test Unit class functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a basic class for testing
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

    def test_unit_creation(self):
        """Test basic unit creation"""
        unit = self.test_class.createUnit(gender=2)  # MALE

        self.assertIsNotNone(unit.name())
        self.assertGreater(unit.mhp(), 0)
        unit.battleInit()
        self.assertEqual(unit.hp(), unit.mhp())
        self.assertTrue(unit.alive())

    def test_unit_damage(self):
        """Test unit taking damage"""
        unit = self.test_class.createUnit(gender=2)
        unit.battleInit()
        initial_hp = unit.hp()

        # Deal 30 damage
        unit.damageHP(30, 0)
        self.assertEqual(unit.hp(), initial_hp - 30)
        self.assertTrue(unit.alive())

        # Deal lethal damage
        unit.damageHP(1000, 0)
        self.assertEqual(unit.hp(), 0)
        self.assertFalse(unit.alive())

    def test_unit_healing(self):
        """Test unit healing"""
        unit = self.test_class.createUnit(gender=2)
        unit.battleInit()
        max_hp = unit.mhp()

        # Take damage
        unit.damageHP(30, 0)
        damaged_hp = unit.hp()
        self.assertEqual(damaged_hp, max_hp - 30)

        # Heal (negative damage)
        unit.damageHP(-20, 2)  # HEALING type
        self.assertEqual(unit.hp(), damaged_hp + 20)

        # Can't heal above max
        unit.damageHP(-1000, 2)
        self.assertEqual(unit.hp(), max_hp)

    def test_unit_turn_state(self):
        """Test unit turn state management"""
        unit = self.test_class.createUnit(gender=2)

        # Initially has no move/act
        self.assertFalse(unit.hasMove())
        self.assertFalse(unit.hasAct())

        # Ready for turn
        unit.readyTurn()
        self.assertTrue(unit.hasMove())
        self.assertTrue(unit.hasAct())
        self.assertFalse(unit.hasCancel())

        # Use move (set move=False, act=True)
        unit.setMoveActCancel(False, True, False)
        self.assertFalse(unit.hasMove())
        self.assertTrue(unit.hasAct())

        # Cancel turn
        unit.canceled()
        self.assertFalse(unit.hasMove())
        self.assertFalse(unit.hasAct())
        self.assertTrue(unit.hasCancel())

    def test_unit_status_effects(self):
        """Test status effect application"""
        unit = self.test_class.createUnit(gender=2)

        # Add status effect
        unit.addStatusEffect(Status.HASTE, duration=1, power=1.5)
        effects = unit.statusEffects()
        self.assertTrue(effects.has(Status.HASTE))

        # Check duration
        self.assertEqual(effects.duration(Status.HASTE), 1)

        # Check power
        self.assertEqual(effects.power(Status.HASTE), 1.5)

    def test_unit_abilities(self):
        """Test unit ability management"""
        unit = self.test_class.createUnit(gender=2)

        # Unit should have attack ability
        abilities = unit.allAbilities()
        self.assertIsInstance(abilities, list)
        self.assertGreater(len(abilities), 0)

    def test_unit_position(self):
        """Test unit position management"""
        unit = self.test_class.createUnit(gender=2)

        unit.setPosn(5, 7, 2)
        self.assertEqual(unit.x(), 5)
        self.assertEqual(unit.y(), 7)
        self.assertEqual(unit.z(), 2)
        self.assertEqual(unit.posn(), (5, 7))
        self.assertEqual(unit.posn3d(), (5, 7, 2))


if __name__ == '__main__':
    unittest.main()
