'''
Created on Oct 31, 2010

@author: pekka
'''

from game import Game
from pygameview import PygameView
from eventManager import EventManager

#------------------------------------------------------------------------------
from controllers import KeyboardController, CPUSpinnerController

def main():
    """Main program to start the game"""
    
    evManager = EventManager()

    keybd = KeyboardController( evManager )
    spinner = CPUSpinnerController( evManager )
    pygameView = PygameView( evManager )
    game = Game( evManager )
    
    spinner.Run()

if __name__ == "__main__":
    main()
