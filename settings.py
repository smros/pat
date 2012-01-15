AGILE_ZEN_API_KEY = '1b40a889322e460e89a575dab15f7419'

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
