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

from const import TIME, Direction

import random

import numpy as np

from agent import QLearning


class SnakeApp(tk.Frame):

    def __init__(self, skin: str, size: tuple, episodes: int, master=None):
        super(SnakeApp, self).__init__(master)
        self.snake = Snake(self, skin, size)
        self.hud = Hud(self)
        self.agent = QLearning(
            18*18, 4, 0.7, 0.5, 0.1, 18*40, 18*40, 40)
        self.episodes = episodes
        self.score = 0
        self.initialize()
        self.snake.board.create_states()
        self.grid_all()

    def initialize(self):
        """ Initializes the HUD and the snake game graphically,
            to be put together in this class and show all in one frame
        """
        self.master.title('Epsilon Voráz')
        self.master.geometry('+350+50')
        self.master.resizable(0, 0)
        self['width'] = 800
        self['height'] = 592
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
        self.observation = None
        # self.bind('<space>', self.reset)
        # self.bind('<q>', self.quit_game)

    def grid_all(self):
        """ Show everything on the this frame using the grid method """
        self.hud.grid(row=0, column=0, sticky='nswe')
        self.snake.grid(row=1, column=0)
        self.snake.focus_set()
        self.grid()

    def update_hud(self):
        """ Updates the HUD with new score """
        self.score = self.snake.get_score()
        self.hud.set_score(self.score)
        self.hud.start_timer()

    def train(self):
        self.observation = self.get_state()

        action = self.agent.get_action(
            self.snake.get_snake(), self.snake.get_food(), 'epsilon-greedy')
        new_observation, reward, terminated, truncated, _ = self.apply_action(
            action)
        self.agent.update(self.snake.get_reason(), self.score)
        self.observation = new_observation

    def play(self):
        self.observation = self.get_state()

        action = self.agent.get_action(
            self.snake.get_snake(), self.snake.get_food(), 'greedy')
        new_observation, reward, terminated, truncated, _ = self.apply_action(
            action)
        self.agent.update(self.snake.get_reason(), self.score)
        self.observation = new_observation

    def apply_action(self, action):
        """ Returns a state given an action"""
        self.snake.event_generate(f'<KeyPress-{Direction.actions[action]}>')
        # self.snake.check_collision()
        return self.snake.get_state(), self.snake.get_reward(), self.snake.game_over(), False, {}

    def generate_random_action(self):
        keystroke = random.choice(['Up', 'Down', 'Right', 'Left'])
        self.snake.event_generate(f'<KeyPress-{keystroke}>')

    def run(self):
        """ Game main loop """
        if not self.snake.game_over():
            self.train()
            self.snake.move_snake()
            self.snake.snake_animation()
            self.snake.check_collision()
            self.update_hud()
            self.after(4, self.run)
        else:
            self.focus_set()
            self.reset()

    def run_play(self):
        """ Game main loop """
        if not self.snake.game_over():
            self.play()
            self.snake.move_snake()
            self.snake.snake_animation()
            self.snake.check_collision()
            self.update_hud()
            self.after(TIME, self.run_play)
        else:
            self.focus_set()
            self.reset_play()

    def reset(self):
        """ Resets the hole game after a game over """
        if self.hud.get_lives() > 0:
            state = self.snake.reset()
            self.hud.update_lives()
            self.hud.reset_timer()
            self.hud.reset_score()
            self.run()
            self.snake.focus_set()
            return state
        else:
            self.agent.graph()
            print('Graphics')
            self.hud.set_lives(10)
            self.run_play()
            # self.master.destroy()

    def reset_play(self):
        """ Resets the hole game after a game over """
        if self.hud.get_lives() > 0:
            state = self.snake.reset()
            self.hud.update_lives()
            self.hud.reset_timer()
            self.hud.reset_score()
            self.run_play()
            self.snake.focus_set()
            return state
        else:
            self.quit_game()

    def quit_game(self):
        """ Quits the game after pressing the 'q' key """
        self.master.destroy()

    def game_over(self):
        """ Returns game status """
        return self.snake.game_over()

    def get_state(self):
        return self.snake.get_state()


if __name__ == '__main__':
    root = tk.Tk()

    skins = ['../resources/img/snakes/blue',
             '../resources/img/snakes/coral',
             '../resources/img/snakes/green',
             '../resources/img/snakes/orange',
             '../resources/img/snakes/purple',
             '../resources/img/snakes/yellow']

    app = SnakeApp('../resources/img/skin/blue', (18, 18), 1000, root)
    app.run()
    app.mainloop()
