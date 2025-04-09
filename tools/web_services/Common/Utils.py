# -*- coding: utf-8 -*-
"""
工具代码
"""

import json, hashlib, os, sys
from django.http import HttpResponse
from django.conf import settings

def HttpResponseJson(rawPyData):
	"""
	@param dictData: dict;
	"""
	return HttpResponse( json.dumps( rawPyData ), content_type="application/json" )

def sign_key(secrt, *args, **kwargs):
	"""
	把args中的数据与 CS_SECRET 组合生成校验码

	◆ 参数名ASCII码从小到大排序（字典序）； 
	◆ 如果参数的值为空不参与签名； 
	◆ 参数名区分大小写； 
	"""
	argD = dict(args)
	argD.update(kwargs)
	
	if "sign_type" in argD:
		del argD["sign_type"]

	vs = list(argD.items())
	vs.sort(key = lambda x : x[0])
	rs = [ "%s=%s" % (k, v) for k, v in vs if (v != None and v != "") ]
	rs.append( "key=%s" % secrt )
	s = "&".join(rs)
	
	m = hashlib.md5(s.encode())
	d = m.hexdigest()
	return d.upper()

def CS_Sign(*args, **kwargs):
	"""
	把args中的数据与 CS_SECRET 组合生成校验码

	◆ 参数名ASCII码从小到大排序（字典序）； 
	◆ 如果参数的值为空不参与签名； 
	◆ 参数名区分大小写； 
	"""
	return sign_key(settings.CS_SECRET, *args, **kwargs)
	
"""
转换后python的字典，key为字符串
"""
def loadJsonPathKeyString(configPath):
	path = format('%s/%s' % (settings.BASE_DIR, configPath))
	f = open(path ,encoding="utf8")
	data = json.load(f)
	f.close()
	return data	

def charge_sign(signStr, *args, **kwargs):
	"""
	充值验证码
	"""
	signs = signStr
	for arg in args:
		if isinstance(arg, tuple) and len(arg) >= 2:
			section = "%s=%s" % (arg[0], arg[1])
			signs = signs + section + "&"
	if signs.endswith("&"):
		signs = signs[0:-1]

	signs += settings.CHARGE_SIGN_KEY
	m = hashlib.md5(signs.encode())
	return m.hexdigest()