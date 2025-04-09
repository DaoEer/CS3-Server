# -*- coding: utf-8 -*-

"""
init extra path
"""
import os, sys

def initExtraRootPath():
	"""
	初始化扩展的目录，以加载其它的脚本
	"""
	parentDir = os.path.dirname( os.path.abspath( __file__ ) )
	parentDir = os.path.dirname( parentDir )
	parentDir = os.path.dirname( parentDir )
	if parentDir not in sys.path:
		sys.path.append( parentDir )
	
	try:
		import django
	except:
		parentDir = os.path.dirname( parentDir )
		if sys.hexversion >= 0x02060000 and sys.hexversion < 0x02070000:
			djp = os.path.join( parentDir, "kbe/tools/server/django_packages/Django-1.6.11" )
			if djp not in sys.path:
				sys.path.append( djp )
		elif sys.hexversion > 0x02070000:
			djps = [ os.path.join( parentDir, "tools/web_services/Common/Lib/django_packages/Django-1.10.6" ),
				os.path.join( parentDir, "tools/web_services/Common/Lib/mysql_connector_packages/mysql-connector-python-2.1.6" ),
				os.path.join( parentDir, "tools/web_services/Common/Lib/mysql_connector_packages/mysql-connector-python-2.1.6/lib" ),
				os.path.join( parentDir, "kbe/tools/server/django_packages/Django-1.8.9" ),
			]
		for djp in djps:
			if djp not in sys.path:
				sys.path.append( djp )
