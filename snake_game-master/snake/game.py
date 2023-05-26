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

from snake_app import Application


class Game(tk.Frame):

    def __init__(self, master=None):
        super(Game, self).__init__(master)
        self.master.title('TkSnake')
        self.master.geometry('+350+50')
        self.master.resizable(0, 0)
        self['width'] = 800
        self['height'] = 592
        self.show_intro()

    def show_intro(self):
        """ This function will show an intro window before the game
            can be started
        """

        # Get main window width and height
        w = self['width']
        h = self['height']

        # Load intro main image
        self.intro = ImageTk.PhotoImage(Image.open('../resources/intro.png'))

        # This canvas holds all the images
        canvas = tk.Canvas(self, width=w, bd=0,
                           height=h - 30, bg='black',
                           highlightthickness=0)

        # Intro image
        canvas.create_image(w / 2, h / 2, image=self.intro, anchor='center')

        # Indicator label
        text = tk.Label(self, text="Press 's' to start", anchor='center',
                        font=('Kenney Mini Square', 15), background='white',
                        foreground='#F40909')

        # Key 's' binded to be used as starter
        self.bind('<s>', self.settings)

        # self.intro_frame.bind('<q>',self.quit_game)
        # Set focus to intro_frame so 's' can be used
        self.focus_set()

        # Grid everything
        canvas.grid(row=0, column=0)
        text.grid(row=1, column=0, sticky='nswe')
        self.grid()

    def settings(self, event):
        """ This function will show a simple menu where the player can
            select a skin to play with, and a board size
        """
        # Bind next window
        self.bind('<s>', self.build_game)

        # Delete intro
        for widget in self.winfo_children():
            widget.destroy()

        # This canvas holds the full menu
        canvas = tk.Canvas(self, width=self['width'], height=self['height'],
                           bg='blue', bd=0, highlightthickness=0)

        # A frame to help putting all in order
        frame = tk.Frame(self, bg='black')

        # Skin checkbutton variable
        self.skin_value = tk.IntVar()

        # Game size checkbutton variable
        self.size_value = tk.IntVar()

        ######################################################################
        """
        Load skins images
        """
        self.blue = ImageTk.PhotoImage(
            Image.open('../resources/img/snakes/blue.png'))
        self.coral = ImageTk.PhotoImage(
            Image.open('../resources/img/snakes/coral.png'))
        self.green = ImageTk.PhotoImage(
            Image.open('../resources/img/snakes/green.png'))
        self.orange = ImageTk.PhotoImage(
            Image.open('../resources/img/snakes/orange.png'))
        self.purple = ImageTk.PhotoImage(
            Image.open('../resources/img/snakes/purple.png'))
        self.yellow = ImageTk.PhotoImage(
            Image.open('../resources/img/snakes/yellow.png'))
        """
        """
        ######################################################################
        """
        Menu text labels
        """
        menu = tk.Label(frame, text='Menu', anchor='center',
                        font=('Kenney Mini Square', 15),
                        foreground='#F40909', bg='black')
        skin = tk.Label(frame, text='Skin', font=('Kenney Mini Square', 15),
                        foreground='#F40909', bg='black', anchor='center')
        size = tk.Label(frame, text='size', anchor='center',
                        font=('Kenney Mini Square', 15),
                        foreground='#F40909', bg='black')
        """
        """
        ######################################################################
        """
        Game size check buttons
        """
        sizes = ['12x14', '14x16', '16x18', '14x14', '16x16', '18x18']
        size_button_ls = [tk.Checkbutton(frame, text=sizes[i], anchor='center',
                                         font=('Kenney Mini Square', 15),
                                         foreground='#F40909', bg='black',
                                         indicatoron=0, bd=0,
                                         highlightthickness=0,
                                         variable=self.size_value,
                                         onvalue=i + 1)
                          for i in range(len(sizes))]
        """
        """
        ######################################################################
        """
        Skins check buttons
        """
        color = [
            self.blue, self.coral, self.green,
            self.orange, self.purple, self.yellow
        ]
        skin_button_ls = [tk.Checkbutton(frame, image=color[i],
                                         indicatoron=0,
                                         variable=self.skin_value,
                                         onvalue=i + 1, bg='black',
                                         bd=0, highlightthickness=0)
                          for i in range(6)]
        """
        """
        ######################################################################
        """
        Grid all
        """
        menu.grid(row=0, column=0, columnspan=2, sticky='nswe')
        skin.grid(row=1, column=0, sticky='nswe', padx=60)
        size.grid(row=1, column=1, sticky='nswe', padx=60)
        for i in range(len(size_button_ls)):
            size_button_ls[i].grid(row=i + 2, column=1)
        for i in range(len(skin_button_ls)):
            skin_button_ls[i].grid(row=i + 2, column=0, ipadx=10, pady=15)
        canvas.create_window(400, 280, window=frame)
        canvas.grid()
        self.grid()
        """
        """
        ######################################################################

    def build_game(self, event):
        """ This function grabs the selected settings and saves them
            to be used in the initialization of the game
        """

        # Delete settings window
        for widget in self.winfo_children():
            widget.destroy()

        skin_dir = {
            1: '../resources/img/skin/blue',
            2: '../resources/img/skin/coral',
            3: '../resources/img/skin/green',
            4: '../resources/img/skin/orange',
            5: '../resources/img/skin/purple',
            6: '../resources/img/skin/yellow'
        }

        size_dic = {
            1: (12, 14), 2: (14, 16), 3: (16, 18),
            4: (14, 14), 5: (16, 16), 6: (18, 18)
        }
        try:
            self.skin = skin_dir[self.skin_value.get()]
            self.size = size_dic[self.size_value.get()]
        except:
            self.skin = skin_dir[1]
            self.size = size_dic[3]
        self.game_loop()

    def game_loop(self):
        """ Initializes and run the game with the selected settings """
        self.app = Application(self, self.skin, self.size)
        self.app.initialize()
        self.app.grid_all()
        self.app.run()


if __name__ == '__main__':
    root = tk.Tk()
    app = Game(root)
    app.mainloop()
