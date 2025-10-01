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

import fsm
import unittest

class FSMTest(unittest.TestCase):

    def testNormalLoop(self):
        # Example of what a standard FSM loop might look like:
        state_machine = fsm.FSM(['state1', 'state2', 'state3'])
        try:
            state_machine.startLoop()
            while state_machine.running:
                if state_machine.state == 'state1':
                    state_machine.trans('state2')
                    continue
                elif state_machine.state == 'state2':
                    state_machine.trans('state3')
                    continue
                elif state_machine.state == 'state3':
                    state_machine.endLoop()
        except fsm.FSMError as error:
            print('FSM Error:', str(error))
            state_machine.endLoop()
        
        # This is unit-testing code and wouldn't appear here for a
        # normal FSM loop.
        self.failIf(state_machine.running)

    def testLoopDetection(self):
        state_machine = fsm.FSM(['state1', 'state2'])
        state_machine.startLoop()
        state_machine.trans('state2')
        state_machine.trans('state1')
        self.assertRaises(fsm.FSMError, state_machine.trans, 'state2')

