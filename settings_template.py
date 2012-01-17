# This app requires a "settings.py" file. Use this file as a template
# and put your AgileZen API key in AGILE_ZEN_API_KEY.

from decimal import Decimal


AGILE_ZEN_API_KEY = '<your AgileZen API key here>'

API_DOMAIN = 'agilezen.com'
API_PATH_PREFIX = '/api/v1'
API_HEADERS = {
    "X-Zen-ApiKey": AGILE_ZEN_API_KEY,
    "Content-Type": "application/json" }
PROJECTS_URL = 'https://agilezen.com/api/v1/projects'
STORIES_URL = 'https://agilezen.com/api/v1/projects/${project_id}/stories'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    '/home/greg/projects/pat/templates/',
)

''' Example

TYPE_TAGS = (
    'proposal',
    'core component',
)
'''

TYPE_TAGS = ()

''' Example

COST_CATEGORY_TAGS = (
    'base',
    'base 20',
)
'''

COST_CATEGORY_TAGS = ()

# Size should always be a "unit" such as "days" (d) and a value separated
# by white space.

''' Example

STORY_SIZE_VALUES = {
    'd': Decimal('8.00')
    'day': Decimal('8.00')
    'days': Decimal('8.00')
}
'''

STORY_SIZE_VALUES = {}
