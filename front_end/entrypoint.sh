cd /var/www
python3 api/main.py &
/opt/docker/bin/entrypoint.sh supervisord
