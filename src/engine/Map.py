## Automatically adapted for numpy.oldnumeric Jul 22, 2012 by 

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

import numpy as Numeric
import pickle as cPickle
import gzip
import re
import random
import logging
from engine import Faction
from OpenGL.GL import *
from twisted.spread import pb

logger = logging.getLogger('map')


# Helper functions for color/texture parsing
def parse_color_data(color_data, default_colors):
    """
    Parse color data from tag into 5-element list for (Top, Left, Back, Right, Front).

    Args:
        color_data: Color specification (tuple, list, or other)
        default_colors: Default 5-element list of colors

    Returns:
        List of 5 color tuples
    """
    if isinstance(color_data, tuple):
        # Old format: single tuple applies to all sides
        if len(color_data) == 3:
            return [color_data] * 5
        elif len(color_data) == 4:
            return [color_data] * 5

    elif isinstance(color_data, list):
        # New format: can specify different colors for each side
        if not color_data:
            return default_colors

        elem_len = len(color_data[0]) if hasattr(color_data[0], '__len__') else 0

        if elem_len in (3, 4):
            if len(color_data) == 1:
                # One color for all sides
                return [color_data[0]] * 5
            elif len(color_data) == 2:
                # Top uses first, others use second
                return [color_data[0]] + [color_data[1]] * 4
            elif len(color_data) == 5:
                # All 5 specified
                return color_data

    return default_colors

class MapSquare(pb.Copyable, pb.RemoteCopy):
    def __init__(self, x, y, zBase, cornerHeights, color, smooth,
                 tag, waterHeight, waterColor):
        # Find our z offset
        self.cornerHeights = cornerHeights
        self.x = x
        self.y = y
        self.z = zBase
        self.unit = None
        self.guiData = {}
