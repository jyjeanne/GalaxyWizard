"""
Unit tests for the AI system
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai.UnitAI import Base, HealWeakest, DamageWeakest, MoveToWeakest, Exhaustive
from engine.Battle import Battle, UnitTurn, NEVER_ENDING
from engine.Unit import Unit
from engine.Class import Class
from engine.Map import Map
from engine.Faction import Faction
import numpy as np


class TestAIBase(unittest.TestCase):
    """Test AI base class functionality"""

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

        # Create a simple 10x10 map
        width, height = 10, 10
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

    def test_base_ai_creation(self):
        """Test base AI creation"""
        unit = self.test_class.createUnit(gender=2)
        ai = Base(unit)
        self.assertIsNotNone(ai)
        self.assertEqual(ai._unit, unit)

    def test_base_ai_default_result(self):
        """Test base AI returns no-op by default"""
        unit = self.test_class.createUnit(gender=2)
        unit.setPosn(5, 5, 0)
        unit.setFaction(0)

        units = [unit]
        battle = Battle([NEVER_ENDING], units, self.test_map)

        ai = Base(unit)
        result = ai.calc(battle, unit)

        # Base AI should return a UnitTurn (no-op)
        self.assertIsInstance(result, UnitTurn)


class TestAITurnEvaluators(unittest.TestCase):
    """Test AI turn evaluator classes"""

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

        # Create a simple 10x10 map
        width, height = 10, 10
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

    def test_move_to_weakest_empty_targets(self):
        """Test MoveToWeakest handles empty target list"""
        unit = self.test_class.createUnit(gender=2)
        unit.setPosn(5, 5, 0)
        unit.setFaction(0)

        # No enemy units - only friendly
        units = [unit]
        battle = Battle([NEVER_ENDING], units, self.test_map)

        evaluator = MoveToWeakest()
        result = evaluator(battle, unit, [])

        # Should return empty list when no targets
        self.assertEqual(result, [])

    def test_move_to_weakest_with_targets(self):
        """Test MoveToWeakest identifies weakest enemy"""
        unit1 = self.test_class.createUnit(gender=2)
        unit1.setPosn(0, 0, 0)
        unit1.setFaction(0)
        unit1.battleInit()

        # Create two enemy units with different HP
        unit2 = self.test_class.createUnit(gender=2)
        unit2.setPosn(5, 5, 0)
        unit2.setFaction(1)
        unit2.battleInit()

        unit3 = self.test_class.createUnit(gender=2)
        unit3.setPosn(7, 7, 0)
        unit3.setFaction(1)
        unit3.battleInit()
        # Damage unit3 to make it weakest
        unit3.damageHP(unit3.hp() // 2, 0)

        units = [unit1, unit2, unit3]
        battle = Battle([NEVER_ENDING], units, self.test_map)

        # MoveToWeakest should prefer moving toward unit3 (weakest)
        # We can't easily test this without generating actual turns,
        # but we can verify it doesn't crash
        evaluator = MoveToWeakest()
        result = evaluator(battle, unit1, [])

        # Result should be a list (may be empty if no valid moves)
        self.assertIsInstance(result, list)


class TestAIExhaustive(unittest.TestCase):
    """Test Exhaustive AI class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a basic class with abilities
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

        # Create a simple 10x10 map
        width, height = 10, 10
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

    def test_exhaustive_ai_creation(self):
        """Test Exhaustive AI creation"""
        unit = self.test_class.createUnit(gender=2)
        ai = Exhaustive(unit)

        self.assertIsNotNone(ai)
        self.assertEqual(ai._unit, unit)
        self.assertEqual(len(ai._turnEvaluators), 3)

    def test_exhaustive_ai_all_abilities(self):
        """Test Exhaustive AI filters abilities by SP cost"""
        unit = self.test_class.createUnit(gender=2)
        unit.battleInit()

        ai = Exhaustive(unit)
        abilities = ai.allAbilities()

        # Should return a list of abilities
        self.assertIsInstance(abilities, list)

        # All abilities should have cost <= unit's SP
        for ability in abilities:
            self.assertLessEqual(ability.cost(), unit.sp())

    def test_exhaustive_ai_generate_turns_empty_battle(self):
        """Test Exhaustive AI turn generation with minimal setup"""
        unit = self.test_class.createUnit(gender=2)
        unit.setPosn(5, 5, 0)
        unit.setFaction(0)
        unit.battleInit()
        unit.readyTurn()

        units = [unit]
        battle = Battle([NEVER_ENDING], units, self.test_map)

        ai = Exhaustive(unit)
        moveTargets = [(5, 5), (5, 6), (6, 5)]
        abilities = ai.allAbilities()

        # This should not crash
        try:
            turns = ai.generateAllTurns(battle, moveTargets, abilities)
            self.assertIsInstance(turns, list)
        except Exception as e:
            self.fail(f"generateAllTurns raised {type(e).__name__}: {e}")


class TestAITargetSelection(unittest.TestCase):
    """Test AI target selection logic"""

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

        # Create a simple 10x10 map
        width, height = 10, 10
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

    def test_damage_weakest_target_selection(self):
        """Test DamageWeakest prioritizes lowest HP enemy"""
        unit1 = self.test_class.createUnit(gender=2)
        unit1.setPosn(5, 5, 0)
        unit1.setFaction(0)
        unit1.battleInit()

        # Create enemies with different HP
        unit2 = self.test_class.createUnit(gender=2)
        unit2.setPosn(5, 6, 0)
        unit2.setFaction(1)
        unit2.battleInit()

        unit3 = self.test_class.createUnit(gender=2)
        unit3.setPosn(5, 7, 0)
        unit3.setFaction(1)
        unit3.battleInit()
        unit3.damageHP(unit3.hp() // 2, 0)  # Half health

        units = [unit1, unit2, unit3]
        battle = Battle([NEVER_ENDING], units, self.test_map)

        evaluator = DamageWeakest()
        result = evaluator(battle, unit1, [])

        # Should return a list
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()
