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

import tkinter as tk

from PIL import ImageTk

from PIL import Image

import os

from board import Board

from const import TileType, Direction, TIME


class Config:
    def __init__(self, skin: str, size: tuple):
        """ Initialize some common config variables """
        self.rows = size[0]
        self.cols = size[1]
        self.block = 40
        self.width = self.cols * self.block + self.block * 2
        self.height = self.rows * self.block + self.block * 2
        self.skin_path = skin


class Snake(tk.Canvas):

    def __init__(self, master, skin: str, size: tuple):
        """ This constructor initializes the game with the skin
            and map size selected by the user. Also initializes
            a Board obj wich holds all posible positions on the
            game.
        """
        self.config = Config(skin, size)
        super(Snake, self).__init__(master,
                                    width=self.config.width,
                                    height=self.config.height,
                                    bd=0,
                                    bg='#46C87B',
                                    highlightthickness=0)

        self.board = Board(self.config.width, self.config.height,
                           self.config.block)
        self.snake = []
        self.snake_x = 0
        self.snake_y = Direction.SPEED
        self.lastKey = 'Down'
        self._game_over = False
        self.score = 0
        self.bind('<Up>', self.get_key)
        self.bind('<Down>', self.get_key)
        self.bind('<Left>', self.get_key)
        self.bind('<Right>', self.get_key)

    def load_images(self):
        """ Here all source images used in the game are loaded from disk """
        self.bg = ImageTk.PhotoImage(
            Image.open('../resources/img/environment/bg.png'))
        self.apple = ImageTk.PhotoImage(
            Image.open('../resources/img/environment/apple.png'))
        self.posion = ImageTk.PhotoImage(
            Image.open('../resources/img/environment/poison.png'))
        self.block = ImageTk.PhotoImage(
            Image.open('../resources/img/environment/crate_box-min.png'))

        self.skin = {}
        for file in os.scandir(self.config.skin_path):
            if file.name.endswith('.png'):
                key = file.name.replace('.png', '')
                self.skin[key] = ImageTk.PhotoImage(Image.open(file.path))

    def set_background(self):
        """ Here background is put in the screen """
        self.create_image((self.config.width) / 2, (self.config.height) / 2,
                          image=self.bg, anchor='center')

    def set_blocks(self):
        """ This function takes care of creating the surrounding blocks """

        # Local constants used to build the blocks
        half_block = self.config.block // 2
        three_halves_block = (self.config.block * 3) // 2
        height_limit = self.config.height - 20
        width_limit = self.config.width - 20

        # Print boundary rows
        for i in range(half_block, self.config.width, self.config.block):
            self.create_image(i, half_block, image=self.block,
                              anchor='center', tag='wall')
            self.board.set_cell_type((i, half_block), TileType.WALL)

            self.create_image(i, height_limit, image=self.block,
                              anchor='center', tag='wall')
            self.board.set_cell_type((i, height_limit), TileType.WALL)

        # Print boundary columns
        for j in range(three_halves_block,
                       self.config.height - self.config.block,
                       self.config.block):
            self.create_image(half_block, j, image=self.block,
                              anchor='center', tag='wall')
            self.board.set_cell_type((half_block, j), TileType.WALL)
            self.create_image(width_limit, j, image=self.block,
                              anchor='center', tag='wall')
            self.board.set_cell_type((width_limit, j), TileType.WALL)

    def set_snake(self):
        """ This function creates and sets the snake on the board """
        x = 60
        y = 140
        head = self.create_image(x, y, image=self.skin['Down'], anchor='center')
        self.snake.append(head)
        for i in range(1, 2):
            body = self.create_image(x,
                                     y - i * self.config.block,
                                     image=self.skin['B001'],
                                     anchor='center')
            self.snake.append(body)
        tail = self.create_image(x,
                                 y - 80,
                                 image=self.skin['T003'],
                                 anchor='center')
        self.snake.append(tail)

    def set_apple(self):
        """ Here the board supplies a valid position for a new apple
            on the board, then creates the apple
        """
        pos = self.board.apple_cell()
        self.create_image(pos[0], pos[1], image=self.apple,
                          anchor='center', tag='apple')

    def set_poison(self):
        """ Here the board supplies a valid position for a new posion
            on the board, the creates the poison
        """
        pos = self.board.poison_cell()
        self.create_image(pos[0], pos[1], image=self.posion,
                          anchor='center', tag='poison')

    def add_tail(self):
        """ This function takes care of adding a new tail every time the
            snakes eats an apple
        """
        tail = self.coords(self.snake[-1])
        last = self.coords(self.snake[-2])
        next_ = self.coords(self.snake[-3])

        if last[0] - next_[0] > 0 or last[0] - next_[0] < 0:
            new = self.create_image(tail[0], tail[1], image=self.skin['B000'])
        else:
            new = self.create_image(tail[0], tail[1], image=self.skin['B001'])
        self.snake.append(new)
        self.snake[-1], self.snake[-2] = self.snake[-2], self.snake[-1]

    def get_key(self, event):
        """ This function makes the snake move in the direction selected by
            the player
        """
        _direction = Direction.dic[event.keysym]
        if _direction[1] + self.snake_y != 0:
            self.snake_x, self.snake_y = _direction
        if _direction[0] + self.snake_x != 0:
            self.snake_x, self.snake_y = _direction
        self.lastKey = event.keysym

    def move_snake(self):
        """ This function moves the images that form the snake, from tail to
            head, giving it the motion animation
        """
        # Make canvas coords and move methods local
        coords = self.coords
        move = self.move

        n = len(self.snake)
        tail = coords(self.snake[-1])
        self.board.set_cell_type((tail[0], tail[1]), TileType.EMPTY)

        for i in range(1, n):
            last = coords(self.snake[n - i])
            next_ = coords(self.snake[n - i - 1])
            move(self.snake[n - i], next_[0] - last[0], next_[1] - last[1])
        move(self.snake[0], self.snake_x, self.snake_y)

        # Make board.set_cell_type local
        set_cell_type = self.board.set_cell_type

        for _id in range(1, len(self.snake)):
            coord = coords(self.snake[_id])
            set_cell_type((coord[0], coord[1]), TileType.SNAKE)

    def snake_animation(self):
        """ This function animates the entire snake while it's moving """

        # Make canvas coords and itemconfigure methods local
        coords = self.coords
        itemconfigure = self.itemconfigure
        tail = self.coords(self.snake[-1])
        n = len(self.snake)

        # Tail animation
        if coords(self.snake[-2])[1] - tail[1] > 0:
            itemconfigure(self.snake[-1], image=self.skin['T003'])
        elif coords(self.snake[-2])[1] - tail[1] < 0:
            itemconfigure(self.snake[-1], image=self.skin['T001'])
        elif coords(self.snake[-2])[0] - tail[0] > 0:
            itemconfigure(self.snake[-1], image=self.skin['T000'])
        else:
            itemconfigure(self.snake[-1], image=self.skin['T002'])

        # Body animation
        for i in range(1, n - 1):
            last = coords(self.snake[n - i])
            mid = coords(self.snake[n - i - 1])
            next_ = coords(self.snake[n - i - 2])
            # Moving down, then right
            if mid[1] - last[1] > 0 and next_[0] - mid[0] > 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR005'])
            # Moving down, then left
            elif mid[1] - last[1] > 0 and next_[0] - mid[0] < 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR004'])
            # Moving up, then right
            elif mid[1] - last[1] < 0 and next_[0] - mid[0] > 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR006'])
            # Moving up, then left
            elif mid[1] - last[1] < 0 and next_[0] - mid[0] < 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR007'])
            # Moving right, then down
            elif mid[0] - last[0] > 0 and next_[1] - mid[1] > 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR007'])
            # Moving right, then up
            elif mid[0] - last[0] > 0 and next_[1] - mid[1] < 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR004'])
            # Moving left, then down
            elif mid[0] - last[0] < 0 and next_[1] - mid[1] > 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR006'])
            # Moving left, then up
            elif mid[0] - last[0] < 0 and next_[1] - mid[1] < 0:
                itemconfigure(self.snake[n - i - 1], image=self.skin['TR005'])
            # Moving vertically
            elif last[0] == mid[0] == next_[0]:
                itemconfigure(self.snake[n - i - 1], image=self.skin['B001'])
            # Moving horizontally
            else:
                itemconfigure(self.snake[n - i - 1], image=self.skin['B000'])
        # Head animation
        itemconfigure(self.snake[0], image=self.skin[self.lastKey])

    def check_collision(self):
        """ This function takes care of checking all possible collisions """

        head = tuple(self.coords(self.snake[0]))
        col_type = self.board.find_collision(head)

        if col_type == TileType.APPLE:
            self.score += 1
            self.delete('apple')
            self.add_tail()
            self.set_apple()
        elif col_type == TileType.POISON:
            self.delete('poison')
            self._game_over = True
        elif (col_type == TileType.WALL) or (col_type == TileType.SNAKE):
            self._game_over = True
        else:
            pass

    def game_over(self):
        """ Returns current game status """
        return self._game_over

    def get_score(self):
        """ Returns current score """
        return self.score

    def build(self):
        """ This function is used to reset the game after a game over """
        self.set_snake()
        self.set_blocks()
        self.set_apple()
        self.set_poison()

    def reset(self):
        """ Resets the game to it's starting state after a game over """
        # Delete snake
        for i in self.snake:
            self.delete(i)
        # Delete and reset other variables
        self.delete('apple')
        self.delete('poison')
        self.snake.clear()
        self.board.clear_board()
        self.lastKey = 'Down'
        self.snake_x, self.snake_y = Direction.dic[self.lastKey]
        self.delete('wall')
        self.build()
        self.score = 0
        self._game_over = False
