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
project_id = api.lookup_project_id('AIP Course Management')
print
print 'Project:', project_id

# Get the stories for project.
print
print 'Stories:'
stories = api.list_stories(project_id)

for item in stories['items']:
    print 'raw:', item
    print 'id: ', item['id']
    print '  color:', item['color']
    print '  priority:', item['priority']
    print '  item:', item['text']
    print '  details:', item['details']
    print '  comments:', item['comments']
    print '  tasks:', item['tasks']
    
