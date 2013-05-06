import os

# Not the best test, but there it is.
IS_HEROKU = os.environ.get('HOME') == '/app' and '.heroku' in os.environ.get('LIBRARY_PATH', '')


SQLALCHEMY_DATABASE_URI = 'sqlite://'
