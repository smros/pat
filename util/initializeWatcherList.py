#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="steve"
__date__ ="$10-Feb-2012 1:14:28 PM$"

# Initializes the watcher files for the Agile Zen notifier
# Goes through the projects, creates a dict for each story with the creater and
# owner of each and writes it to a yaml file.

import yaml
import os.path
from ConfigParser import RawConfigParser
import sys
sys.path.append('../src')
import api

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
WATCHER_PATH = os.path.join(
    os.path.dirname(__file__), '..',CONFIG.get('watcher', 'path') )
API_KEY = CONFIG.get('api','key')



if __name__ == "__main__":

#    zz=raw_input('This will overwrite any existing watcher files.  Proceed? (Y/N)?')
#    if zz!='Y' and zz!='y':
#        sys.exit(0)
    print API_KEY
    print CFG_PATH
    print WATCHER_PATH
    projects=api.get_projects()
    print projects



    for item in projects['items']:
        watchersDict=dict()
        id=item['id']
        print id
        fname=os.path.join(WATCHER_PATH, str(id)+'.yaml')
        try:
            print fname
            f=open(fname,'wt')
        except IOError as e:
            print 'Exception in file open'
            print e

        stories=api.get_stories(item['id'])
        for story in stories['items']:
#            print story['owner']['email']
#            print story['creator']['email']
            print 'Story ID: '+str(story['id'])+', owner: ' + story['owner']['email'] + ', creator: ' + story['creator']['email']
            currentList=[ story['creator']['email'], story['owner']['email' ] ]
            # Remove duplicates
            currentList=list(set(currentList))
            print currentList
            watchersDict[story['id']] = currentList

        print watchersDict
        f.write(yaml.dump(watchersDict))
        f.close()


