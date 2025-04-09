# -*- coding: utf-8 -*-


"""
usage:
	Buff持有效果,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine


class HoldEffectCrossFade( HoldEffect ):
	"""
	持有效果：模型、光效等实体支持淡入淡出效果
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.dissolveData = []
		self.starDissolveDegree = 0.0
		self.endDissolveDegree = 0.0
		self.dissolveTime = 0.0
		self.startDelayTime = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self.dissolveColor = dictDat["Param1"]							# 消融的边缘颜色
		self.dissolveDirection = dictDat["Param2"]						# 消融的方向 比如(0,0,1)为纵向从上到下消融
		if len(dictDat["Param3"].strip()):
			self.dissolveData = dictDat["Param3"].strip().split("|")
		if len(self.dissolveData) >= 3:
			self.starDissolveDegree = float(self.dissolveData[0])		# 消融的程度, 0为不消融, 1为完全消融掉
			self.endDissolveDegree = float(self.dissolveData[1])		# 需要到到达消融的程度
			self.dissolveTime = float(self.dissolveData[2])				# 消融时间
		if len(self.dissolveData) >= 4:
			self.startDelayTime = float(self.dissolveData[3]) 			# 延时


	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.allClients.OnDissolve( receiver.id, self.dissolveColor, self.dissolveDirection, self.starDissolveDegree, self.endDissolveDegree, self.dissolveTime, self.startDelayTime )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.EndDissolve( receiver.id, self.endDissolveDegree, self.starDissolveDegree, self.dissolveTime )
		HoldEffect.onEnd( self, effectData, receiver )

