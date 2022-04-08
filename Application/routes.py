from aiohttp import web
from Driver import MyDriver
import logging
import base64
import json
import os

logging.basicConfig(filename='app_routes.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

routes = web.RouteTableDef()
myDriver = MyDriver.getInstance()
driver = myDriver.GetDriver()
config = {}


def read_config():
    global config
    file = open('config.json')
    config = json.load(file)


def write_config():
    global config
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)


@routes.get('/ping')
async def get_ping(request):
    data = {'status': 200}
    return web.json_response(status=200, data=data)


@routes.get('/suspend')
async def get_suspend(request):
    os.system('systemctl suspend')
    data = {'status': 200}
    return web.json_response(status=200, data=data)


@routes.get('/setURL')
async def get_url(request):
    status = 500
    try:
        read_config()
        config['show'] = 'url'
        write_config()

        try:
            driver.get(config['url'])
            status = 200
        except Exception as e:
            page_state = driver.execute_script('return document.readyState;') == 'complete'
            if page_state:
                status = 200
            logging.warning(f'setURL : {page_state}')
    except Exception as e:
        logging.error(f'/setURL : status - {e}')
    data = {'status': status}
    return web.json_response(status=status, data=data)


@routes.get('/setImage')
async def get_image(request):
    status = 500
    try:
        read_config()
        config['show'] = 'image'
        write_config()

        try:
            path = os.path.join(config['projectPath'], 'Assets', config['image'])
            driver.get(rf'file://{path}')
            status = 200
        except Exception as e:
            page_state = driver.execute_script('return document.readyState;') == 'complete'
            if page_state:
                status = 200
            logging.warning(f'setImage : {page_state}')
    except Exception as e:
        logging.error(f'/setImage : status - {e}')
    data = {'status': status}
    return web.json_response(status=status, data=data)


@routes.get('/setVideo')
async def get_video(request):
    status = 500
    try:
        read_config()
        config['show'] = 'video'
        write_config()

        try:
            path = os.path.join(config['projectPath'], 'Site', 'index.html')
            driver.get(rf'file://{path}')
            status = 200
        except Exception as e:
            page_state = driver.execute_script('return document.readyState;') == 'complete'
            if page_state:
                status = 200
            logging.warning(f'setVideo : {page_state}')
    except Exception as e:
        logging.error(f'/setVideo : status - {e}')
    data = {'status': status}
    return web.json_response(status=status, data=data)


@routes.post("/uploadImage")
async def post_image(request):
    data = await request.json()
    status = 500
    try:
        read_config()
        img_data = data['image']
        img_format = data['image_name'].split('.')[-1]
        config['image'] = f'image.{img_format}'
        path = os.path.join(config['projectPath'], 'Assets', config['image'])
        write_config()
        with open(path, "wb") as fh:
            fh.write(base64.b64decode(img_data))
        status = 200
    except Exception as e:
        logging.error(f'/uploadImage : status - {e}')
    data = {'status': status}
    return web.json_response(status=status, data=data)


@routes.post("/uploadURL")
async def post_url(request):
    data = await request.json()
    status = 500
    try:
        read_config()
        config['url'] = data['url']
        write_config()
        status = 200
    except Exception as e:
        logging.error(f'/uploadURL : status - {e}')
    data = {'status': status}
    return web.json_response(status=status, data=data)
