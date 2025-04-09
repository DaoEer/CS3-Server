# -*- coding: utf-8 -*-


"""创建初始账号"""
"""
from . import models
import hashlib

srvConf = "default"

users = models.GMUser.objects.using(srvConf)
nameList = [ user.name.lower() for user in users ]
userNameList = [ user.user_name.lower() for user in users ]

name = "admin"
userName = "administrator"
password = "123456"

if name not in nameList and userName not in userNameList:
	r = GMUser.objects.using(srvConf).create(
		name= name,
		user_name = userName,
		password= hashlib.md5( password.encode("utf-8") ).hexdigest(),
		auth = 1,
		auth_query = 1,
	)
"""