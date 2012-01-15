from django.template import Context, Template
from django.template.loader import render_to_string


class Story(object):
    def __init__(self, item_story):
        self.id       = item_story['id']
        self.text     = item_story['text']
        self.details  = item_story['details']
        self.tasks    = item_story['tasks']
        self.comments = item_story['comments']

    def get_html_formatted(self):
        info_dict = {'story': self}
        html = render_to_string(
            'story/story.html',
            info_dict
        ).replace('\n', '').replace('\t', '')
        return html

