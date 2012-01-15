# This app requires a "settings.py" file. Use this file as a template
# and put your AgileZen API key in AGILE_ZEN_API_KEY

AGILE_ZEN_API_KEY = '<your agilezen api key kere>'

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