#        self.texture = texture
        self.color = color
        self.cornerColors = [[color[0], color[0], color[0], color[0]],
                             [color[1], color[1], color[1], color[1]],
                             [color[2], color[2], color[2], color[2]],
                             [color[3], color[3], color[3], color[3]],
                             [color[4], color[4], color[4], color[4]]]
        self.smooth = smooth
        self.tag = tag
        self.waterHeight = waterHeight
        self.waterColor = waterColor
        self.smoothed = []
        self.search = None

    def minHeight(self):
        return min(self.z,
                   self.z + self.cornerHeights[0],
                   self.z + self.cornerHeights[1],
                   self.z + self.cornerHeights[2],
                   self.z + self.cornerHeights[3])

    def maxHeight(self):
        return max(self.z,
                   self.z + self.cornerHeights[0],
                   self.z + self.cornerHeights[1],
                   self.z + self.cornerHeights[2],
                   self.z + self.cornerHeights[3])

    def setUnit(self, u):
        if self.unit != None:
            raise Exception("Unit was moved into a map square that " + 
                            "already has a unit!")
        self.unit = u
        u.setPosn(self.x, self.y, self.z)

    def posn2d(self):
        return (self.x, self.y)

    def posn(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return "(%d,%d,%d)" % (self.x, self.y, self.z)
    
    # Added for GuiMapEditor
#    def texture(self):
#        return self.guiData['texture']
    
#    def color(self):
#        return self.guiData['color']
    
    def height(self):
        return self.z
   
    def texture(self):
        if 'texture' in self.tag:
            tex = self.tag['texture']
            if isinstance(tex, str):
                return [tex,tex,tex,tex,tex]
            elif isinstance(tex, list):
                if len(tex) == 1:
                    return [tex[0],tex[0],tex[0],tex[0],tex[0]]
                elif len(tex) == 2:
                    return [tex[0],tex[1],tex[1],tex[1],tex[1]]
                elif len(tex) == 5:
                    return [tex[0],tex[1],tex[2],tex[3],tex[4]]
                else:
                    # Default for unsupported list lengths
                    return ["none","none","none","none","none"]
            else:
                return ["none","none","none","none","none"]
        # Default when no texture in tag
        return ["none","none","none","none","none"]

#    def color(self):
#        return self.tag['color']
    
    def tagName(self):
        if 'texture' in self.tag:
            return self.tag['name']
        return ''


    # FIXME: do smoothing here so we don't have to
    #         smooth the entire map on edits
    def setTag(self,tag = None):
        """Set the tag and update colors with variance."""
        if tag == None:
            tag = self.tag
        else:
            self.tag = tag

        # Default colors (Top, Left, Back, Right, Front)
        default_colors = [(1.0, 1.0, 1.0, 1.0)] * 5
        default_variance = [(0.0, 0.0, 0.0, 0.0)] * 5

        # Parse colors and variance using helper function
        colors = parse_color_data(tag.get("color"), default_colors)
        variance = parse_color_data(tag.get("colorVar"), default_variance)

        # Apply variance to colors
        self.color = []
        for (color, var) in zip(colors, variance):
            # Extend to 4 components if needed
            if len(color) == 3:
                color = color + (1.0,)
            if len(var) == 3:
                var = var + (0.0,)

            # Apply random variance
            varied_color = tuple(
                color[i] - random.random() * var[i]
                for i in range(4)
            )
            self.color.append(varied_color)

        self.cornerColors = [[self.color[0], self.color[0], self.color[0], self.color[0]],
                             [self.color[1], self.color[1], self.color[1], self.color[1]],
                             [self.color[2], self.color[2], self.color[2], self.color[2]],
                             [self.color[3], self.color[3], self.color[3], self.color[3]],
                             [self.color[4], self.color[4], self.color[4], self.color[4]]]
        if 'waterColor' in tag:
            self.waterColor = tag['waterColor']
       
    def setTexture(self,texture):
        self.tag['texture'] = texture
            
    def setColor(self,color):
        self.tag['color'] = color
        
    def plusHeight(self,height=1):
        self.z += height
        for i in range(0,4):
            self.cornerHeights[i] -= height

    def minusHeight(self,height=1):
        self.z -= height
        for i in range(0,4):
            self.cornerHeights[i] += height
            
#    def setCornerHeight(self,corner,height):
#        self.cornerHeights[corner] = height
    # End added for GuiMapEditor
    
class Map(pb.Copyable, pb.RemoteCopy):
    def __init__(self, width, height, z, tileProperties,
                 globalWaterHeight, globalWaterColor, tags_):
        self._loadString = ""
        self.waterHeight = globalWaterHeight
        self.waterColor = globalWaterColor
        self.tags = tags_
        self.width = width
        self.height = height
        self.squares = []
        for x in range(0, width):
            self.squares.append([])
            for y in range(0, height):
                props = tileProperties[x,y]
                tag = {}
                if props['tag'] in tags_:
                    tag = tags_[props['tag']]

                #color list: Top, Left, Back, Right, Front.
                [(tr, tg, tb, ta),
                 (lr, lg, lb, la),
                 (br, bg, bb, ba),
                 (rr, rg, rb, ra),
                 (fr, fg, fb, fa)] = [(1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0)]
                #variance list: Top, Left, Back, Right, Front
                [(vtr, vtg, vtb, vta),
                 (vlr, vlg, vlb, vla),
                 (vbr, vbg, vbb, vba),
                 (vrr, vrg, vrb, vra),
                 (vfr, vfg, vfb, vfa)] = [(0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0)]

                texture = "none"
                if "color" in tag:
                    c = tag["color"]
                    if isinstance(c, tuple): #check for old format
                        if len(c) == 3:
                            [(tr, tg, tb),
                             (lr, lg, lb),
                             (br, bg, bb),
                             (rr, rg, rb),
                             (fr, fg, fb)] = [c,c,c,c,c]
                        elif len(c) == 4:
                            [(tr, tg, tb, ta),
                             (lr, lg, lb, la),
                             (br, bg, bb, ba),
                             (rr, rg, rb, ra),
                             (fr, fg, fb, fa)] = [c,c,c,c,c]

                    elif isinstance(c, list): #under the new format, Top, Left, Back, Right, Front.  
                        if len(c[0]) == 3:
                            if len(c) == 1:
                                [(tr, tg, tb),
                                 (lr, lg, lb),
                                 (br, bg, bb),
                                 (rr, rg, rb),
                                 (fr, fg, fb)] = [c[0],c[0],c[0],c[0],c[0]] #only one member makes all sides that color
                            if len(c) == 2:
                                [(tr, tg, tb),
                                 (lr, lg, lb),
                                 (br, bg, bb),
                                 (rr, rg, rb),
                                 (fr, fg, fb)] = [c[0],c[1],c[1],c[1],c[1]] #two members makes the top the first
                            if len(c) == 5:                                 #and the rest the second color
                                [(tr, tg, tb),
                                 (lr, lg, lb),
                                 (br, bg, bb),
                                 (rr, rg, rb),
                                 (fr, fg, fb)] = [c[0],c[1],c[2],c[3],c[4]] #the other option is to specify all 5.
                        elif len(c[0]) == 4:
                            if len(c) == 1:
                                [(tr, tg, tb, ta),
                                 (lr, lg, lb, la),
                                 (br, bg, bb, ba),
                                 (rr, rg, rb, ra),
                                 (fr, fg, fb, fa)] = [c[0],c[0],c[0],c[0],c[0]] #same as above
                            if len(c) == 2:
                                [(tr, tg, tb, ta),
                                 (lr, lg, lb, la),
                                 (br, bg, bb, ba),
                                 (rr, rg, rb, ra),
                                 (fr, fg, fb, fa)] = [c[0],c[1],c[1],c[1],c[1]]
                            if len(c) == 5:
                                [(tr, tg, tb, ta),
                                 (lr, lg, lb, la),
                                 (br, bg, bb, ba),
                                 (rr, rg, rb, ra),
                                 (fr, fg, fb, fa)] = [c[0],c[1],c[2],c[3],c[4]]
                                
                                
                    else:
                        pass  #log? raise exception?

                if "colorVar" in tag:
                    c = tag["colorVar"]
                    if isinstance(c, tuple): #check for old format
                        if len(c) == 3:
                            [(vtr, vtg, vtb),
                             (vlr, vlg, vlb),
                             (vbr, vbg, vbb),
                             (vrr, vrg, vrb),
                             (vfr, vfg, vfb)] = [c,c,c,c,c]
                        elif len(c) == 4:
                            [(vtr, vtg, vtb, vta),
                             (vlr, vlg, vlb, vla),
                             (vbr, vbg, vbb, vba),
                             (vrr, vrg, vrb, vra),
                             (vfr, vfg, vfb, vfa)] = [c,c,c,c,c]

                    elif isinstance(c, list): #under the new format, Top, Left, Back, Right, Front.  
                        if len(c[0]) == 3:
                            if len(c) == 1:
                                [(vtr, vtg, vtb),
                                 (vlr, vlg, vlb),
                                 (vbr, vbg, vbb),
                                 (vrr, vrg, vrb),
                                 (vfr, vfg, vfb)] = [c[0],c[0],c[0],c[0],c[0]] #only one member makes all sides that variance
                            if len(c) == 2:
                                [(vtr, vtg, vtb),
                                 (vlr, vlg, vlb),
                                 (vbr, vbg, vbb),
                                 (vrr, vrg, vrb),
                                 (vfr, vfg, vfb)] = [c[0],c[1],c[1],c[1],c[1]] #two members makes the top the first
                            if len(c) == 5:                                    #and the rest the second variance
                                [(vtr, vtg, vtb),
                                 (vlr, vlg, vlb),
                                 (vbr, vbg, vbb),
                                 (vrr, vrg, vrb),
                                 (vfr, vfg, vfb)] = [c[0],c[1],c[2],c[3],c[4]] #the other option is to specify all 5.
                        elif len(c[0]) == 4:
                            if len(c) == 1:
                                [(vtr, vtg, vtb, vta),
                                 (vlr, vlg, vlb, vla),
                                 (vbr, vbg, vbb, vba),
                                 (vrr, vrg, vrb, vra),
                                 (vfr, vfg, vfb, vfa)] = [c[0],c[0],c[0],c[0],c[0]] #same as above
                            if len(c) == 2:
                                [(vtr, vtg, vtb, vta),
                                 (vlr, vlg, vlb, vla),
                                 (vbr, vbg, vbb, vba),
                                 (vrr, vrg, vrb, vra),
                                 (vfr, vfg, vfb, vfa)] = [c[0],c[1],c[1],c[1],c[1]]
                            if len(c) == 5:
                                [(vtr, vtg, vtb, vta),
                                 (vlr, vlg, vlb, vla),
                                 (vbr, vbg, vbb, vba),
                                 (vrr, vrg, vrb, vra),
                                 (vfr, vfg, vfb, vfa)] = [c[0],c[1],c[2],c[3],c[4]]
                                
                                
                    else:
                        pass  #log? raise exception?
                    
                if "texture" in tag:
                    texture = tag["texture"]
                waterHeight = globalWaterHeight
                waterColor = globalWaterColor
                if 'waterHeight' in props:
                    waterHeight = props['waterHeight']
                elif 'waterHeight' in tag:
                    waterHeight = tag['waterHeight']
                if 'waterColor' in tag:
                    waterColor = tag['waterColor']
                smooth = False
                if "smooth" in tag:
                    smooth = tag["smooth"]
                smoothed = False
                if "cornerHeights" in props:
                    cornerHeights = list(props["cornerHeights"])
                    smooth = False
                elif "cornerHeights" in tag:
                    cornerHeights = list(tag["cornerHeights"])
                else:
                    cornerHeights = [0,0,0,0]
                    if smooth and y-1 >= 0:
                        up = self.squares[x][y-1]
                        if up.smooth:
                            smoothed = True
                            cornerHeights[0] = up.z+up.cornerHeights[2]-z[x,y]
                            cornerHeights[1] = up.z+up.cornerHeights[3]-z[x,y]
                    if smooth and x-1 >= 0:
                        left = self.squares[x-1][y]
                        if left.smooth:
                            cornerHeights[2] = left.z+left.cornerHeights[3]-z[x,y]
                            if not smoothed:
                                cornerHeights[0] = left.z+left.cornerHeights[1]-z[x,y]
                            smoothed = True
#                     for i in range(4):
#                        if cornerHeights[i] < -8 or cornerHeights[i] > 8:
#                            cornerHeights[i] = 0 # make a step


                c = [(tr - random.random() * vtr,tg - random.random() * vtg,tb - random.random() * vtb,ta - random.random() * vta),
                     (lr - random.random() * vlr,lg - random.random() * vlg,lb - random.random() * vlb,la - random.random() * vla),
                     (br - random.random() * vbr,bg - random.random() * vbg,bb - random.random() * vbb,ba - random.random() * vba),
                     (rr - random.random() * vrr,rg - random.random() * vrg,rb - random.random() * vrb,ra - random.random() * vra),
                     (fr - random.random() * vfr,fg - random.random() * vfg,fb - random.random() * vfb,fa - random.random() * vfa)]
                self.squares[x].append(MapSquare(x, y, z[x,y],
                                                 cornerHeights,
                                                 c,
                                                 smooth, tag,
                                                 waterHeight,
                                                 waterColor))
                
        # Normalize z-heights of smoothed squares a bit, so that the
        # middle of the square is has a z-height in the middle of the
        # corner heights.
        for x in range(0, width):
            for y in range(0, height):
                sq = self.squares[x][y]
                if not sq.smooth:
                    continue
                ch = list(sq.cornerHeights)
                ch.sort()
                zDiff = (ch[0] + ch[1] + ch[2] + ch[3] + 3) / 4
                sq.z += zDiff
                for i in range(0, 4):
                    sq.cornerHeights[i] -= zDiff

        self.smoothColors()
                    
        # If a square doesn't have a water height, but one of its
        # neighbors does, and this square was smoothed, inherit the
        # water height of its neighbor.
        for x in range(0, width):
            for y in range(0, height):
                sq = self.squares[x][y]
                if sq.waterHeight != 0: # or not sq.smoothed:
                    continue
                highestWater = 0
                waterColor = None
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.waterHeight > highestWater:
                        waterColor = up.waterColor
                        highestWater = up.waterHeight
                if y+1 < self.height:
                    down = self.squares[x][y+1]
                    if down.waterHeight > highestWater:
                        waterColor = down.waterColor
                        highestWater = down.waterHeight
                if x-1 >= 0:
                    left = self.squares[x-1][y]
                    if left.waterHeight > highestWater:
                        waterColor = left.waterColor
                        highestWater = left.waterHeight
                if x+1 < self.width:
                    right = self.squares[x+1][y]
                    if right.waterHeight > highestWater:
                        waterColor = right.waterColor
                        highestWater = right.waterHeight
                if highestWater > 0 and sq.minHeight() < highestWater:
                    sq.waterHeight = highestWater
                    sq.waterColor = waterColor

    def smoothColors(self):
        # Smooth colors between squares with the same tag. The idea is
        # to make the colorVar smooth instead of on a per-square basis.
        for x in range(0, self.width):
            for y in range(0, self.height):
                sq = self.squares[x][y]
                #smooth topsides
                smoothedUp = False 
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.tag == sq.tag:
                        smoothedUp = True
                        sq.cornerColors[0][0] = up.cornerColors[0][2]
                        sq.cornerColors[0][1] = up.cornerColors[0][3]
                if x-1 >= 0:
                    left = self.squares[x-1][y]
                    if left.tag == sq.tag:
                        sq.cornerColors[0][2] = left.cornerColors[0][3]
                        if not smoothedUp:
                            sq.cornerColors[0][0] = left.cornerColors[0][1]
                #smooth leftsides
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.tag == sq.tag:
                        sq.cornerColors[1][0] = up.cornerColors[1][1]
                        sq.cornerColors[1][3] = up.cornerColors[1][2]
                #smooth backsides
                if x-1 >= 0:
                    up = self.squares[x-1][y]
                    if up.tag == sq.tag:
                        sq.cornerColors[2][1] = up.cornerColors[2][0]
                        sq.cornerColors[2][2] = up.cornerColors[2][3]
                #smooth rightsides
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.tag == sq.tag:
                        sq.cornerColors[3][1] = up.cornerColors[3][0]
                        sq.cornerColors[3][2] = up.cornerColors[3][3]
                #smooth backsides
                if x-1 >= 0:
                    up = self.squares[x-1][y]
                    if up.tag == sq.tag:
                        sq.cornerColors[4][0] = up.cornerColors[4][1]
                        sq.cornerColors[4][3] = up.cornerColors[4][2]
        
    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.loadString())

    def getStateToCopy(self):
        return self.loadString()

    def setCopyableState(self, state):
        m = MapIO.loadString("remote map", state)
        self.__dict__.update(m.__dict__)
        
    def setLoadString(self, text):
        self._loadString = text
        
    def loadString(self):
        r = ("VERSION = 1\n\n"
            +"WIDTH = %s\n" % self.width
            +"HEIGHT = %s\n\n" % self.height
            +"WATER_HEIGHT = %d\n" % self.waterHeight
            +"WATER_COLOR = %s\n\n" % repr(self.waterColor)
            +"TILE_PROPERTIES = {\n")
        for tagName in self.tags.keys():
            tag = self.tags[tagName]
            r += "    '%s':\t{\n" % tagName
            for k,v in tag.items():
                if k != "name":
                    r += "\t\t    '%s': %s,\n" % (k, repr(v))
            r = r[:-2] + "\n    },\n"
        r += "}\n\nLAYOUT = '''\n"
        for y in range(0, self.height):
            for x in range(0, self.width):
                sq = self.squares[x][y]
                s = "%d" % sq.height()
                if ((('cornerHeights' not in sq.tag) and
                     sq.cornerHeights != [0, 0, 0, 0]) or
                    ('cornerHeights' in sq.tag and
                     sq.cornerHeights != sq.tag['cornerHeights'])):
                    s += repr(sq.cornerHeights)
                if (('waterHeight' not in sq.tag) or
                    sq.waterHeight != sq.tag['waterHeight']):
                    s += "wh" + repr(sq.waterHeight)
                s += sq.tagName()
                r += "%-30s" % s
            r += "\n"
        r += "'''\n"
        return r        

    def squareExists(self, x, y):
        return (x >= 0 and y >= 0 and x < self.width and y < self.height)

    def resetSearchCosts(self):
        sq = self.squares
        for x in range(0, self.width):
            for y in range(0, self.height):
                sq[x][y].search = None

    def getPotentialConnections(self, square):
        result = []
        (x, y) = (square.x, square.y)
        if x > 0:
            result.append(self.squares[x-1][y])
        if x < self.width - 1:
            result.append(self.squares[x+1][y])
        if y > 0:
            result.append(self.squares[x][y-1])
        if y < self.height - 1:
            result.append(self.squares[x][y+1])
        return result

    def bfs(self, start, expand, visitPredicate, resultPredicate):
        startX = start[0]
        startY = start[1]
        self.resetSearchCosts()
        sq = self.squares
        result = []
        q = [sq[startX][startY]]
        q[0].search = (0, None)
        while len(q) > 0:
            s = q.pop(0)
            if resultPredicate(s):
                result.append(s)
            for newS in expand(s):
                if newS.search == None:
                    newS.search = (s.search[0] + 1, s)
                    if visitPredicate(newS):
                        q.append(newS)
                    else:
                        newS.search = None
        return result

    # FIXME: don't use faction() directly?
    # FIXME: this should be in the AI code, not here
    def closestUnits(self, unit, faction):
        def visit(s):
            connectedOK = (s.search[1] == None or
                           connected(s.search[1], s, unit))
            return connectedOK
        def resultp(s):
            for neighbor in self.getPotentialConnections(s):
                if (neighbor.unit != None and
                    neighbor.unit.faction() == faction and
                    neighbor.unit.alive()):
                    return True
            return False
        start = (unit.x(), unit.y())
        expand = lambda s: self.getPotentialConnections(s)
        result = self.bfs(start, expand, visit, resultp)
        return result
    
    def reachable(self, unit):
        def visit(s):
            costOK = s.search[0] <= unit.move()
            connectedOK = (s.search[1] == None or
                           connected(s.search[1], s, unit))
            return costOK and connectedOK
        start = (unit.x(), unit.y())
        resultp = lambda s: s.unit == None
        expand = lambda s: self.getPotentialConnections(s)
        result = self.bfs(start, expand, visit, resultp)
        return [(s.x, s.y) for s in result]

    def fillDistances(self, unit, posn):
        def visit(s):
            connectedOK = (s.search[1] == None or
                           connectedIgnoringUnits(s.search[1], s, unit))
            return connectedOK
        start = posn
        resultp = lambda s: s.unit == None
        expand = lambda s: self.getPotentialConnections(s)
        self.bfs(start, expand, visit, resultp)

    def shortestPath(self, targetX, targetY):
        sq = self.squares
        result = [sq[targetX][targetY]]
        while result[-1].search[0] != 0:
            (cost, prev) = result[-1].search
            result.append(prev)
        return result

    def changeCorner(self, x, y, corner, change):
        sq = self.squares[x][y]
        getDiag = False
        
        if 'smooth' in sq.tag and sq.tag['smooth'] == True:
            # find the corner's neighbors: (x,y),(x,y+dy),(x+dx,y),(x+dx,y+dy)
            dx = 1
            dy = 1
            if corner < 2:
                dy = -1
            if corner % 2 == 0:
                dx = -1
                    
            # move them along with us if they match up (same tag, height)
            if self.squareExists(x,y+dy):
                nb = self.squares[x][y+dy]
                if (nb.tag == sq.tag and
                    nb.cornerHeights[corner-2*dy] + nb.height() ==
                    sq.cornerHeights[corner] + sq.height()):
                    getDiag = True
                    nb.cornerHeights[corner-2*dy] += change
            if self.squareExists(x+dx,y):
                nb = self.squares[x+dx][y]
                if (nb.tag == sq.tag and
                    nb.cornerHeights[corner-dx] + nb.height() ==
                    sq.cornerHeights[corner] + sq.height()):
                    getDiag = True
                    nb.cornerHeights[corner-dx] += change
            if getDiag == True and self.squareExists(x+dx,y+dy):
                nb = self.squares[x+dx][y+dy]
                if (nb.tag == sq.tag and
                    nb.cornerHeights[3-corner] + nb.height() ==
                    sq.cornerHeights[corner] + sq.height()):
                    nb.cornerHeights[3-corner] += change
        sq.cornerHeights[corner] += change

    def index(self, x, y):
        return y * self.width + x

    def __repr__(self):
        result = ''
        sq = self.squares
        for y in range(0, self.height):
            for x in range(0, self.width):
                result = result + '%s ' % sq[x][y].z
            result = result + '\n'
        return result
   
