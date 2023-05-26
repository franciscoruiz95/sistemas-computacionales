# Python snake game implementation

This is a simple, but yet, good looking python implementation of the classic
snake game, made by me, as a python practice/learning project.

Made with tkinter (with practice/learning purpose also). The game was build from what at the begining were, moving rectangles that simulated the snake. Food and poison were a mere circle in a random position.

At the begining I used tkinter capability of tracking and finding overlapping objects to check for collisions, but this approch made the game feel wierd, so much in fact, that some times the snake would eat the apple without fully overlapping it. I realized that using tkinter for this purpose was not good at all, the reason being that overlapping is detected by tkinter when objects share even one pixel.

So, after finding out this problem I took a different aproach. After researching for a little bit, a found that I could implement a "board" where the snake, food and poison could be set.

this aproach proved to be a good one. I implemented a 'board' class which simulates all valid positions in the game, where the snake can move, and the apple and poison can be set without ever colliding with the moving snake. This board class made collision detection way better and afterwards, the snake could eat the apple in a perfect way.

The next major problem was working with the images and making the game animated, which took me a little bit to figure out, because tkinter is not really made for making a game, but that didn't stoped me from trying.

I found a lot of free stuff on the internet, such images, sounds etc. Everything in this game was made with free resouces that thanksfully are found out there for anyone to use. As you will see the snake art is specially good.

The snake art designer is Anya Biryukova, checkout her page. She's got great art work at http://www.biryuk.com/

The game at this point is up and running. Overall is being a great practice tool, I recommend you to try it out.