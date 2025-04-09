# -*- coding: utf-8 -*-

import Functions
import KBEMath
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import KBEDebug
import Math
import csarithmetic
import math
import csdefine
import MonsterModelNumberCopyPlayer
import ItemTypeEnum
import CalcProperties

class EffectCreateTiShen( EffectSkillBase ):
	"""
	召唤替身
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._scriptID = ""
		self._offsetFront = 0.0
		self._offsetLeft = 0.0
		self._lifeTime = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dictmon
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._scriptID = dictDat["Param1"]
		
		if dictDat["Param2"]:
			offset = dictDat["Param2"].split("|")
			self._offsetFront = float( offset[0] )
			if len(offset) >= 2:
				self._offsetLeft = float( offset[1] )
		if dictDat["Param3"]:
			self._lifeTime = float(dictDat["Param3"])

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		yaw = receiver.direction.z
		position = Math.Vector3( receiver.position )
		if self._offsetFront:
			position.x += self._offsetFront * math.sin( yaw )
			position.z += self._offsetFront * math.cos( yaw )
		if self._offsetLeft:
			position.x += self._offsetLeft * math.sin( yaw - math.pi/2 )
			position.z += self._offsetLeft * math.cos( yaw - math.pi/2 )

		param = {}
		param.update( receiver.getModelDict() )
		param.update( {"ownerID":receiver.id} )
		param.update( {"spawnPos":tuple(Math.Vector3(position))} )
		param.update( {"spawnDir":tuple(Math.Vector3(receiver.direction))} )
		param.update( {"level":receiver.level} )
		param.update( {"uname":receiver.getName()} )
		param.update( {"HP": receiver.HP } )
		param.update( {"MP": receiver.MP } )
		param.update( {"gangQiState":receiver.gangQiState} )
		param.update( {"gangQiValue":receiver.gangQiValue} )
		param.update( {"profession": receiver.getProfession() } )
		param.update( {"jingjieLevel": receiver.jingjieLevel} )
		param.update(CalcProperties.getEffectProperty(receiver))

		if MonsterModelNumberCopyPlayer.datas.get("MonsterExtTiShen",None):
			modelNumber =  MonsterModelNumberCopyPlayer.datas["MonsterExtTiShen"][receiver.getGender()][receiver.getCamp()][receiver.getProfession()]
			param.update( {"modelNumber":modelNumber} )
		else:
			KBEDebug.ERROR_MSG("MonsterModelNumberCopyPlayer config is not has MonsterExtTiShen")
		entity = receiver.createEntityByScriptID( self._scriptID, position, Math.Vector3( receiver.direction ),param )
		if entity:
			entity.delayDestroy(self._lifeTime)


