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

			if 'WalkSpeed' in configData:
				self.setEntityProperty( "moveSpeed", float(configData["WalkSpeed"]) )

			if 'InitActionId' in configData:
				self.setEntityProperty("initActionId",configData["InitActionId"])

			if 'DisplayOnClient' in configData:
				self.setEntityProperty("displayOnClient",int(configData["DisplayOnClient"])) 

			if 'IconTypeOnMap' in configData:
				self.setEntityProperty("iconTypeOnMap",configData["IconTypeOnMap"])
				
		else:
			KBEDebug.WARNING_MSG("NPCPropertyLoader::initData() configData is none!!!")