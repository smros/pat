import os
import os.path
import httplib
import json
from string import Template
from decimal import Decimal

from settings import (
    AGILE_ZEN_API_KEY,
    API_DOMAIN,
    API_PATH_PREFIX,
    API_HEADERS,
    PROJECTS_URL,
    STORIES_URL,
    STORY_SIZE_VALUES,
)

from django.template.loader import render_to_string

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
    def get_project_by_id(cls, id):
        conn = httplib.HTTPSConnection(API_DOMAIN)
        conn.request(
            'GET',
            PROJECTS_URL + '/' + str(id) + '/?with=everything',
            headers=API_HEADERS
        )
        response = conn.getresponse().read()
        return _parse_response(response)

    @classmethod
    def get_projects(cls):
        conn = httplib.HTTPSConnection(API_DOMAIN)
        conn.request(
            'GET', PROJECTS_URL + '?with=everything', headers=API_HEADERS
        )
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

        project_from_azen = Project.get_project_by_id(self.id)
        self.createTime   = project_from_azen['createTime']
        self.description  = project_from_azen['description']
        self.details      = project_from_azen['details']
        self.invites      = project_from_azen['invites']
        self.members      = project_from_azen['members']
        self.metrics      = project_from_azen['metrics']
        self.name         = project_from_azen['name']
        self.owner        = project_from_azen['owner']
        self.phases       = project_from_azen['phases']
        self.roles        = project_from_azen['roles']

        self.cost_categories = []

        stories_from_azen = self.az_api_list_stories()
        
        for story_from_azen in stories_from_azen['items']:
            story = Story(self, story_from_azen)
            self.stories.append(story)

    def get_stories_by_type(self, story_type, order_mask=0):
        if order_mask == 0:
            story_fiter_string = '%s' % (story_type)
            ordering = False
            stories = []
        else:
            story_fiter_string = '%s %i' % (story_type, order_mask)
            ordering = True
            stories = {}

        for story in self.stories:
            for tag in story.tags:
                if tag['name'].find(story_fiter_string) > -1:
                    if ordering:
                        story_type_from_tag, order = tag['name'].split()
                        order = Decimal(order)
                        stories[order] = story
                    else:
                        stories.append(story)

        if ordering:
            stories_ordered = []
            keys = stories.keys()
            keys.sort()
            
            for key in keys:
                stories_ordered.append(stories[key])

            stories = stories_ordered

        return stories

    def get_stories_by_type_cost_category(
        self, story_type=None, cost_category=None):
        
        stories_type_list = []
        stories_cost_category_list = []

        for story in self.stories:
            for tag in story.tags:
                if tag['name'].find(story_type) > -1:
                    stories_type_list.append(story)

        for story in self.stories:
            for tag in story.tags:
                if tag['name'] == cost_category:
                    stories_cost_category_list.append(story)

        return set(stories_type_list).intersection(
            set(stories_cost_category_list)
        )

    def _detect(self, func, seq):
        '''Return the first element that satisfies the predicate func.'''
        # I don't like this one bit ... maybe I just don't get it :) <gis>
        
        for item in seq:
            if func(item):
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
            # there has to be a better way to do this than "self._detect" <gis>
            
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

    def get_project_description(self):
        return self.description.replace('\n', '').replace('\t', '')

    def get_stories(self):
        return self.stories

    def get_story_by_id(self, id):
        story_to_return = None
        
        for story in self.stories:
            if story.id == id:
                story_to_return = story
                break

        return story_to_return

    def get_story_by_text(self, text):
        story_to_return = None
        
        for story in self.stories:
            if story.text == text:
                story_to_return = story
                break

        return story_to_return

    def get_stories_by_owner(self, name):
        stories_to_return = []

        for story in self.stories:
            if story.owner['name'] == name:
                stories_to_return.append(story)

        return stories_to_return

    def get_html_formatted(self):
        info_dict = {'project': self}
        html = render_to_string(
            'project/project.html',
            info_dict
        ).replace('\n', '').replace('\t', '')
        return html

    def sum_stories_size(self, story_type=None, cost_category=None):
        stories = self.get_stories_by_type_cost_category(
            story_type=story_type, cost_category=cost_category
        )
        total_size = Decimal('0.00')

        for story in stories:
            size, unit = story.size.split()
            size = Decimal(size)
            total_size += size

        return total_size

    def write_project_html(self):
        html_staging_path = './html_staging/%i' % self.id
        
        if not os.path.exists(html_staging_path):
            os.makedirs(html_staging_path, mode=0755)

        html_staging_path_file = \
            html_staging_path + '/' + str(self.id) + '_project.html'

        html_file = open(html_staging_path_file, 'w')
        html_file.write(self.get_html_formatted())
        print 'wrote project: %i; %s' % (self.id, self.name)
        html_file.close()

    def write_all_project_stories_html(self):
        html_staging_path = './html_staging/%i' % self.id
        
        if not os.path.exists(html_staging_path):
            os.makedirs(html_staging_path, mode=0755)

        html_staging_path_file = \
            html_staging_path + '/' + str(self.id) + '_all_stories.html'

        html_file = open(html_staging_path_file, 'w')

        for story in self.stories:
            html_file.write(story.get_html_formatted())
            html_file.write('<hr/>')
            print 'wrote story: %i; %s' % (story.id, story.text)

        html_file.close()

    def write_stories_by_type_html(self, story_type, order_mask=0):
        html_staging_path = './html_staging/%i' % self.id
        
        if not os.path.exists(html_staging_path):
            os.makedirs(html_staging_path, mode=0755)

        html_staging_path_file = \
            html_staging_path + '/' + str(self.id) + '_' + story_type + '.html'

        html_file = open(html_staging_path_file, 'w')

        stories = self.get_stories_by_type(story_type, order_mask=order_mask)

        for story in stories:
            html_file.write(story.get_html_formatted())
            html_file.write('<hr/>')
            print 'wrote story: %i; %s' % (story.id, story.text)

        html_file.close()

    def write_story_html(self, story_id):
        html_staging_path = './html_staging/%i' % self.id
        
        if not os.path.exists(html_staging_path):
            os.makedirs(html_staging_path, mode=0755)

        html_staging_path_file = html_staging_path + '/' + str(self.id) + '.html'

        for story in self.stories:
            if story.id == story_id:
                story_file_path = \
                    html_staging_path + '/' + str(story.id) + '.html'
                story_file = open(story_file_path, 'w')
                story_file.write(story.get_html_formatted())
                print 'wrote story: %i; %s' % (story.id, story.text)
                break
