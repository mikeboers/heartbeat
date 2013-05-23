Personal Server Heartbeats
==========================

~~~
git clone git@github.com:mikeboers/heartbeat.git
cd heartbeat

# Name to taste.
WEB=web-heartbeat-$(whoami)
WORKER=worker-heartbeat-$(whoami)

# Create a Heroku app for the web server and worker (sorry Heroku).
heroku create --remote web $WEB
heroku create --remote worker $WORKER
heroku labs:enable user-env-compile --app=$WEB
heroku labs:enable user-env-compile --app=$WORKER

# Provision the database
heroku addons:add heroku-postgresql:dev --app=$WEB
DATABASE_URL=$(heroku config --shell --app=$WEB | grep HEROKU_POSTGRES | cut -d= -f2-)
heroku config:set "DATABASE_URL=$DATABASE_URL" --app=$WEB
heroku config:set "DATABASE_URL=$DATABASE_URL" --app=$WORKER

# Setup credentials and notification.
heroku config:set USERNAME=yourname PASSWORD=yourpass --app=$WEB
heroku config:set SECRET_KEY=$(head -c 1024 /dev/urandom | md5) --app=$WEB

# Setup email.
heroku addons:add postmark:10k --app=$WEB
heroku addons:add postmark:10k --app=$WORKER
heroku config:set NOTIFY_EMAIL=heartbeat@mikeboers.com --app=$WEB
heroku config:set NOTIFY_EMAIL=heartbeat@mikeboers.com --app=$WORKER


# Deploy.
git push web
git push worker

# Setup the processes.
heroku ps:scale web=1 --app=$WEB
heroku ps:scale web=0 worker=1 --app=$WORKER
~~~

And you're done.

To bulk-add a few services:

~~~
for site in alice.com bob.com; do
   echo "INSERT INTO services (name, cron_spec, url_to_monitor) VALUES ('$site', '*/5 * * * *', 'http://$site');" | heroku pg:psql --app=$WEB
done
~~~

For a local install:

~~~
virtualenv --no-site-packages venv
. venv/bin/activate
pip install -r requirements
./bin/migrate
foreman start
~~~

