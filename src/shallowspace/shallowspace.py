'''
Created on Oct 31, 2010

@author: pekka
'''

from game import Game
from pygameview import PygameView
from eventmanager import EventManager
from controllers import KeyboardController, CPUSpinnerController

#------------------------------------------------------------------------------
def main():
    """Main program to start the game"""
    
    evManager = EventManager()

    keybd = KeyboardController( evManager )
    spinner = CPUSpinnerController( evManager )
    game = Game( evManager )
    pygameView = PygameView( evManager )
    
    spinner.run()

if __name__ == "__main__":
    main()
