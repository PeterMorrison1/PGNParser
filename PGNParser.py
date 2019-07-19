"""
Parses .pgn files and creates PGN objects for each game in the .pgn file.
The end result is a list of PGN objects, so the .pgn file can have multiple games.

To run the parser, instantiate a new Parser with the .pgn file, then run parse_pgn.
Example:
    parser = Parser.PGNParser('my_chess_games.pgn')
    games = parser.parse_pgn() # games will be a list of PGN objects
    for game in games:
        game.print_pgn()

If the moves in the game contain comments or other values that aren't '{ [%eval 0.13] } 1...' (as this
is already handled since this is made for the Lichess database), then extra regex strings can be passed
through the parse_pgn() function.
"""
import re


class PGN(object):
    """
    Stores a game stored in a pgn file, which are the tags found in [square brackets] in the .pgn file.
    Also stores the move list found in the .pgn file.
    """

    TAGS = ['Event', 'Site', 'White', 'Black', 'Result', 'Annotator', 'PlyCount', 'Date',
            'UTCDate', 'UTCTime', 'WhiteElo', 'BlackElo', 'WhiteRatingDiff',
            'BlackRatingDiff', 'ECO', 'Opening', 'TimeControl', 'Time', 'Termination']

    def __init__(self, Event=None, Site=None, White=None, Black=None, Result=None,
                 Annotator=None, PlyCount=None, Date=None, UTCDate=None, UTCTime=None,
                 WhiteElo=None, BlackElo=None, WhiteRatingDiff=None,
                 BlackRatingDiff=None, ECO=None, Opening=None, TimeControl=None,
                 Time=None, Termination=None, moves=None):
        self.Event = Event
        self.Site = Site
        self.White = White
        self.Black = Black
        self.Result = Result
        self.Annotator = Annotator
        self.PlyCount = PlyCount
        self.Date = Date
        self.UTCDate = UTCDate
        self.UTCTime = UTCTime
        self.WhiteElo = WhiteElo
        self.BlackElo = BlackElo
        self.WhiteRatingDiff = WhiteRatingDiff
        self.BlackRatingDiff = BlackRatingDiff
        self.ECO = ECO
        self.Opening = Opening
        self.TimeControl = TimeControl
        self.Time = Time
        self.Termination = Termination
        self.moves = moves if moves is not None else []

    def print_pgn(self):
        """
        Prints all of the attribute values for the object.
        """
        print(self.Event, self.Site, self.White, self.Black, self.Result,
              self.Annotator, self.PlyCount, self.Date, self.UTCDate, self.UTCTime,
              self.WhiteElo, self.BlackElo, self.WhiteRatingDiff,
              self.BlackRatingDiff, self.ECO, self.Opening, self.TimeControl,
              self.Time, self.Termination, self.moves)

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14} {15} {16} {17} ' \
               '{18} {19}'.format(self.Event, self.Site, self.White, self.Black, self.Result,
                                       self.Annotator, self.PlyCount, self.Date, self.UTCDate,
                                       self.UTCTime, self.WhiteElo, self.BlackElo, self.WhiteRatingDiff,
                                       self.BlackRatingDiff, self.ECO, self.Opening, self.TimeControl,
                                       self.Time, self.Termination, self.moves)


    def get_pgn_dict(self):
        """
        Gets the dictionary of attributes and their values for the object.

        :return: the dictionary of attributes for the object
        """
        return self.__dict__

    def get_move_pairs(self):
        """
        Creates a list of pairs from the move list. So element 1 is the first move from both players.

        :return: list of strings, each containing two moves that are separated by a single space
        """
        return [i + ' ' + j for i, j in zip(self.moves[::2], self.moves[1::2])]


class Parser(object):
    """
    Parses the .pgn file provided.
    """

    def __init__(self, file):
        """
        Initializes the Parser object.

        :param file: the .pgn file to parse
        """
        self.PGNList = []
        self.file = file
        self.pgn = PGN()
        # self.file_iter = iter(open(self.file, '['))

    def parse_pgn(self, *args):
        """
        Parses the .pgn file assigned to the class.

        :param args: strings of regex to remove from move list (for comments specific to your file)
        :return: list of PGN objects
        """
        with open(self.file) as infile:
            for line in infile:
                # parse tags
                if line.startswith('[') or line.startswith('{'):
                    # Replace '[' and '{' because some may mess it up.
                    for s in PGN.TAGS:
                        if line.split(' ')[0].replace('[', '') == s:
                            self._set_pgn_tags(line, s)

                # parse move list
                elif line.startswith('1.'):
                    self._set_pgn_moves(line, args)
                    self.PGNList.append(self.pgn)
                    self.pgn = PGN()

        return self.PGNList

    def _set_pgn_tags(self, line, match):
        """
        Sets game tags for PGN object.

        :param line: each line in the .pgn file
        :param match: the matching event tag in PGN.TAGS
        """
        setattr(self.pgn, match, line.split('"')[1])

    def _set_pgn_moves(self, line, args):
        """
        Sets the move list for the PGN object.

        :param line: each lin ein the .pgn file
        :param args: strings of regex to remove from move list (for comments specific to your file)
        """
        # Remove '{ [%eval -0.09] }' and excess spaces caused from removing it
        line = re.sub('([\-\d\.\%eval]){4,}|([\{\}\[\]])|([\d\.\d]){2,}', '', line)
        line = re.sub('\s+', ' ', line)

        # Remove anything matching with passed in regex
        for regex in args:
            line = re.sub(regex, '', line)

        # split based on turn #. so '1.' '2.' '3.' each has both players moves in the turn
        move_list = line.split()
        scores = ['0-1', '1-0', '0-0', 'O-1', '1-O', 'O-O', 'o-1', '1-o', 'o-o']
        if move_list[-1] in scores:
            del move_list[-1]
        setattr(self.pgn, 'moves', move_list)