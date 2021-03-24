import os
import time
import requests
import shutil
import secrets
import string
import random
from enum import auto
from bs4 import BeautifulSoup

import config


class STATUS(auto):
    OK = 200
    NOT_FOUND = 404


SESSION = requests.session()


class Check:
    @staticmethod
    def check_result_path():
        is_exist = os.path.exists(config.RESULT_PATH)

        if is_exist is False:
            os.makedirs(config.RESULT_PATH)

    @staticmethod
    def check_file_exist(file_name):
        is_exist = os.path.exists(config.RESULT_PATH + file_name)

        return True if is_exist is True else False


class Parser:
    def __init__(self):
        self.url = self.generate_url()

    @staticmethod
    def generate_url():
        url_body = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(random.randint(5, 6)))
        complete_url = config.MAIN_URL + url_body

        return complete_url

    def make_request(self):
        response_result = False

        while response_result is False:
            try:
                with SESSION.get(self.url, headers={'user-agent': config.USER_AGENT}) as get_response:
                    status = get_response.status_code

                    if status == STATUS.OK:
                        response_result = True

                        return get_response.text

                    else:
                        print(f'[main link] {status} Пробуем еще раз через 5 секунд...')
                        time.sleep(5)

            except Exception as error:
                print(str(error.args[0]) + '\t Пробуем еще раз через 15 секунд...')
                time.sleep(15)

    def find_image(self):
        soup = BeautifulSoup(self.make_request(), 'html.parser')
        find_image = soup.find('img', id='screenshot-image')

        try:
            if config.NO_SCREENSHOT not in find_image.attrs['src']:
                image_data = {'url': find_image.attrs['src'], 'id': find_image.attrs['image-id']}

                return image_data

        except Exception:
            return None

    def download_image(self, image_data):
        image_url = image_data['url']
        image_name = image_data['id'] + '.png'

        if Check.check_file_exist(image_name) is False:
            result = False

            try:
                while result is False:
                    with SESSION.get(image_url, stream=True) as get_response:
                        status = get_response.status_code

                        if status == STATUS.OK:
                            with open(config.RESULT_PATH + image_name, 'wb') as save_file:
                                get_response.raw.decode_content = True
                                shutil.copyfileobj(get_response.raw, save_file)

                                print(self.url + ' \t->\t' + image_url + '\t->\t' + config.RESULT_PATH + image_name)
                                result = True

                                return True

                        elif status == STATUS.NOT_FOUND:
                            return False

                        else:
                            print(f'[picture link] {status} Пробуем еще раз через 5 секунд...')
                            time.sleep(5)

            except Exception:
                return False
