from django.template.loader import render_to_string


class Story(object):
    def __init__(self, item_story):
        self.id       = item_story['id']
        self.colour   = item_story['color']
        self.priority = item_story['priority']

        if item_story.has_key('deadline'):
            self.deadline = item_story['deadline']
        else:
            self.deadline = None
            
        self.size     = item_story['size']
        self.status   = item_story['status']
        self.owner    = item_story['owner']
        self.phase    = item_story['phase']
        self.text     = item_story['text']
        self.details  = item_story['details']
        self.tasks    = item_story['tasks']
        self.comments = item_story['comments']
        self.tags     = item_story['tags']

    def get_html_formatted(self):
        info_dict = {'story': self}
        html = render_to_string(
            'story/story.html',
            info_dict
        ).replace('\n', '').replace('\t', '')
        return html
