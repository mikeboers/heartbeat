Personal Server Heartbeats
==========================

~~~
git clone git@github.com:mikeboers/heartbeat.git
cd heartbeat

# Name to taste.
WEB=web-heartbeat-$(whoami)
WORKER=worker-heartbeat-$(whoami)

# Create a Heroku app for the web server.
heroku create --remote server $WEB
heroku create --remote worker $WORKER
heroku labs:enable user-env-compile -a $WEB
heroku labs:enable user-env-compile -a $WORKER

# Provision the database
heroku addons:add heroku-postgresql:dev --app=$WEB
DATABASE_URL=$(heroku config --shell --app=$WEB | grep HEROKU_POSTGRES | cut -d= -f2)
heroku config:set "DATABASE_URL=$DATABASE_URL" --app=$WEB
heroku config:set "DATABASE_URL=$DATABASE_URL" --app=$WORKER

# Deploy.
git push web
git push worker

# Setup the processes.
heroku ps:scale web=1 --app=$WEB
heroku ps:scale web=0 worker=1 --app=$WORKER
~~~

And you're done.
