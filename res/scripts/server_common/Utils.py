import hashlib, math


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