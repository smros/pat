from django.template.loader import render_to_string
from decimal import Decimal

from settings import (
    TYPE_TAGS,
    COST_CATEGORY_TAGS,
)


class Story(object):
    
    def __init__(self, project=None, item_story=None):
        self.id       = item_story['id']
        self.project  = project
        self.colour   = item_story['color']
        self.priority = item_story['priority']

        if item_story.has_key('deadline'):
            self.deadline = item_story['deadline']
        else:
            self.deadline = None
            
        self.size          = item_story['size']
        self.status        = item_story['status']
        self.owner         = item_story['owner']
        self.phase         = item_story['phase']
        self.text          = item_story['text']
        self.details       = item_story['details']
        self.tasks         = item_story['tasks']
        self.comments      = item_story['comments']
        self.tags          = item_story['tags']
        self.types         = []
        self.cost_category = ''

        self.determine_type_and_order()
        self.determine_cost_category()

        if self.cost_category not in self.project.cost_categories:
            self.project.cost_categories.append(self.cost_category)

    def determine_type_and_order(self):
        for tag in self.tags:
            for type_tag in TYPE_TAGS:
                if tag['name'].find(type_tag) > -1:
                    self.types.append(type_tag)

    def determine_cost_category(self):
        for tag in self.tags:
            if tag['name'] in COST_CATEGORY_TAGS:
                self.cost_category = tag['name']

    def get_html_formatted(self):
        info_dict = {'story': self}
        html = render_to_string(
            'story/story.html',
            info_dict
        ).replace('\n', '').replace('\t', '')
        return html
