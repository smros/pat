"""A handle for updating the database."""
from ConfigParser import RawConfigParser
import os.path
import sys
sys.path.append('../../src')
sys.path.append('../../src/db')
from projectStory import projectStoriesDB
import api

## Config stuff here

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..','..','..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
DB_NAME =  os.path.join(
    os.path.dirname(__file__), '..','..','..',CONFIG.get('db', 'dbname') )


class dbHandler():
    
    def __init__(self,interested_in, getrecipients):
        self.interested_in = interested_in
        self.getrecipients = getrecipients
        
    def handle(self, message):

        print message
        prjID=message.project_id
        storyID=message.story_id
        owner=message.owner

        # Check if story is in DB yet, with startTime

            # If so, check if story has been moved to anything but Working,
            # then  calculate duration, update endtime

        # Else, if story is not in db, check if it is marked working
            # If so, insert a new event into DB.
            # If not, ignore quit


  




        
