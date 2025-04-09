#coding:utf-8

import sys
import KBEDebug
from ObjectScript.ObjectScriptBase import EntityPropertyLoader

class NPCPropertyLoader( EntityPropertyLoader.EntityPropertyLoader ):
	def __init__( self ):
		EntityPropertyLoader.EntityPropertyLoader.__init__( self )

	def initData( self, configData ):
		if configData is not None:
			EntityPropertyLoader.EntityPropertyLoader.initData( self, configData )
			if 'Title' in configData:
				self.setEntityProperty("title",configData["Title"])

			if 'EntityScript' in configData:
				self.setEntityProperty("entityScript",configData["EntityScript"])

			if 'IsBoss' in configData:
				self.setEntityProperty("isBoss",configData["IsBoss"])
			
			if 'Faction' in configData:
				self.setEntityProperty("faction",configData["Faction"])
			
			if 'Camp' in configData:
				self.setEntityProperty("camp",configData["Camp"])
			
			if 'AttrLevel' in configData:
				self.setEntityProperty("attrLevel",configData["AttrLevel"])

			if 'MerchantType' in configData:
				self.setEntityProperty("merchantType",configData["MerchantType"])

			if 'Uname' in configData:
				self.setEntityProperty("uname",configData["Uname"])
		else:
			KBEDebug.WARNING_MSG("NPCPropertyLoader::initData() configData is none!!!")