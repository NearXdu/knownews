from aiohttp import web
from aiohttp import web
from route import *

app = web.Application()
setup_routes(app)
web.run_app(app, host="0.0.0.0", port=8080)
