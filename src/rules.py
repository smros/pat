""" A specification that determine when and how to activate handlers.
Modify the method create_handlers() to implement custom behavior.
"""

import sys
import time
import re
import httplib

from handlers.debug.handler import PrintHandler
from handlers.feed.handler import FeedHandler
from handlers.mail.handler import MailHandler
import api


def create_handlers(debugging=False):
    """Return a list of handlers."""
    handlers = [
        MailHandler(is_moved_to_ready, active_members_without_creator),
        MailHandler(is_marked_blocked, everyone),
        MailHandler(is_marked_deployed, active_members_with_creator),
        FeedHandler(u'AgileZen: all', 'all', lambda msg: True) ]
    def create_feedhandler(id):
        return FeedHandler(u'AgileZen #' + str(id),
            'project-' + str(id),
            lambda msg: msg.project_id == id)
    for id in api.get_active_project_ids():
        handlers.append(create_feedhandler(id))
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

def everyone(msg):
    """Return a list of all mail addresses of all involved people.
    """
    dicts = api.get_people(msg.project_id)
    return set(map(lambda member: member['email'], dicts))

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
    return set(map(lambda member: member['email'], dicts))

def creators(msg):
    """Return a set with the creator's mail address."""
    creator = msg.creator_mail
    return set((creator, ))
