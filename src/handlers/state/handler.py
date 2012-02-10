"""A handle for updating the yaml state files."""
from ConfigParser import RawConfigParser
import os.path

## Config stuff here

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..','..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
WATCHER_PATH = os.path.join(
    os.path.dirname(__file__), '..',CONFIG.get('watcher', 'path') )

class StateHandler():
    
    def __init__(self):
        pass
        
    def handle(self, message):
        print message