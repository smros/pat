""" A specification that determine when and how to activate handlers.
Modify the method create_handlers() to implement custom behavior.
"""

from handlers.debug.handler import PrintHandler
from handlers.feed.handler import FeedHandler
from handlers.mail.handler import MailHandler
from handlers.webhook.handler import WebhookHandler
import api
import yaml
import os.path
from ConfigParser import RawConfigParser
import syslog


# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
WATCHER_PATH = CONFIG.get('watcher', 'path')


def create_handlers(debugging=False):
    """Return a list of handlers."""
    handlers = [
        MailHandler(is_moved_to_ready, watchers),
        MailHandler(is_marked_blocked, everyone),
        MailHandler(is_marked_deployed, active_members_with_creator),
        FeedHandler(u'AgileZen: all', 'all', always),
        WebhookHandler(is_new) ]
    def _create_feedhandler(project_id):
        """Bind project_id within the predicate lambda below."""
        return FeedHandler(u'AgileZen #' + str(project_id),
            'project-' + str(project_id),
            lambda msg: msg.project_id == project_id)
    for project_id in api.get_active_project_ids():
        handlers.append(_create_feedhandler(project_id))
    if debugging:
        handlers.append(PrintHandler())      
    return handlers

def is_new(msg):
    """See comment in message.py"""
    return msg.is_new()

def is_marked_blocked(msg):
    """See comment in message.py"""
    return msg.is_marked_blocked()

def is_marked_deployed(msg):
    """See comment in message.py"""
    return msg.is_marked_deployed()

def is_moved_to_ready(msg):
    """See comment in message.py"""
    return msg.is_moved_to_ready()

def always(msg):
    """For handlers that should trigger in all cases."""
    return True
    
def everyone(msg):
    """Return a list of all mail addresses of all involved people.
    """
    dicts = api.get_people(msg.project_id)
    return set([member['email'] for member in dicts])

def active_members_with_creator(msg):
    """Return a set of mail addresses of all active members and the
    message's creator.
    """
    return active_members(msg) | creators(msg)

def active_members_without_creator(msg):
    """Return a set of mail addresses of all active members except for the
    creator of the message.
    """
    return active_members(msg) - creators(msg)

def active_members(msg):
    """Return a list of all mail addresses of people having the role Members.
    """
    dicts = api.get_people(msg.project_id, 'Members')
    return set([member['email'] for member in dicts])

def creators(msg):
    """Return a set with the creator's mail address."""
    creator = msg.creator_mail
    return set((creator, ))

def watchers(msg):
    """Return a set with all the current watchers of this story"""
    # get msg ID
    storyID=msg.story_id
    print( 'My story ID is '+ str(storyID))
    # get project ID
    projID=msg.project_id
    print( 'My project ID is: ' + str(projID))
    # get watchers (as emails) from yaml file from msg ID
    fpath=os.path.join(WATCHER_PATH,str(projID)+'.yaml')
    print( 'Attempting to open watcher file:' + fpath)
    f=open(fpath,'rt')
    watcherDict=yaml.load(f)
    f.close()
    watcherList=watcherDict[storyID]
    print( 'My watcher list is: ')
    syslog.syslog( 'In watchers handler')
    return(set(watcherList))