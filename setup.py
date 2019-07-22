from setuptools import setup

setup(
    name='GameNotationParser',
    version='1.0',
    packages=['tests', 'pgn_parser'],
    url='https://github.com/The-Canuck/PGNParser',
    license='LICENSE',
    author='Peter Morrison',
    author_email='morrisonman56@gmail.com',
    description='A chess pgn parser.',
    long_description=open('README.md').read(),
    keywords='chess pgn game'
)
