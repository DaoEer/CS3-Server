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



class EffectCameraLookAtTarget( EffectSkillBase ):
	"""
	镜头注视效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self.CameraTime = ""
		self.CameraTargetLotation = ""
		self.CameraTargetRotator = ""
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self.CameraTime = dictDat["Param1"]				# 飞行时间|镜头停留时间|镜头飞回时间
		self.CameraTargetLotation = dictDat["Param2"]	# 镜头目标位置偏移量(0|0|0) 单位是cm
		self.CameraTargetRotator = dictDat["Param3"]	# 镜头目标旋转偏移量(0|0|0) 单位是cm

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if caster.getClient():
			caster.client.CameraLookAtTarget(  receiver.id, self.CameraTime, self.CameraTargetLotation, self.CameraTargetRotator )



