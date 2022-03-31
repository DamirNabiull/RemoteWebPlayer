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
    return web.Response(status=200)


@routes.get('/setURL')
async def get_url(request):
    status = 500
    try:
        read_config()
        config['show'] = 'url'
        write_config()
        while len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])

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
async def get_url(request):
    status = 500
    try:
        read_config()
        config['show'] = 'image'
        write_config()
        while len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])

        try:
            path = os.path.join(config['projectPath'], 'Assets', config['image'])
            driver.get(rf'file://{path}')
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


@routes.post("/uploadImage")
async def post_image(request):
    data = await request.json()
    status = 500
    try:
        read_config()
        img_data = data['image']
        img_format = data['image_name'].split('.')[-1]
        config['image'] = f'image.{img_format}'
        write_config()
        with open(config['image'], "wb") as fh:
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


@routes.post("/uploadVideo")
async def post_url(request):
    data = await request.json()
    status = 500
    try:
        read_config()
        config['video'] = data['video']
        write_config()
        status = 200
    except Exception as e:
        logging.error(f'/uploadVideo : status - {e}')
    data = {'status': status}
    return web.json_response(status=status, data=data)