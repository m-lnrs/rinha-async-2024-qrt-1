import os
import locale
import uvicorn
import argparse

from loguru import logger
from rinha.api import app
from rinha.controller import MainController

# set the locale for the application
try:
	locale.setlocale(locale.LC_ALL, os.environ.get("LOCALE", default="pt_BR.UTF-8"))
except:
	logger.warning("impossible to set locale")

if (__name__ == "__main__"):
	parser = argparse.ArgumentParser(description='starts the flask application')
	parser.add_argument('--dev', action='store_true', help='run the server on dev mode with debuger on')
	parser.add_argument('--host', default='127.0.0.1', help='the server host ip')
	parser.add_argument('--port', default='5000', type=int, help='the server port')
	args, unknown = parser.parse_known_args()

	uvicorn.run("asgi:app", host=args.host, port=args.port, reload=args.dev)
