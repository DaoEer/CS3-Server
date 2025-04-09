# -*- coding: utf-8 -*-


"""
usage:
	技能加载类

attribute:
	pass

member function:
	pass

callback:
	pass

"""
import json
import re

#common
import csconst
import csdefine
import Singleton
import KBEDebug
import KBEngine
import LoadModule
import SmartImport


def utf16ToJsonCfg( path ):
	allPath = csconst.CONFIG_PATCH + path
	fileObject = open( allPath, encoding="utf16" )
	jsFileObj = json.loads( fileObject.read() )
	fileObject.close()
	return jsFileObj

class EffectLoader( Singleton.Singleton ):
	def __init__( self ):
		self._effects = {}
		self._holdEffects = {}

	def getEffect( self, effectID ):
		return self._effects.get( effectID, None )
		
	def getHoldEffect( self, effectID ):
		return self._holdEffects.get( effectID, None )
		
	def loadAllEffects( self ):
		"""
		初始化SkillEffectTable技能效果映射表
		"""
		effectDatas = utf16ToJsonCfg("Skill/SkillConfigs/SkillEffectTable.json")
		for effectData in effectDatas:
			if effectData["HitEffectType"] == "EffectAddFixIDEffect":
				KBEDebug.ERROR_MSG( "Effect(%s) script(EffectAddFixIDEffect) can't add EffectAddFixIDEffect again!"%effectData["Name"] )
				continue													# 为防止死循环，EffectAddFixIDEffect不实例化它
			effectInst = self.createEffect( effectData )
			effectID = int( effectData["Name"] )
			self._effects[effectID] = effectInst
			
		effectDatas = utf16ToJsonCfg("Skill/SkillConfigs/SkillHoldEffectTable.json")
		for effectData in effectDatas:
			if effectData["HitEffectType"] == "HoldEffectAddFixIDEffect":
				KBEDebug.ERROR_MSG( "Effect(%s) script(HoldEffectAddFixIDEffect) can't add HoldEffectAddFixIDEffect again!"%effectData["Name"] )
				continue													# 为防止死循环，HoldEffectAddFixIDEffect不实例化它
			effectInst = self.createEffect( effectData )
			effectID = int( effectData["Name"] )
			self._holdEffects[effectID] = effectInst
			
	def reloadConfig( self ):
		"""
		"""
		for id,e in KBEngine.entities.items():					#热更新前，取消掉持续效果
			if not e.isReal():
				continue
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				for effectData in e.holdEffectData:
					if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_FIX_ID:	#这里只重新加载通过固定ID添加的持有效果，因为buff和skill添加的会在BuffLoader和SkillLoader中处理
						effect = self.getHoldEffect( effectData.sourceID )
						effect.onEnd( effectData, e )
		
		self._effects.clear()
		self._holdEffects.clear()
		self.loadAllEffects()
		
		for id,e in KBEngine.entities.items():					#热更新后，重新加上持续效果
			if not e.isReal():
				continue
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				for effectData in e.holdEffectData:
					if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_FIX_ID:	#这里只重新加载通过固定ID添加的持有效果，因为buff和skill添加的会在BuffLoader和SkillLoader中处理
						effect = self.getHoldEffect( effectData.sourceID )
						if effect:
							effect.onBegin( effectData, e )
		
		return True

	def createEffect( self, effectData, Skill = None ):
		"""
		创建一个效果
		"""
		effectType = effectData["HitEffectType"]
		if re.match( "Effect", effectType ) != None:
			effectClass = SmartImport.smartImport( "ConfigObject.Skill.Effect." + effectType + ":" + effectType )
			effectInstance = effectClass()
		elif re.match( "HoldEffect", effectType ) != None:
			effectClass = SmartImport.smartImport( "ConfigObject.Skill.Effect.HoldEffect." + effectType + ":" + effectType )
			effectInstance = effectClass()
		else:
			KBEDebug.CRITICAL_MSG("createEffect error!!")
		effectInstance.init( effectData, Skill )
		return effectInstance


g_effects = EffectLoader()
g_effects.loadAllEffects()

