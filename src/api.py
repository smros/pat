"""Some utility functions to access the AgileZen API (v1)."""

import os.path
import httplib
import json
from string import Template
from ConfigParser import RawConfigParser

# AgileZen-related constants, read API key from cfg.
CFG_PATH = os.path.join(os.path.dirname(__file__), '..', 'settings.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
API_KEY = CONFIG.get('agilezen', 'api_key')
API_DOMAIN = 'agilezen.com'
API_PATH_PREFIX = '/api/v1'
API_HEADERS = {
    "X-Zen-ApiKey": API_KEY,
    "Content-Type": "application/json" }
PROJECTS_URL = 'https://agilezen.com/api/v1/projects'
STORIES_URL = 'https://agilezen.com/api/v1/projects/${project_id}/stories'


def get_projects():
    """Return a list of all projects."""
    conn = httplib.HTTPSConnection(API_DOMAIN)
    conn.request("GET", PROJECTS_URL, headers=API_HEADERS)
##    print 'got here 3'
##    print PROJECTS_URL
##    print API_HEADERS
##    print API_DOMAIN
    response = conn.getresponse().read()
    return _parse_response(response)

def get_people(project_id, role = None):
    """Return a list of members (dictionaries) that have the given role
    in the project. If role is None, return all members.
    """
    path = API_PATH_PREFIX + '/projects/' + str(project_id) + '?with=roles'
    conn = httplib.HTTPSConnection(API_DOMAIN)
    conn.request("GET", path, headers=API_HEADERS)
    response = conn.getresponse().read()
    data = _parse_response(response)
    if role is not None:
        role_dict = _detect(lambda r: r['name'] == role, data['roles'])
        if (role_dict):
            return role_dict['members']
        else:
            raise APIException('Failed to read members with role <'
                + role + '> from API.')
    else:
        result = []
        for each in data['roles']:
            result += each['members']
        return result

def list_stories(project_id):
    """Return a list of all stories."""
    conn = httplib.HTTPSConnection(API_DOMAIN)
    t = Template(STORIES_URL)
    url = t.substitute(dict(project_id=project_id)) + "?with=details,comments,tasks"
##    print 'got here 2'
##    print url
##    print API_HEADERS
##    print API_DOMAIN
    conn.request("GET", url, headers=API_HEADERS)
    response = conn.getresponse().read()
##    print response
    return _parse_response(response)

def get_story(project_id, story_id):
    """Return the details and comments of a story."""
    path = API_PATH_PREFIX
    path +='/projects/' + str(project_id) + '/stories/' + str(story_id)
    path += '?with=details,comments,tags'
    conn = httplib.HTTPSConnection(API_DOMAIN)
    conn.request("GET", path, headers=API_HEADERS)
    response = conn.getresponse().read()
    return _parse_response(response)

def get_active_project_ids():
    """Return a the IDs of all non-archived projects.""" 
    data = get_projects()
    return [int(project['id']) for project in data['items']]
    
def lookup_project_id(name):
    """Return the project's ID with the given name.
    If not found raise exception.
    """
    data = get_projects()
    for project in data['items']:
        if (project['name'] == name):
            return int(project['id'])
    raise APIException('Unknown project name ' + name)     

def _parse_response(response):
    """Try to parse the JSON response. Raises APIException on failure."""
    if response is None:
        raise APIException('Failed to read data from API.')
    try:
        return json.loads(response)
    except:
        raise APIException('Failed to parse data from API.')

def _detect(fun, seq):
    """Return the first element that satisfies the predicate fun."""
    for item in seq:
        if fun(item):
            return item
    return None

class APIException(Exception):
    """Raised when API is not accessible or data cannot be parsed."""
    pass
