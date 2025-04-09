#coding:utf-8

import sys
import KBEDebug
from ObjectScript.ObjectScriptBase import EntityPropertyLoader

class MonsterPropertyLoader( EntityPropertyLoader.EntityPropertyLoader ):
	def __init__( self ):
		EntityPropertyLoader.EntityPropertyLoader.__init__( self )

	def initData( self, configData ):
		if configData is not None:
			EntityPropertyLoader.EntityPropertyLoader.initData( self, configData )
			if 'Profession' in configData:
				self.setEntityProperty("profession",int(configData["Profession"]))

			if 'HPModifyRatio' in configData:
				self.setEntityProperty("hpModifyRatio",float(configData["HPModifyRatio"]))

			if 'DamageModifyRatio' in configData:
				self.setEntityProperty("damageModifyRatio",float(configData["DamageModifyRatio"]))

			if 'Title' in configData:
				self.setEntityProperty("title",configData["Title"])

			if 'Faction' in configData:
				self.setEntityProperty("faction",configData["Faction"])
			
			if 'Camp' in configData:
				self.setEntityProperty("camp",configData["Camp"])

			if 'Uname' in configData:
				self.setEntityProperty("uname",configData["Uname"])

			if 'AttrLevel' in configData:
				self.setEntityProperty("attrLevel",configData["AttrLevel"])

			if 'territoryRange' in configData:
				self.setEntityProperty("territoryRange",int(configData["territoryRange"]))

			if 'viewRange' in configData:
				self.setEntityProperty("viewRange",int(configData["viewRange"]))

			if 'chaseDistance' in configData:
				self.setEntityProperty( "chaseDistance", float(configData["chaseDistance"]) )
				
			if 'InitActionId' in configData:
				self.setEntityProperty("initActionId",configData["InitActionId"])

			if 'DisplayOnClient' in configData:
				self.setEntityProperty("displayOnClient",int(configData["DisplayOnClient"]))
				
		else:
			KBEDebug.WARNING_MSG("MonsterPropertyLoader::initData() configData is none!!!")
