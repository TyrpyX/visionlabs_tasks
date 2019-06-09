import asyncio
import imghdr
import os
import time
from logging import getLogger, INFO, StreamHandler

import aiohttp
import requests

LOAD_FOLDER = './load'
IMAGE_TYPES = ['jpeg', 'jpg', 'png']
UPLOAD_ENDPOINT = 'http://localhost:5000/images'

logger = getLogger(__name__)


def configure_logger():
    handler = StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(INFO)


async def load_file(path: str) -> None:
    '''
    Uploads only declared file types asynchronously
    :param path: path to folder
    :return:
    '''
    if not os.path.exists(path):
        raise Exception('Provided directory doesn\'t exist')
    async with aiohttp.ClientSession() as session:
        for _object in os.listdir(path):
            file_path = os.path.join(path, _object)
            if os.path.isfile(file_path) and imghdr.what(file_path) in IMAGE_TYPES:
                with open(file_path, 'rb') as file:
                    files = {'file': file}
                    async with session.post(UPLOAD_ENDPOINT, data=files) as resp:
                        if resp.status != 200:
                            logger.warning(f"Can't upload {_object}")
        logger.info("Uploading finished")


def load_sync(path: str) -> None:
    '''
    Uploads only declared file types synchronously
    :param path: path to folder
    :return:
    '''
    if not os.path.exists(path):
        raise Exception('Provided directory doesn\'t exist')
    for _object in os.listdir(path):
        file_path = os.path.join(path, _object)
        if os.path.isfile(file_path) and imghdr.what(file_path) in IMAGE_TYPES:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                requests.post(url=UPLOAD_ENDPOINT, files=files)


if __name__ == "__main__":
    configure_logger()
    asyncio.run(load_file(LOAD_FOLDER))
