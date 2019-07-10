#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import glob
import datetime
import json

import base64
import requests
import socket
import wget

import vkapi


def remove_symbols(filename):
    if len(filename) >=128:
        return re.sub(r'[\\\\/:*?\"<>|\n\r\xa0]', "", filename[0:126])
    else:
        return re.sub(r'[\\\\/:*?\"<>|\n\r\xa0]', "", filename)


def file_exists(path):
    try:
        return os.path.exists(path)
    except OSError:
        return False


def get_path(self, flags, Object):
    if flags:
        path = Object.getExistingDirectory(self, "Выберите папку для скачивания", "", Object.ShowDirsOnly)
        if path == "":
            return os.getcwd()
        else:
            return path
    else:
        return os.getcwd()


def remove_files(paths):
    files = glob.glob(paths)
    
    if not files:
        return True

    for file in files:
        try:
            os.remove(file)
        except:
            continue


def get_host_api(flags):
    if flags:
        return vkapi.HOST_API_PROXY
    else:
        return vkapi.HOST_API


def get_host_oauth(flags):
    if flags:
        return vkapi.OAUTH_PROXY
    else:
        return vkapi.OAUTH


def check_connection(url):
    try:
        requests.get(url, timeout=5)
    except Exception:
        return False

    return True


def get_internal_ip():
    try:
        return socket.gethostbyname(socket.getfqdn())
    except Exception:
        return None


def get_external_ip():
    try:
        return bytes(requests.get("http://ident.me/", timeout=5).content
            ).decode("utf-8")

    except Exception:
        return None


def get_network_info():
    return requests.get("http://ipinfo.io", timeout=5).json()


def unix_time_stamp_convert(time):
    return datetime.datetime.fromtimestamp(int(time)
        ).strftime("%d.%m.%Y %H:%M:%S")


def time_duration(time):
    return str(datetime.timedelta(seconds=int(time)))


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


def downloads_files_in_wget(url, filename, progress):
    wget.download(url, filename, bar=progress)


def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)