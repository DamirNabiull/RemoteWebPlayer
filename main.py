from aiohttp import web
from routes import routes
from Driver import MyDriver


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=8080)

    myDriver = MyDriver.getInstance()
    driver = myDriver.GetDriver()
