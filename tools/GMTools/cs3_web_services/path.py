# -*- coding: utf-8 -*-

"""
init extra path
"""
import os, sys
from common import Functions

def initExtraRootPath():
	"""
	初始化扩展的目录，以加载其它的脚本
	"""
	parentDir = os.path.dirname( os.path.abspath( __file__ ) )
	parentDir = os.path.dirname( parentDir )
	configPath = Functions.getSeverConfigPath()
	if parentDir not in sys.path:
		sys.path.append( parentDir )
	if configPath not in sys.path:
		sys.path.append(configPath)
	
	if sys.hexversion > 0x02070000:
		djp = os.path.join( parentDir, "common/Lib/django_packages/Django-1.10.6" )
		if djp not in sys.path:
			sys.path.append( djp )
	else:
		pass
		#print("You may need to install Python3.4.")
	#try:
	#	import mysql.connector.django
	#except:
	if sys.hexversion > 0x02070000:
		djps = [ os.path.join( parentDir, "common/Lib/mysql_connector_packages/mysql-connector-python-2.1.6" ),
				os.path.join( parentDir, "common/Lib/mysql_connector_packages/mysql-connector-python-2.1.6/lib" ),
				os.path.join( parentDir, "common/Lib/configparser" ),
				os.path.join( parentDir, "common/Lib/" ),
			]
		for djp in djps:
			if djp not in sys.path:
				sys.path.append( djp )
	else:
		pass
		#print("You may need to install python3.4 or later")
	
