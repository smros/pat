"""A handle for updating the yaml state files."""
from ConfigParser import RawConfigParser
import os.path
import sys
sys.path.append('../../src')
import api

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
        print message
        prjID=message.project_id
        storyID=message.story_id

        fname=os.path.join(WATCHER_PATH, str(prjID)+'.yaml')
        try:
            print fname
            f=open(fname,'rt')
        except IOError as e:
            print 'Exception in file open, in state handler.'
            print e

        storyDict=yaml.load(f)
        f.close()

        if storyDict.__contains__(storyID):
            storyList=storyDict[storyID]
            storyList.append(message.creator_mail)
            storyDict[storyID]=list(set(storyList))
        else:
            storyDict[storyID]=list(message.creator_mail)

        try:
            f=open(fname,'wt')
        except IOError as e:
            print 'Exception in file open, in state handler.'
            print e

        f.write(yaml.dump(storyDict))
        f.close()




        
