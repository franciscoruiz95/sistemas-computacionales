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

from snake import Snake

from hud import Hud

from const import TIME

import random

import string


class Application(tk.Frame):

    def __init__(self, master, skin: str, size: tuple):
        super(Application, self).__init__(master)
        self.snake = Snake(self, skin, size)
        self.hud = Hud(self)

    def initialize(self):
        """ Initializes the HUD and the snake game graphically,
            to be put together in this class and show all in one frame
        """
        # Load hud
        self.hud.load_images()
        self.hud.set_score_label()
        self.hud.set_timer_label()
        self.hud.set_lives_labels()
        # Load core game
        self.snake.load_images()
        self.snake.set_background()
        self.snake.set_snake()
        self.snake.set_blocks()
        self.snake.set_apple()
        self.snake.set_poison()
        self.bind('<space>', self.reset)
        self.bind('<q>', self.quit_game)

    def grid_all(self):
        """ Show everything on the this frame using the grid method """
        self.hud.grid(row=0, column=0, sticky='nswe')
        self.snake.grid(row=1, column=0)
        self.snake.focus_set()
        self.grid()

    def update_hud(self):
        """ Updates the HUD with new score """
        score = self.snake.get_score()
        self.hud.set_score(score)
        self.hud.start_timer()

    def generate_random_keystroke(self):
        keystroke = random.choice(['Up', 'Down', 'Right', 'Left'])
        self.snake.event_generate(f'<KeyPress-{keystroke}>')

    def run(self):
        """ Game main loop """
        if not self.snake.game_over():
            self.generate_random_keystroke()
            self.snake.move_snake()
            self.snake.snake_animation()
            self.snake.check_collision()
            self.update_hud()
            self.after(TIME, self.run)
        else:
            self.focus_set()

    def reset(self, event):
        """ Resets the hole game after a game over """
        if self.hud.get_lives() > 0:
            self.snake.reset()
            self.hud.update_lives()
            self.hud.reset_timer()
            self.hud.reset_score()
            self.run()
            self.snake.focus_set()
        else:
            self.master.master.destroy()

    def quit_game(self, event):
        """ Quits the game after pressing the 'q' key """
        self.master.master.destroy()

    def game_over(self):
        """ Returns game status """
        return self.snake.game_over()
