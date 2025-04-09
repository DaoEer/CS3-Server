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


#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import csdefine



class EffectRotateRoleCamera( EffectSkillBase ):
	"""
	偏转玩家摄像机
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.rotateStr = "0|0|0" #分别为旋转的3个值 例如 90|45|30 分别对应X Y Z
		self.armLength = 0.0 #臂长
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.rotateStr = dictDat["Param1"]
		self.armLength = float( dictDat["Param2"] )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			receiver.client.CLIENT_RotateCamera( self.rotateStr,self.armLength )

