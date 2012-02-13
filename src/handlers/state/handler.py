"""A handle for updating the yaml state files."""
from ConfigParser import RawConfigParser
import os.path
import api
import yaml
import sys
sys.path.append('../../src')

## Config stuff here

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..','..','..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
WATCHER_PATH = os.path.join(
    os.path.dirname(__file__), '..','..','..',CONFIG.get('watcher', 'path') )

class StateHandler():
    
    def __init__(self,interested_in, getrecipients):
        self.interested_in = interested_in
        self.getrecipients = getrecipients
        
    def handle(self, message):

        # Load the yaml for the stored watcher list,
        # get the owner and creator for the given story, then add them
        # to the list and 'set' the list to remove duplicates.

        print message
        prjID=message.project_id
        storyID=message.story_id

        fname=os.path.join(WATCHER_PATH, str(prjID)+'.yaml')
        try:
            print fname
            f=open(fname,'rt')
            storyDict=yaml.load(f)
        except IOError as e:
            print 'Exception in file open, in state handler, creating file'
            print e
            # File doesn't exist,create it
            f=open(fname,'wt')
            f.close()
            f=open(fname,'rt')
            storyDict=dict()
        
        f.close()

        if storyDict:
            if storyDict.__contains__(storyID):
                storyList=storyDict[storyID]
                storyList.append(message.creator_mail)
                storyList.append(message.owner_mail)
            else:
                storyList=[message.creator_mail, message.owner_mail]

        else:
            storyList=[message.creator_mail, message.owner_mail]
            storyDict=dict()

        storyDict[storyID]=list(set(storyList))

        try:
            f=open(fname,'wt')
        except IOError as e:
            print 'Exception in file open, in state handler.'
            print e

        f.write(yaml.dump(storyDict))
        f.close()




        
