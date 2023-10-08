# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import requests
import frappe
import frappe.utils
from frappe.utils.oauth import login_oauth_user
from frappe.utils.password import get_decrypted_password

@frappe.whitelist(allow_guest=True)
def login_via_wecom(code: str, state: str):
	def get_access_token(corpid,corpsecret):
		# 获取access_token
		r = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}')
		return r.json()['access_token']

	def get_userid(code,corpid,corpsecret):
		access_token = get_access_token(corpid,corpsecret)
		info = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/auth/getuserinfo?access_token={access_token}&code={code}').json()
		info.update({'email':info['userid']})
		return info

	providers = frappe.get_all("Social Login Key", fields=["*"])

	out = {}
	for provider in providers:
		out[provider.name] = {
			"client_id": provider.client_id,
			"client_secret": get_decrypted_password("Social Login Key", provider.name, "client_secret"),
		}

	info = get_userid(code,out['wecom']['client_id'],out['wecom']['client_secret'])
	login_oauth_user(info, provider='wecom', state={'token':'1'})
