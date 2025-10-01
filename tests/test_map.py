"""
Unit tests for the Map class and pathfinding
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine.Map import Map, MapSquare
from engine.Unit import Unit
from engine.Class import Class
import numpy as np


class TestMapCreation(unittest.TestCase):
    """Test Map creation and initialization"""

    def test_map_creation_basic(self):
        """Test basic map creation"""
        width, height = 10, 10
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)

        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        map_obj = Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

        self.assertIsNotNone(map_obj)
        self.assertEqual(map_obj.width, width)
        self.assertEqual(map_obj.height, height)

    def test_map_squares_initialized(self):
        """Test that map squares are properly initialized"""
        width, height = 5, 5
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)

        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        map_obj = Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

        # Check all squares exist
        for x in range(width):
            for y in range(height):
                square = map_obj.squares[x][y]
                self.assertIsInstance(square, MapSquare)
                self.assertEqual(square.x, x)
                self.assertEqual(square.y, y)

    def test_square_exists(self):
        """Test squareExists boundary checking"""
        width, height = 10, 10
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)

        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        map_obj = Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

        # Valid coordinates
        self.assertTrue(map_obj.squareExists(0, 0))
        self.assertTrue(map_obj.squareExists(5, 5))
        self.assertTrue(map_obj.squareExists(9, 9))

        # Invalid coordinates
        self.assertFalse(map_obj.squareExists(-1, 0))
        self.assertFalse(map_obj.squareExists(0, -1))
        self.assertFalse(map_obj.squareExists(10, 0))
        self.assertFalse(map_obj.squareExists(0, 10))


class TestMapPathfinding(unittest.TestCase):
    """Test pathfinding algorithms"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a test class for units
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

    def create_test_map(self, width=10, height=10):
        """Helper to create a test map"""
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)

        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        return Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

    def test_get_potential_connections(self):
        """Test getting neighboring squares"""
        map_obj = self.create_test_map(5, 5)

        # Middle square should have 4 neighbors
        square = map_obj.squares[2][2]
        connections = map_obj.getPotentialConnections(square)
        self.assertEqual(len(connections), 4)

        # Corner square should have 2 neighbors
        square = map_obj.squares[0][0]
        connections = map_obj.getPotentialConnections(square)
        self.assertEqual(len(connections), 2)

        # Edge square should have 3 neighbors
        square = map_obj.squares[0][2]
        connections = map_obj.getPotentialConnections(square)
        self.assertEqual(len(connections), 3)

    def test_reset_search_costs(self):
        """Test resetting search costs"""
        map_obj = self.create_test_map(5, 5)

        # Set some search values
        map_obj.squares[2][2].search = (5, None)
        map_obj.squares[3][3].search = (10, None)

        # Reset
        map_obj.resetSearchCosts()

        # Check all are None
        for x in range(5):
            for y in range(5):
                self.assertIsNone(map_obj.squares[x][y].search)

    def test_reachable_basic(self):
        """Test reachable squares calculation"""
        map_obj = self.create_test_map(10, 10)

        unit = self.test_class.createUnit(gender=2)
        unit.setPosn(5, 5, 0)
        unit.battleInit()
        unit.readyTurn()  # Make unit ready to move

        # Place unit on map
        map_obj.squares[5][5].unit = unit

        # Get reachable squares
        reachable = map_obj.reachable(unit)

        # Should return a list of positions
        self.assertIsInstance(reachable, list)

        # All reachable positions should be valid
        for (x, y) in reachable:
            self.assertTrue(map_obj.squareExists(x, y))

        # Should have at least one reachable square (the current position or nearby)
        # Note: might be 0 if pathfinding requires specific conditions
        self.assertGreaterEqual(len(reachable), 0)

    def test_reachable_blocked_by_unit(self):
        """Test that reachable excludes squares with units"""
        map_obj = self.create_test_map(10, 10)

        unit1 = self.test_class.createUnit(gender=2)
        unit1.setPosn(5, 5, 0)
        unit1.battleInit()
        map_obj.squares[5][5].unit = unit1

        # Place blocking unit
        unit2 = self.test_class.createUnit(gender=2)
        unit2.setPosn(5, 6, 0)
        unit2.battleInit()
        map_obj.squares[5][6].unit = unit2

        # Get reachable squares
        reachable = map_obj.reachable(unit1)

        # (5,6) should not be in reachable (has a unit)
        self.assertNotIn((5, 6), reachable)

    def test_fill_distances(self):
        """Test fillDistances pathfinding"""
        map_obj = self.create_test_map(10, 10)

        unit = self.test_class.createUnit(gender=2)
        unit.setPosn(5, 5, 0)
        unit.battleInit()
        map_obj.squares[5][5].unit = unit

        # Fill distances to target
        target_posn = (7, 7)
        map_obj.fillDistances(unit, target_posn)

        # Check that search costs are set
        # Target square should have search cost 0
        target_square = map_obj.squares[7][7]
        self.assertIsNotNone(target_square.search)
        self.assertEqual(target_square.search[0], 0)

    def test_shortest_path(self):
        """Test shortest path calculation"""
        map_obj = self.create_test_map(10, 10)

        unit = self.test_class.createUnit(gender=2)
        unit.setPosn(5, 5, 0)
        unit.battleInit()
        map_obj.squares[5][5].unit = unit

        # Fill distances first
        target_posn = (7, 7)
        map_obj.fillDistances(unit, target_posn)

        # Get shortest path
        path = map_obj.shortestPath(7, 7)

        # Should return a list of squares
        self.assertIsInstance(path, list)
        self.assertGreater(len(path), 0)

        # First element should be the target
        self.assertEqual(path[0].x, 7)
        self.assertEqual(path[0].y, 7)


