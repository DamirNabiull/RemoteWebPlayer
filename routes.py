from aiohttp import web
from Driver import MyDriver
import logging
import base64
import json

logging.basicConfig(filename='app_routes.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

routes = web.RouteTableDef()
myDriver = MyDriver.getInstance()
driver = myDriver.GetDriver()
config = {}


def ReadConfig():
    global config
    file = open('config.json')
    config = json.load(file)


def WriteConfig():
    global config
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)


@routes.get('/start')
async def get_start(request):
    status = 500
    try:
        driver.get(myDriver.GetLink())
        status = 200
    except Exception as e:
        page_state = driver.execute_script('return document.readyState;') == 'complete'
        if page_state:
            status = 200
    logging.warning(f'/start : status - {status}')
    return web.Response(status=status)


@routes.get('/addTab')
async def get_add(request):
    data = await request.json()
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        driver.get(data['link'])
    except Exception as e:
        driver.close()
        logging.error(f'/addTab : status - No link')
        return web.Response(status=500, text='No link')
    return web.Response(status=200, text='OK')
    # data = {'some': 'data'}
    # return web.json_response(data)


@routes.get('/closeTab')
async def get_close(request):
    if len(driver.window_handles) > 1:
        driver.close()
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])


@routes.get('/setURL')
async def get_url(request):
    status = 500
    try:
        ReadConfig()
        config['show'] = 'url'
        WriteConfig()
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
        ReadConfig()
        config['show'] = 'image'
        WriteConfig()
        while len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])

        try:
            path = config['projectPath']
            img_name = config['image']
            driver.get(rf'{path}\{img_name}')
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
        ReadConfig()
        img_data = data['image']
        img_format = data['image_name'].split('.')[-1]
        config['image'] = f'image.{img_format}'
        WriteConfig()
        with open(config['image'], "wb") as fh:
            fh.write(base64.b64decode(img_data))
        status = 200
    except Exception as e:
        print(e)
    data = {'status': status}
    return web.json_response(status=status, data=data)


@routes.post("/uploadURL")
async def post_url(request):
    data = await request.json()
    status = 500
    try:
        ReadConfig()
        config['url'] = data['url']
        WriteConfig()
        status = 200
    except Exception as e:
        print(e)
    data = {'status': status}
    return web.json_response(status=status, data=data)


@routes.post("/uploadVideo")
async def post_url(request):
    data = await request.json()
    status = 500
    try:
        ReadConfig()
        config['video'] = data['video']
        WriteConfig()
        status = 200
    except Exception as e:
        print(e)
    data = {'status': status}
    return web.json_response(status=status, data=data)