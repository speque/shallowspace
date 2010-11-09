'''
Created on Oct 31, 2010

@author: pekka
'''

from game import Game
from pygameview import PygameView
from eventManager import EventManager
import ConfigParser
import os
import constants

#------------------------------------------------------------------------------
from controllers import KeyboardController, CPUSpinnerController
import shallowSpace

def main():
    """Main program to start the game"""
    
    evManager = EventManager()

    programPath = os.path.join(os.path.dirname(shallowSpace.__file__))
    confFilePath = os.path.abspath(programPath, "../../config/config.cfg")
    config = ConfigParser.ConfigParser()
    config.read(confFilePath)
    config.set("Images", "rootdir", os.path.abspath(programPath, "../../"))
    constants.CONFIG = config

    keybd = KeyboardController( evManager )
    spinner = CPUSpinnerController( evManager )
    pygameView = PygameView( evManager )
    game = Game( evManager )
    
    spinner.Run()

if __name__ == "__main__":
    main()
