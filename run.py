import sys

sys.path.append('src')

import api


result = api.get_projects()
print
for key, val in result.iteritems():
    print key, val
    
items = result['items']
print
print 'Items:'
for item in items: #Note:  This is actually a list of the projects.
    print item

# Look at project 0.
item = items[0]
print
print 'Items[0]:'
for key, val in item.iteritems():
    print key, val


# Lookup a non-archived project (case sensitive)
project_id = api.lookup_project_id('Test Project')
print
print 'Project:', project_id

# Get the stories for project.
print
print 'Stories:'
stories = api.list_stories(project_id)

storiesDict=dict()

for item in stories['items']:
    print 'raw:', item
    print 'id: ', item['id']
    print '  color:', item['color']
    print '  priority:', item['priority']
    print '  item:', item['text']
    print '  details:', item['details']
    print '  comments:', item['comments']
    print '  tasks:', item['tasks']
    print '  milestones:', item['milestones']
    storiesDict[item['id']]=item

print 'storiesDict:'

print storiesDict

story=4

print "Here's story " + str(story)
print storiesDict[story]

print "Here's story " + str(story) + "'s comments"
comments=storiesDict[story]['comments']
print comments
for item in comments:
    print item['text']
    print item['createTime']
    print item['author']['userName']

zzz=raw_input('Waiting...')

print 'Milestones for item ' + str(story)
milestones= storiesDict[story]['milestones']

for item in milestones:
    print item


print 'Test Pull stories by username'

stories=api.list_stories_filter_by_user_and_tag(project_id,user='smroszczak')
for item in stories:
    print item

print 'Test Pull stories by tag'

stories=api.list_stories_filter_by_user_and_tag(project_id,tag='government_renewal')
print stories
for item in stories:
    print item

#print 'Test Pull stories by tag and username'


    
