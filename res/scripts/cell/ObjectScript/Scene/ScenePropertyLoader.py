#coding:utf-8

import sys
import KBEDebug
from ObjectScript.ObjectScriptBase import EntityPropertyLoader

class ScenePropertyLoader( EntityPropertyLoader.EntityPropertyLoader ):
	def __init__( self ):
		EntityPropertyLoader.EntityPropertyLoader.__init__( self )

	def initData( self, configData ):
		if configData is not None:
			EntityPropertyLoader.EntityPropertyLoader.initData( self, configData )
			
		else:
			KBEDebug.WARNING_MSG("ScenePropertyLoader::initData() configData is none!!!")