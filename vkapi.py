#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

# Домен API
HOST_API = 'https://api.vk.com/'
# Домен OAuth
OAUTH = 'https://oauth.vk.com/'

HOST_API_PROXY ="https://vk-api-proxy.xtrafrancyz.net/"
OAUTH_PROXY = "https://vk-oauth-proxy.xtrafrancyz.net/"

# Версия API
VK_API_VERSION = "5.89" 

#Время ожидания ответа
TIME_OUT = 10

# Юзер-агент пользователя
HEADER = {'user-agent': 'VKAndroidApp/5.11.1-2316'}

# Прокси от KateMobile
PROXY_KATE = {'https' : 'https://proxy.katemobile.ru:3752'}

# Мне было день генерировать receipt. 
# По хорошему его можно получить тут(android.clients.google.com/c2dm/register3)
#receipt = "GF54PiFkdbb:APA91bEgyuoeagtS_1avbyY-_6UPRQ5fCJZwbv016qlNY-84iM81bfJgzIc28Tq_U7rvCqWb04nCOlj1M5A2yvZ793cnF8uZHhvKoGeHv9IzmR2ysSkKCn3aAff01IYFEv5nZFf02_hkVfszB2TRJ21XTNaUtvYO9A"
receipt = "JSv5FBbXbY:APA91bF2K9B0eh61f2WaTZvm62GOHon3-vElmVq54ZOL5PHpFkIc85WQUxUH_wae8YEUKkEzLCcUC5V4bTWNNPbjTxgZRvQ-PLONDMZWo_6hwiqhlMM7gIZHM2K2KhvX-9oCcyD1ERw4"

# client_id и client_secret приложений
client_keys = [
  [2274003, 'hHbZxrka2uZ6jB1inYsH'], # 'Android'
  [3140623, 'VeWdmVclDCtn6ihuP1nt'], # 'iPhone' 
  [3682744, 'mY6CDUswIVdJLCD3j15n'], # 'iPad'
  [3697615, 'AlVXZFMUqyrnABp8ncuU'], # 'Windows PC'  
  [2685278, 'lxhD8OD7dMsqtXIm5IUY'], # 'Kate Mobile'
  [5027722, 'Skg1Tn1r2qEbbZIAJMx3'], # 'VK Messenger'
  [4580399, 'wYavpq94flrP3ERHO4qQ'], # 'Snapster (Android)'  
  [2037484, 'gpfDXet2gdGTsvOs7MbL'], # 'Nokia (Symbian)'
  [3502557, 'PEObAuQi6KloPM4T30DV'], # 'Windows Phone'
  [3469984, 'kc8eckM3jrRj8mHWl9zQ'], # 'Lynt'
  [3032107, 'NOmHf1JNKONiIG5zPJUu']  # 'Vika (Blackberry)'
]


def call_oauth(method, param={}, **kwargs):
	"""Выполнение метода VK API"""
	try:
		response = requests.get(method, 
			params=param, headers=HEADER, timeout=TIME_OUT).json()
	except Exception as e:
		raise e

	if 'error' in response:
		if 'need_captcha' == response['error']:
			raise Exception("Error : F*CKING CAPTHA!")
		
		elif 'need_validation' == response['error']:
			if 'ban_info' in response:
				# print(response)
				raise Exception("Error: {error_description}".format(**response))
			
			return "Error: 2fa isn't supported"
		
		else:
			raise Exception("Error : {error_description}".format(**response))

	return response


def call(method, param={}, **kwargs):
	"""Выполнение метода VK API"""
	try:
		response = requests.get(method, 
			params=param, headers=HEADER, timeout=TIME_OUT).json()
	except Exception as e:
		raise e

	if 'error' in response: 
		raise Exception("VKError #{error_code}: {error_msg}".format(**response['error']))

	return response


def autorization(login, password, client_id, client_secret, code, captcha_sid, captcha_key, path):
	param = {
      'grant_type': 'password',
      'client_id': client_id,
      'client_secret': client_secret,
      'username': login,
      'password': password,
      'v': VK_API_VERSION,
      '2fa_supported': '1',
      'code':code,
      'captcha_sid' : captcha_sid,
      'captcha_key' : captcha_key
    }
	
	return call_oauth(path + "token", param)


def refreshToken(access_token, path):
	param = {
		'access_token': access_token,
      	'receipt' : receipt,
      	'v' : VK_API_VERSION
	}

	return call(path + "method/auth.refreshToken", param)


def user_get(access_token, path):
	param = {
		'access_token':access_token,
		'v':VK_API_VERSION
	}

	return call(path + "method/users.get", param)


def get_audio(refresh_token, path):
	param = {
		'access_token':refresh_token,
		'v': VK_API_VERSION
	}

	return call(path + "method/audio.get", param)


def get_catalog(refresh_token, path):
	param = {
      'access_token':refresh_token,
      'v': VK_API_VERSION
    }

	return call(path + "method/audio.getCatalog", param)


def get_playlist(refresh_token, path):
	param = {  
      'access_token':refresh_token,
      'owner_id':'',
      'id':'',
      'need_playlist':1,
      'v': VK_API_VERSION
    }

	return call(path + "method/execute.getPlaylist", param)


def get_music_page(refresh_token, path):
	param = {
      'func_v':3,
      'need_playlists':1,
      'access_token':refresh_token,
      'v': VK_API_VERSION
    }

	return call(path + "method/execute.getMusicPage", param)