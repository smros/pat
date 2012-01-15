import os
import os.path
import httplib
import json
from string import Template

from settings import *

from story import Story


def _parse_response(response):
    '''Try to parse the JSON response. Raises APIException on failure.'''
    
    if response is None:
        raise APIException('Failed to read data from API.')
    
    try:
        return json.loads(response)
    except:
        raise APIException('Failed to parse data from API.')


class APIException(Exception):
    '''Raised when API is not accessible or data cannot be parsed.'''
    pass


class Project(object):

    @classmethod
    def get_projects(cls):
        conn = httplib.HTTPSConnection(API_DOMAIN)
        conn.request('GET', PROJECTS_URL, headers=API_HEADERS)
        response = conn.getresponse().read()
        return _parse_response(response)

    @classmethod
    def lookup_project_id(cls, name):
        '''
        Return the project's ID with the given name.
        If not found raise exception.
        '''
        
        data = cls.get_projects()
        
        for project in data['items']:
            if (project['name'] == name):
                return int(project['id'])
            
        raise APIException('Unknown project name ' + name)

    def __init__(self, project_text):
        self.id = self.lookup_project_id(project_text)
        self.stories = []
        
        stories_from_azen = self.az_api_list_stories()
        
        for story_from_azen in stories_from_azen['items']:
            story = Story(story_from_azen)
            self.stories.append(story)

    def _detect(self, fun, seq):
        '''Return the first element that satisfies the predicate fun.'''
        # I don't like this one bit <gis>
        
        for item in seq:
            if fun(item):
                return item
        return None

    def az_api_list_stories(self):
        '''Return a list of all stories.'''
        conn = httplib.HTTPSConnection(API_DOMAIN)
        t = Template(STORIES_URL)
        url = t.substitute(
            dict(project_id=self.id)
        ) + '?with=everything'
        conn.request('GET', url, headers=API_HEADERS)
        response = conn.getresponse().read()
        return _parse_response(response)

    def az_api_get_people(self, role=None):
        path = API_PATH_PREFIX + '/projects/' + str(self.id) + '?with=roles'
        conn = httplib.HTTPSConnection(API_DOMAIN)
        conn.request('GET', path, headers=API_HEADERS)
        response = conn.getresponse().read()
        data = _parse_response(response)
        
        if role is not None:
            # there has to be a better way to do this than "self._detect"
            
            role_dict = self._detect(
                lambda r: r['name'] == role, data['roles']
            )
            
            if (role_dict):
                return role_dict['members']
            else:
                raise APIException(
                    'Failed to read members with role <' + role + '> from API.'
                )
        else:
            result = []
            
            for each in data['roles']:
                result += each['members']
            return result

    def get_stories(self):
        return self.stories

    def get_story_by_id(self, id):
        story_to_return = None
        
        for story in self.stories:
            if story.id == id:
                story_to_return = story

        return story_to_return

    def get_story_by_text(self, text):
        story_to_return = None
        
        for story in self.stories:
            if story.text == text:
                story_to_return = story

        return story_to_return

    def get_stories_by_owner(self, name):
        stories_to_return = []

        for story in self.stories:
            if story.owner['name'] == name:
                stories_to_return.append(story)

        return stories_to_return

    def write_html(self):
        html_staging_path = './html_staging/%i' % self.id
        
        if not os.path.exists(html_staging_path):
            os.makedirs(html_staging_path, mode=0755)

        html_staging_path_file = html_staging_path + '/' + str(self.id) + '.html'

        html_file = open(html_staging_path_file, 'w')

        for story in self.stories:
            html_file.write(story.get_html_formatted())
            print 'wrote story: %i; %s' % (story.id, story.text)

        html_file.close()

    def write_story_html(self, story_id):
        html_staging_path = './html_staging/%i' % self.id
        
        if not os.path.exists(html_staging_path):
            os.makedirs(html_staging_path, mode=0755)

        html_staging_path_file = html_staging_path + '/' + str(self.id) + '.html'

        for story in self.stories:
            if story.id == story_id:
                story_file_path = html_staging_path + '/' + str(story.id) + '.html'
                story_file = open(story_file_path, 'w')
                story_file.write(story.get_html_formatted())
                print 'wrote story: %i; %s' % (story.id, story.text)
