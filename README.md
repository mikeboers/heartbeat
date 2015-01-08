Personal Server Heartbeats
==========================

Setup on Own Server:
--------------------

~~~

# Clone the project.
git clone git@github.com:mikeboers/heartbeat.git
cd heartbeat

# Setup the virtualenv, requirements, and database.
. bin/bootstrap

# Create a `.env` file with sensible defaults.
cat > .env <<EOF
USERNAME='you'
PASSWORD='monkey'
SECRET_KEY='$(head -c 1024 /dev/urandom | md5)'
NOTIFY_EMAIL='you@example.com'
EOF

# Start the process.
foreman start

~~~


Setup on (2) Heroku Apps:
-------------------------
~~~
# Clone the project.
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
heroku config:set DATABASE_URL="$DATABASE_URL" --app=$WEB

# Setup credentials and notification.
heroku config:set USERNAME=yourname PASSWORD=yourpass --app=$WEB
heroku config:set SECRET_KEY=$(head -c 1024 /dev/urandom | md5) --app=$WEB

# Setup email.
heroku addons:add postmark:10k --app=$WEB
heroku config:set NOTIFY_EMAIL=heartbeat@yoursite.com --app=$WEB
heroku config:set DEFAULT_MAIL_SENDER=heartbeat@yoursite.com --app=$WEB

# Setup Postmark signatures.
heroku addons:open postmark --app=$WEB

# Copy the WEB config to WORKER.
heroku config:set $(heroku config -s --app=$WEB) --app=$WORKER

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


