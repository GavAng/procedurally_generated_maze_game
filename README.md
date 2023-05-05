# procedurally_generated_maze_game

Cave Crawler, a browser game that lets you play through 5 procedurally generated maze levels, before ending with the option to log
your name and time in a leaderboard.

This was created for my Advanced Higher Computing Science project, a subject which I ended up getting first prize in.


## Setup Instructions

1. Run the following installation command:
> pip install Flask

2. Run mazeServer.py and enter localhost port 8080 into your browser
3. Scroll down to play the game and view the leaderboard


## Game Instructions

You start in the top left corner of a darkened maze, and your goal is to reach a red exit point that will be situated at one of the other
maze corners. As you move, the lighting in the maze will change arround you.


## Reflections and Improvements

This project was made over a year and a half ago, and looking back there is a lot I would like to improve:

- Add test coverage
- Use NumPy as the program deals with a lot of lists
- Improve the wall generating part of the algorithm
- Improve code readability and comments

An improved version of the maze generating script, but not the game, is present in my 'procedurally_generated_game' repo.
