# -*- coding: utf-8 -*-
"""
工具代码
"""
import hashlib, math

from xml.dom.minidom import parse as xmlParse

import json, hashlib, os, sys
from django.http import HttpResponse
from django.conf import settings

def HttpResponseJson(rawPyData):
	"""
	@param dictData: dict;
	"""
	return HttpResponse( json.dumps( rawPyData ), content_type="application/json" )

#---------------------------------------------------------------
#json相关
#---------------------------------------------------------------
def loadJsonDataByFile(file):
	"""
	根据文件名加载json文件数据
	"""
	fileObject = open( file, encoding="utf8" )
	fileContent = fileObject.read()
	if fileContent.startswith(u'\ufeff'):
		fileContent = fileContent.encode('utf8')[3:].decode('utf8')
		
	jsFileObj = json.loads( fileContent )
	fileObject.close()
	return jsFileObj
	
#---------------------------------------------------------------
#xml相关
#---------------------------------------------------------------
def loadXmlData(file):
	"""
	加载xml文件数据
	"""
	domTree = xmlParse(file)
	collection = domTree.documentElement
	return collection


#---------------------------------------------------------------
#校验码
#---------------------------------------------------------------
def str_make_md5( s ):
	"""
	编码给定的地址
	"""
	md5 = hashlib.md5(s.encode("utf-8"))
	return md5.hexdigest()

def MD5_Sign(secrt, *args, **kwargs):
	"""
	把args中的数据与 DSHY_SECRET 组合生成校验码

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

def SecretMD5Sign(secret, *args, **kwargs):
	"""
	把args中的数据与 DSHY_SECRET 组合生成校验码

	◆ 参数名ASCII码从小到大排序（字典序）； 
	◆ 如果参数的值为空不参与签名； 
	◆ 参数名区分大小写； 
	"""
	return MD5_Sign(secret, *args, **kwargs)