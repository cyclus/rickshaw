$PROJECT = $GITHUB_REPO = 'rickshaw'
$GITHUB_ORG = 'cyclus'

$ACTIVITIES = ['pytest', 'version_bump', 'changelog', 'tag', 'push_tag',
               'pypi',
               #'conda_forge',  # no feedstock yet
               'ghrelease']
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'

$DOCKER_CONDA_DEPS = ['python-json-logger', 'pprintpp', 'jinja2']
$DOCKER_INSTALL_COMMAND = 'git clean -fdx && ./setup.py install --user'

$VERSION_BUMP_PATTERNS = [
    ('rickshaw/__init__.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', 'VERSION\s*=.*', "VERSION = '$VERSION'"),
]
