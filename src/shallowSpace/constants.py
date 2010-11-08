'''
Created on Oct 31, 2010

@author: pekka
'''

import ConfigParser

DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3

GRID_SIZE = 70

CONF_FILE = "/home/pekka/Dropbox/ShallowSpace/config/config.cfg"

def getGameConfig():
    config = ConfigParser.ConfigParser()
    config.read(CONF_FILE)
    return config
    
CONFIG = getGameConfig()