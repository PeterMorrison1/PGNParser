# PGNParser

This library is a parser created for PGN (.pgn). 

PGN files are also known as 'Portable Game Notation' which is a format used to store chess games.
The .pgn stores information about one or more games, including the event name, the player names, player ELO, and more,
including the moves each player made in each turn.
 
I created the PGNParser to read .pgn files from the Lichess database (https://database.lichess.org/).
Because this is my goal, the current version of the parser is only tested on files from this database.

An example of using the parser is:

```python
from pgn_parser import PGNParser

parser = PGNParser.Parser('my_chess_games.pgn')
games = parser.parse_pgn() # games will be a list of PGN objects
for game in games:
    game.print_pgn()
```

