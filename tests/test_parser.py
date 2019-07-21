
from unittest import TestCase
from pgn_parser import PGNParser


class TestParser(TestCase):
    def test_parse_pgn(self):
        parser = PGNParser.Parser('tests/test.pgn')
        games = parser.parse_pgn()

        game_string = ''
        for game in games:
            game_string = game_string + game.__str__() + '\n'

        with open('tests/correct_out.txt') as file:
            correct = file.read()
        self.assertTrue(game_string == correct)
