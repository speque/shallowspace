'''
Created on Oct 31, 2010

@author: pekka
'''

from game import Game
from pygameview import PygameView
from eventmanager import EventManager
from controllers import KeyboardController, CPUSpinnerController
import argparse
from constants import DEBUG

#------------------------------------------------------------------------------
def main():
    """Main program to start the game"""
    
    parser = argparse.ArgumentParser(description='Shallow Space')
    parser.add_argument('--debug', dest='debug', action='store_true',
       default=False, help='turn on debug')

    args = parser.parse_args()
    
    DEBUG = args.debug

    evManager = EventManager()

    keybd = KeyboardController( evManager )
    spinner = CPUSpinnerController( evManager )
    game = Game( evManager )
    pygameView = PygameView( evManager )
    
    spinner.run()

if __name__ == "__main__":
    main()
