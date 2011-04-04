'''
Created on Oct 31, 2010

@author: pekka
'''

from game import Game
from pygameview import PygameView
from eventmanager import EventManager
from controllers import KeyboardController, CPUSpinnerController
import argparse
import constants

#------------------------------------------------------------------------------
def main():
    """Main program to start the game"""
    
    parser = argparse.ArgumentParser(description='Shallow Space')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
       default=False, help='turn on debug')

    args = parser.parse_args()

    constants.DEBUG = args.debug

    event_manager = EventManager()

    keyboard_controller = KeyboardController(event_manager)
    spinner = CPUSpinnerController(event_manager)
    game = Game(event_manager)
    pygame_view = PygameView(event_manager)
    
    spinner.run()

if __name__ == "__main__":
    main()
