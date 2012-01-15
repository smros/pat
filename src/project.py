import os
import api
from story import Story


class Project(object):
    def __init__(self, project_text):
        self.id = api.lookup_project_id(project_text)
        self.stories = []
        
        stories_from_azen = api.list_stories(self.id)
        
        for story_from_azen in stories_from_azen['items']:
            story = Story(story_from_azen)
            self.stories.append(story)

    def get_stories(self):
        return self.stories

    def get_story(self, id):
        story_to_return = None
        
        for story in self.stories:
            if story.id == id:
                story_to_return = story

        return story_to_return

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

        html_staging_path_file = html_staging_path + '/' + str(project.id) + '.html'

        story_file = open(html_staging_path_file, 'w')

        for story in self.stories:
            story_file_path = html_staging_path + '/' + str(story.id) + '.html'
            story_file = open(story_file_path, 'w')
            story_file.write(story.get_html_formatted())
            print 'wrote story: %i; %s' % (story.id, story.text)
