#    <one line to give the program's name and a brief idea of what it does.>
#    Copyright (C) <2020>  <Jose Briceño>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from random import choice

from const import TileType


class Board:
    def __init__(self, width, height, units=40):
        """ Initializes the variables needed to make a board """
        self.width = width
        self.height = height
        self.units = units
        self.tiles = {}
        self.make_board()

    def make_board(self):
        """ Calculates and saves all valid positions into a dictionary """
        for row in range(self.units // 2, self.width, self.units):
            for col in range(self.units // 2, self.height, self.units):
                self.tiles[(row, col)] = TileType.EMPTY

    def set_cell_type(self, cell: tuple, cell_type: int = 0):
        """ Simple function to set a cell as filled by some type of object """
        self.tiles[cell] = cell_type

    def find_collision(self, head: tuple) -> int:
        """ Returns the head's current position for collision checking """
        return self.tiles[head]

    def _find_free_cell(self) -> tuple:
        """ This functions finds and returns a valid position on the board
            to set a new object. Meant to be used by Board class only
        """
        cell = choice(list(self.tiles.keys()))
        while self.tiles[cell] != 0:
            cell = choice(list(self.tiles.keys()))
        return cell

    def apple_cell(self) -> tuple:
        """ Finds and returns a valid position for a new apple """
        apple = self._find_free_cell()
        assert self.tiles[apple] == TileType.EMPTY
        self.tiles[apple] = TileType.APPLE
        return apple

    def poison_cell(self) -> tuple:
        """ Finds and returns a valid position for a new poison """
        poison = self._find_free_cell()
        assert self.tiles[poison] == TileType.EMPTY
        self.tiles[poison] = TileType.POISON
        return poison

    def clear_board(self):
        """ Sets all positions to empty except for the walls positions, when
            the game needs to be reset after a game over
        """
        for key in self.tiles:
            if 1 <= self.tiles[key] <= 3:
                self.tiles[key] = 0