class MapIO(object):

    def load(mapname):
        with open(mapname, 'r') as mapfile:
            text = mapfile.read()
        return MapIO.loadString(mapname, text)
    
    def loadString(mapname, text):
        """Load map data from string using safe literal evaluation.

        Uses ast.literal_eval for safety instead of eval() to prevent
        arbitrary code execution. Only Python literals are allowed.
        """
        import ast

        # Parse the map file safely
        mapData = {}
        try:
            # Split into assignment statements
            lines = text.split('\n')
            current_var = None
            current_value = []
            in_multiline = False

            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Handle multiline strings (''')
                if "'''" in line:
                    if not in_multiline:
                        # Start of multiline string
                        var_name = line.split('=')[0].strip()
                        in_multiline = True
                        current_var = var_name
                        current_value = []
                        # Check if it ends on same line
                        if line.count("'''") == 2:
                            # Single line triple-quoted string
                            content = line.split("'''")[1]
                            mapData[var_name] = content
                            in_multiline = False
                            current_var = None
                    else:
                        # End of multiline string
                        mapData[current_var] = '\n'.join(current_value)
                        in_multiline = False
                        current_var = None
                        current_value = []
                    continue

                if in_multiline:
                    current_value.append(line)
                    continue

                # Regular assignment
                if '=' in line and not in_multiline:
                    var_name, value = line.split('=', 1)
                    var_name = var_name.strip()
                    value = value.strip()

                    # Use ast.literal_eval for safe evaluation of Python literals
                    try:
                        mapData[var_name] = ast.literal_eval(value)
                    except (ValueError, SyntaxError) as e:
                        raise ValueError(f"Invalid map data for {var_name}: {e}")

        except Exception:
            # Fallback to old method for backward compatibility
            # This is expected for map files with Python code (variable definitions)
            logger.debug(f"Map '{mapname}' uses Python code, parsing with eval()")
            try:
                compiled = compile(text, mapname, 'exec')
                localVars = {}
                eval(compiled, {}, localVars)
                mapData = localVars
            except Exception as eval_error:
                raise ValueError(f"Map parsing failed: {eval_error}")

        if mapData["VERSION"] != 1:
            raise ValueError(f"Map version {mapData['VERSION']} not supported")
        width = mapData['WIDTH']
        height = mapData['HEIGHT']
#        tilePropertiesTemplate = {}
        waterHeight = 0
        waterColor = [0.3, 0.3, 0.6]
        if 'WATER_HEIGHT' in mapData:
            waterHeight = mapData['WATER_HEIGHT']
        if 'WATER_COLOR' in mapData:
            waterColor = mapData['WATER_COLOR']
        if 'TILE_PROPERTIES' in mapData:
            tags = mapData['TILE_PROPERTIES']
            for k in tags.keys():
                tags[k]['name'] = k
                if 'waterColor' not in tags[k]:
                    tags[k]['waterColor'] = waterColor
                if 'waterHeight' not in tags[k]:
                    tags[k]['waterHeight'] = waterHeight
        else:
            tags = {}
        layoutLines = mapData['LAYOUT'].split('\n')
        layoutLines.pop(0)
        zdata = Numeric.zeros((width, height))
        tileProperties = Numeric.zeros((width, height), dtype=object)
        y = 0
        padded_lines = 0  # Track irregular map shape
        for line in layoutLines:
            if re.match(re.compile(r'^\s*$'), line):
                continue
            # Split on multiple spaces (2+) to handle padded tiles
            # The layout uses %-30s formatting which creates spaces between tiles
            tiles = re.split(r'\s{2,}', line.strip())
            # Filter out empty strings from the split
            tiles = [t for t in tiles if t.strip()]

            # If we have fewer tiles than expected, pad with defaults
            # This is expected for triangular or irregular-shaped maps
            if len(tiles) < width:
                padded_lines += 1
                # Pad with default tile data
                tiles.extend(['0'] * (width - len(tiles)))

            for x in range(0, width):
                tileData = tiles[x] if x < len(tiles) else '0'
                tileProperties[x,y] = {}
                # Updated regex to handle floats in corner heights (including negative)
                m = re.match(re.compile(
                    r'(\d+)(\[(-?[\d.]+),\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(-?[\d.]+)\])?(wh(\d+))?(\w*)'), tileData)
                if m is None:
                    raise ValueError(f"Invalid tile data at position ({x},{y}): '{tileData}'")
                zdata[x,y] = int(m.group(1))
                tileProperties[x,y]['tag'] = m.group(9) if m.group(9) else ''
                if m.group(2) != None:
                    tileProperties[x,y]['cornerHeights'] = [int(float(m.group(3))),int(float(m.group(4))),int(float(m.group(5))),int(float(m.group(6)))]
                if m.group(7) != None:
                    tileProperties[x,y]['waterHeight'] = int(m.group(8))
            y += 1

        # Log map shape summary if irregular
        if padded_lines > 0:
            logger.debug(f"Loaded irregular map: {mapname} ({width}x{height}, {padded_lines} padded rows)")

        m = Map(width, height, zdata, tileProperties, waterHeight, waterColor, tags)
        m.setLoadString(text)
        return m

    load = staticmethod(load)
    loadString = staticmethod(loadString)

def connectedIgnoringUnits(sq1, sq2, unit):
    return connected(sq1, sq2, unit, True)

def connected(sq1, sq2, unit, ignoreUnits=False):
    if not ignoreUnits:
        if (sq2.unit != None and
            sq2.unit.alive() and
            not Faction.friendly(unit.faction(), sq2.unit.faction())):
            return False
    if sq1 is sq2:
        return False
    if sq1.z == 0 or sq2.z == 0:
        return False
    if sq1.z + 4 < sq1.waterHeight or sq2.z + 4 < sq2.waterHeight:
        return False
#    if sq1.maxHeight() - sq1.minHeight() > 16:
#        return False
#    if sq2.maxHeight() - sq2.minHeight() > 16:
#        return False
    result = abs(sq1.z - sq2.z) <= unit.jump()
    return result

