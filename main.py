import argparse
import sys

from parser.parser import *


def parser():
    parser_args = argparse.ArgumentParser(description='Парсер изображений с prnt.sc')
    parser_args.add_argument('count', type=int, help='Колличество получаемых изображений')

    return parser_args


if __name__ == '__main__':
    args = parser().parse_args()

    count = args.count
    result = 0

    try:
        Check.check_result_path()

    except Exception as error:
        sys.exit('Не могу создать папку' + str(error))

    while result != count:
        img_parser = Parser()

        image_found = img_parser.find_image()

        if image_found:
            download_image = img_parser.download_image(image_found)

            if download_image is True:
                result += 1
