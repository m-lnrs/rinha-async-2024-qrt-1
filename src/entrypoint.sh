# bash parameter expansion: assign a DEFAULT value when environment variable not set or null

# PORT will be set to '5000' if APP_PORT not set or null
# the value of APP_PORT remains not set
# PORT="${APP_PORT:-5000}"

# if APP_PORT not set or null, set it's value to '5000'
# then that value will be set to PORT
PORT="${APP_PORT:=5000}"
WORKERS="${APP_WORKERS:=1}"
KEEPALIVE="${APP_KEEPALIVE:=300}"

exec uvicorn --host 0.0.0.0 --port $PORT asgi:app --workers $WORKERS --timeout-keep-alive $KEEPALIVE --loop uvloop --backlog 4092
