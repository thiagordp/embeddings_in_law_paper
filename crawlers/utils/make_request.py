""""""
import time

import requests
import wget

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"


def get_page(url):
    """

    :param url:
    :return:
    """
    headers = {"user-agent": MOBILE_USER_AGENT}
    data = requests.get(url, headers=headers)

    return data


def download_file(url, dest_path):
    wget.download(url, dest_path)