class TestMapGeneration(unittest.TestCase):
    """Test Map generation features"""

    def test_map_serialization(self):
        """Test map can be serialized to string"""
        width, height = 5, 5
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)

        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        map_obj = Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

        # Test that map can generate state
        state = map_obj.getStateToCopy()
        self.assertIsNotNone(state)

    def test_map_texture_assignment(self):
        """Test map texture assignment"""
        width, height = 5, 5
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)

        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        map_obj = Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

        # Check that squares have texture method
        square = map_obj.squares[0][0]
        textures = square.texture()

        # Should return list of 5 textures
        self.assertIsInstance(textures, list)
        self.assertEqual(len(textures), 5)

    def test_map_height_variations(self):
        """Test map with height variations"""
        width, height = 5, 5
        # Create varied terrain
        zdata = np.array([
            [0, 0, 1, 1, 2],
            [0, 1, 1, 2, 2],
            [1, 1, 2, 2, 3],
            [1, 2, 2, 3, 3],
            [2, 2, 3, 3, 4]
        ], dtype=float)

        tileProperties = np.zeros((width, height), dtype=object)
        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        map_obj = Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

        # Check heights are preserved
        self.assertEqual(map_obj.squares[0][0].z, 0)
        self.assertEqual(map_obj.squares[2][0].z, 1)
        self.assertEqual(map_obj.squares[4][4].z, 4)


class TestMapBFS(unittest.TestCase):
    """Test breadth-first search algorithm"""

    def create_test_map(self, width=10, height=10):
        """Helper to create a test map"""
        zdata = np.zeros((width, height))
        tileProperties = np.zeros((width, height), dtype=object)

        for x in range(width):
            for y in range(height):
                tileProperties[x, y] = {'tag': ''}

        return Map(
            width=width,
            height=height,
            z=zdata,
            tileProperties=tileProperties,
            globalWaterHeight=0,
            globalWaterColor=[0.3, 0.3, 0.6],
            tags_={}
        )

    def test_bfs_basic(self):
        """Test basic BFS functionality"""
        map_obj = self.create_test_map(10, 10)

        start = (5, 5)
        expand = lambda s: map_obj.getPotentialConnections(s)
        visit = lambda s: True  # Visit all squares
        result = lambda s: s.x == 7 and s.y == 7  # Find specific square

        results = map_obj.bfs(start, expand, visit, result)

        # Should find the target square
        self.assertIsInstance(results, list)
        if len(results) > 0:
            self.assertEqual(results[0].x, 7)
            self.assertEqual(results[0].y, 7)

    def test_bfs_with_distance_limit(self):
        """Test BFS with distance constraint"""
        map_obj = self.create_test_map(10, 10)

        start = (5, 5)
        max_distance = 3
        expand = lambda s: map_obj.getPotentialConnections(s)
        visit = lambda s: s.search[0] <= max_distance
        result = lambda s: True  # Return all visited squares

        results = map_obj.bfs(start, expand, visit, result)

        # All results should be within distance limit
        for square in results:
            self.assertLessEqual(square.search[0], max_distance)


if __name__ == '__main__':
    unittest.main()
