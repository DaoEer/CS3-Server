# -*- coding: utf-8 -*-


"""
usage:
	技能效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#python
import random
#cell
#common
import KBEDebug
import csdefine
import ItemTypeEnum
#data
import Skill.SkillReceiverDefine as SkillReceiverDefine
import Skill.SkillCasterDefine as SkillCasterDefine


class EffectSkillBase:
	"""
	技能效果
	"""
	def __init__( self ):
		self._actForbid 		= csdefine.ACTION_FORBID_NONE
		self._casterActForbid 	= csdefine.ACTION_FORBID_NONE
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		self._actForbid = getattr( csdefine, dictDat["ReceiverActForbid"], csdefine.ACTION_FORBID_NONE )			# 玩法类型限制
		self._casterActForbid = getattr( csdefine, dictDat["CasterActForbid"], csdefine.ACTION_FORBID_NONE )	# 玩法类型限制

	def canEffect( self,skill, caster, receiver ):
		"""
		效果添加检测
		"""
		if receiver.actionForbidSign( self._actForbid ):
			return False
		if caster.actionForbidSign( self._casterActForbid ):
			return False
		#是异常抵抗
		if self.checkExceptionResist( receiver ):
			return False
			
		effectName = self.__class__.__name__
		if effectName in SkillReceiverDefine.Datas:
			flag = receiver.getEntityFlag()
			if flag in SkillReceiverDefine.Datas[effectName]:
				if not SkillReceiverDefine.Datas[effectName][flag]:
					KBEDebug.WARNING_MSG( "receiver(type:%d) in skill effectName(%s) is limit(SkillReceiverDefine)!!"%(flag,effectName) )
				return SkillReceiverDefine.Datas[effectName][flag]

		if effectName in SkillCasterDefine.Datas:
			_flag = caster.getEntityFlag()
			if _flag in SkillCasterDefine.Datas[effectName]:
				if not SkillCasterDefine.Datas[effectName][_flag]:
					KBEDebug.WARNING_MSG( "caster(type:%d) in skill effectName(%s) is limit(SkillCasterDefine)!!"%(_flag,effectName) )
				return SkillCasterDefine.Datas[effectName][_flag]

		return True

	def onReceive( self, skill, caster, receiver ):
		"""
		接受效果
		"""
		pass

	def checkExceptionResist( self, receiver ):
		"""
		是否异常抵抗
		"""
		if self._actForbid == csdefine.ACTION_FORBID_BE_DEPRESS:
			if (ItemTypeEnum.PRECENTRATIO - receiver.depress_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		elif self._actForbid == csdefine.ACTION_FORBID_BE_HIT_BACK:
			if (ItemTypeEnum.PRECENTRATIO - receiver.hitback_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		elif self._actForbid == csdefine.ACTION_FORBID_BE_CONTROL:
			if (ItemTypeEnum.PRECENTRATIO - receiver.control_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		elif self._actForbid == csdefine.ACTION_FORBID_INSANE:
			if (ItemTypeEnum.PRECENTRATIO - receiver.insane_resist) < random.randint(0, ItemTypeEnum.PRECENTRATIO ):
				return True
		return False