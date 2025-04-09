# -*- coding: utf-8 -*-


"""
usage:
	效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""

import KBEngine
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csarithmetic
import KBEMath
import Math
import Const

class EffectJSZZSearch( EffectSkillBase ):
	"""
	金树种子 搜索种植点
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.scriptID = ""
		self.radius = 0.0
		self.totalTime = 0.0
		self.showTime = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.scriptID = dictDat["Param1"]
		self.radius = float(dictDat["Param2"])
		self.totalTime = float( dictDat["Param3"].split("|")[0] )
		self.showTime = float( dictDat["Param3"].split("|")[1] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		position = csarithmetic.getPositionByLink( caster.position, self.radius )
		spaceEntity = caster.getCurrentSpace()
		if spaceEntity:
			plantPos = spaceEntity.getScript().getPlantCenterPos()
			dstPos = Math.Vector3(KBEMath.Unreal2KBEnginePosition( tuple(plantPos) ))
			yaw = csarithmetic.getYawByVector3((dstPos - position))
			caster.createEntityByScriptID( self.scriptID, position, Math.Vector3(0,0,yaw), {})

		if caster.getClient():
			caster.client.CLIENT_ChangeJSZZSearchBtn(self.totalTime,self.showTime)
