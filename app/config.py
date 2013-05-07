import os

ROOT_PATH = os.path.abspath(os.path.join(__file__, '..', '..'))

# Not the best test, but there it is.
IS_HEROKU = os.environ.get('HOME') == '/app' and '.heroku' in os.environ.get('LIBRARY_PATH', '')

if IS_HEROKU:
    TEMPORARY_DATABASE_URI = 'sqlite://'
else:
    sqlite_dir = os.path.join(ROOT_PATH, 'var', 'sqlite')
    if not os.path.exists(sqlite_dir):
        os.makedirs(sqlite_dir)
    TEMPORARY_DATABASE_URI = 'sqlite:///%s' % os.path.join(ROOT_PATH, 'var', 'sqlite', 'main.sqlite')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', TEMPORARY_DATABASE_URI)
