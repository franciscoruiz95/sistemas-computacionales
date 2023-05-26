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

from .const import TIME


class Hud(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super(Hud, self).__init__(master, *args, **kwargs)

        # Change frame background
        self['bg'] = 'black'
        # Set all extra space to cloumns number 0 and 1
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)
        # Timer variable
        self.timer = tk.StringVar()
        self.timer.set('00:00')
        self.start_time = 0
        # Score
        self.score = tk.StringVar()
        self.score.set('SCORE: 0')
        # Lives
        self.lives = 3
        self.life_lost = None
        self.lives_label = None

    def load_images(self):
        """ Loads images used for the HUD from disk """
        self.heart = ImageTk.PhotoImage(
            Image.open('./resources/img/hud/heart.png'))
        self.life_lost = ImageTk.PhotoImage(
            Image.open('./resources/img/hud/life_lost.png'))

    def set_score_label(self):
        """ Creates the score label on the top left corner """
        self.score_label = tk.Label(self,
                                    textvariable=self.score,
                                    width=8,
                                    font=('Kenney Mini Square', 15),
                                    foreground='#FF6200',
                                    background='black',
                                    anchor='w')
        self.score_label.grid(row=0, column=0, sticky='nswe')

    def set_lives_labels(self):
        """ Creates 3 hearts on the right top corner, representing lives left
        """
        self.lives_label = [tk.Label(self, image=self.heart,
                                     anchor='center', background='black')
                            for i in range(3)]
        for i in range(3):
            self.lives_label[i].grid(row=0, column=i + 2)

    def set_timer_label(self):
        """ Sets a simple timer in the top center of the screen """
        self.time = tk.Label(self,
                             textvariable=self.timer,
                             width=8,
                             font=('Kenney Mini Square', 16),
                             foreground='#FF6200',
                             background='black')
        self.time.grid(row=0, column=1, sticky='w')

    def start_timer(self):
        """ Initializes the timer when the game starts """
        time = divmod(int(self.start_time), 60)
        self.timer.set('{:02}:{:02}'.format(*time))
        self.start_time += TIME / 1000

    def update_lives(self):
        """ Removes a heart from the right top corner, every time
            a life is lost
        """
        if (self.lives_label):
            self.lives_label[self.lives - 1]['image'] = self.life_lost
            self.lives -= 1

    def set_score(self, score):
        """ Sets the score text on the left top corner """
        self.score.set(f'SCORE: {score}')

    def reset_score(self):
        self.score.set('SCORE: 0')

    def reset_timer(self):
        self.timer.set('00:00')
        self.start_time = 0

    def reset_lives(self):
        self.lives = 3
        for i in range(3):
            self.lives_label[i]['image'] = self.heart

    def get_lives(self):
        return self.lives
