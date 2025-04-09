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

import math
#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine



class EffectAttributeWXHJ( EffectSkillBase ):
	"""
	五行画卷属性判定效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._attributeType = ""
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			self._attributeType = dictDat["Param1"]
	
	def canEffect( self, skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if receiver.isState( csdefine.ENTITY_STATE_DEAD ):
			return False
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		resultType = 0
		attributeType = receiver.queryTemp("attributeType", None)
		if attributeType == None:
			receiver.setTemp("attributeType", self._attributeType)
			attributeType = self._attributeType
		elif attributeType == self._attributeType:
			receiver.monsterAISendCommand( receiver.id, "Agree" )
			resultType = 1
			receiver.allClients.CLIENT_OnPictureStopHighlight()
		else:
			receiver.monsterAISendCommand( receiver.id, "Atypism" )
			resultType = 2
			receiver.allClients.CLIENT_OnPictureStopHighlight()
		if attributeType == "jin":
			attributeType = 0
		elif attributeType == "mu":
			attributeType = 1
		elif attributeType == "shui":
			attributeType = 2
		elif attributeType == "huo":
			attributeType = 3
		elif attributeType == "tu":
			attributeType = 4
		receiver.allClients.CLIENT_OnBulletHitPicture( resultType, attributeType )