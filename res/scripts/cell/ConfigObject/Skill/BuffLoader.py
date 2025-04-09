# -*- coding: utf-8 -*-


"""
usage:
	buff加载类

attribute:
	pass

member function:
	pass

callback:
	pass

"""

import KBEngine
#cell
import ConfigObject.Skill.SkillBase.Skill as Skill
import ConfigObject.Skill.SkillBase.CombatSkill as CombatSkill
#common
import Singleton
import KBEDebug
import LoadModule
import SmartImport
import csconst
import json
import csdefine

def utf16ToJsonCfg( path ):
	allPath = csconst.CONFIG_PATCH + path
	fileObject = open( allPath, encoding="utf16" )
	jsFileObj = json.loads( fileObject.read() )
	fileObject.close()
	return jsFileObj

CLIENT_BUFF_NAME = ["BuffClientHold", "BuffClientLoop", "BuffClientStackable", "BuffClientHitBack", "BuffClientHit"]

class BuffLoader( Singleton.Singleton ):
	def __init__( self ):
		self._buffs = {}

	def __getitem__( self, buffID ):
		return self._buffs.get( buffID, None )
			
	def reloadConfig( self ):
		"""
		技能热更新支持
		"""	
		for id,e in KBEngine.entities.items():					#热更新前，取消掉持续效果
			if not e.isReal():
				continue
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				for buffData in list(e.attrBuffs.values()):
					buff = self[ buffData.buffID ]
					buff.removeHoldEffect( e, buffData )

		self._buffs.clear()
		self.loadAllBuff()

		for id,e in KBEngine.entities.items():				#热更新后，重新加上持续效果
			if not e.isReal():
				continue
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				for buffData in list(e.attrBuffs.values()):
					buff = self[ buffData.buffID ]
					if buff:
						buff.addHoldEffect( e, buffData )
		
		if self._buffs:
			return True
		return False

	def loadAllBuff( self ):
		"""
		加载所有技能
		"""
		buffDatas=[]
		buffDatas = utf16ToJsonCfg("Skill/SkillConfigs/BuffTable.json")
		self.loadBuffConfig(buffDatas)
		
		buffDatas = utf16ToJsonCfg("Skill/SkillConfigs/BuffTableTest.json")
		self.loadBuffConfig(buffDatas, True)
		
	def loadBuffConfig( self, buffDatas, isAllowedRepeat=False ):
		for data in buffDatas:		
			try:
				buffID = int( data["Name"] )
				buffType = data["BuffType"]
				# 客户端buff不需要加载到服务器
				if buffType in CLIENT_BUFF_NAME:
					continue
				buffClass = SmartImport.smartImport( "ConfigObject.Skill.Buff." + buffType + ":" + buffType )
				buffInstance = buffClass()
				buffInstance.init( data )
				self.register( buffID, buffInstance, isAllowedRepeat )
			except:
				KBEDebug.EXCEHOOK_MSG( "load buff %s error" % buffID )

	def register( self, buffID, buff, isAllowedRepeat=False ):
		if not isAllowedRepeat and buffID in self._buffs:
			KBEDebug.ERROR_MSG( "buffID(%d) is repeat use!!"%buffID)
			return
		self._buffs[ buffID ] = buff


g_buffs = BuffLoader()
g_buffs.loadAllBuff()

