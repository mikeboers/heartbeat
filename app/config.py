import datetime
import os

ROOT_PATH = os.path.abspath(os.path.join(__file__, '..', '..'))

DEBUG = bool(os.environ.get("DEBUG"))

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

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
SECRET_KEY = os.environ.get('SECRET_KEY')

NOTIFY_EMAIL = os.environ.get('NOTIFY_EMAIL')
NOTIFY_PROWL = os.environ.get('NOTIFY_PROWL')
NOTIFY_ANDROID = os.environ.get('NOTIFY_ANDROID')

MAIL_SERVER = os.environ.get('MAIL_SERVER') or os.environ.get('POSTMARK_SMTP_SERVER') or 'localhost'
MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or os.environ.get('POSTMARK_API_KEY')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or os.environ.get('POSTMARK_API_KEY')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or NOTIFY_EMAIL

PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=20*365)

