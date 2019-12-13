[DEV]
## celery run
celery -A dmcode_server.celery_run worker -B --loglevel=debug

