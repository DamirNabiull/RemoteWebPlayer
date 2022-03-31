from aiohttp import web
from routes import routes
import json
import os


if __name__ == '__main__':
    file = open('config.json')
    config = json.load(file)
    config['projectPath'] = os.getcwd()
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=8080)

