# -*- coding: utf-8 -*-
import hashlib, json
from django.conf import settings
from django.http import HttpResponse
from .Define import SERVER_KEY

"""
工具代码
"""

def convert_str_int( val, lmin = 0, lmax = 0x7fffffff ):
	"""
	把字符串转換为整数，并检查有效范围
	@return: 转換后的数值（成功）或None（失败）
	"""
	try:
		r = int( val )
	except ValueError:
		return None
	
	if lmin <= r <= lmax:
		return r
	return None

def makeUriParam(**kws):
	"""
	通过传递进来的参数，生成一条排序过的uri参数
	"""
	vl = list( kws.items() )
	vl.sort( key = lambda x : x[0] )
	sl = [ "%s=%s" % (e[0], e[1]) for e in vl ]
	uri = "&".join( sl )
	return uri

def encryptSign(**kws):
	"""
	把args中的数据与 CS_SECRET 组合生成校验码

	◆ 参数名ASCII码从小到大排序（字典序）； 
	◆ 如果参数的值为空不参与签名； 
	◆ 参数名区分大小写； 
	"""
	arg = {}
	arg.update(kws)
	
	if "key" in arg:
		del arg["key"]

	vs = list(arg.items())
	vs.sort(key = lambda x : x[0])
	rs = [ "%s=%s" % (k, v) for k, v in vs if (v != None and v != "") ]
	rs.append( "key=%s" % settings.CS_SECRET_KEY )
	s = "&".join(rs)
	
	m = hashlib.md5(s.encode())
	d = m.hexdigest()
	return d.upper()
	
def extractParam(**kws):
	"""
	"""
	arg = {}
	arg.update(kws)
	
	params = {}
	for key in SERVER_KEY:
		value = arg.get(key, None)
		if value is None :
			continue
		params[key] = value
	return params

def HttpResponseJson(rawPyData):
	"""
	@param dictData: dict;
	"""
	return HttpResponse( json.dumps( rawPyData ), content_type="application/json" )


