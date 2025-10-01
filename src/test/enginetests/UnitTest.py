# Copyright (C) 2005 Jeremy Jeanne <jyjeanne@gmail.com>
#
# This file is part of GalaxyWizard.
#
# GalaxyWizard is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# GalaxyWizard is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GalaxyWizard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import unittest
import resources as Resources
from engine import Unit
import constants as Constants

class UnitCreationTestCase(unittest.TestCase):
    def testUnitCreation(self):
        '''Test creating a basic unit'''
        unit = Unit.Unit(Unit.MALE)
        self.assertIsNotNone(unit)
        self.assertIsNotNone(unit.unitID)

    def testUnitGender(self):
        '''Test unit gender functions'''
        self.assertEqual(Unit.genderAsString(Unit.NEUTER), "neuter")
        self.assertEqual(Unit.genderAsString(Unit.FEMALE), "female")
        self.assertEqual(Unit.genderAsString(Unit.MALE), "male")

    def testUnitPosition(self):
        '''Test unit positioning'''
        unit = Unit.Unit(Unit.FEMALE)
        unit.setPosn(5, 10)
        self.assertEqual(unit.x(), 5)
        self.assertEqual(unit.y(), 10)

