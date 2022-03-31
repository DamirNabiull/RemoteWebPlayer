from aiohttp import web
import json
import os


def set_config():
    file = open('config.json')
    config = json.load(file)
    config['projectPath'] = os.getcwd()
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)


if __name__ == '__main__':
    set_config()

    from routes import routes

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=8080)

