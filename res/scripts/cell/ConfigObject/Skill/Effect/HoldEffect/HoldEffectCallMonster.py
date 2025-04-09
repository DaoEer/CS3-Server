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
import Math
#common
import csdefine
import KBEDebug




class HoldEffectCallMonster( HoldEffect ):
	"""
	持有效果：召唤monster
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.scriptID = ""
		self.enableSpace = []
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@parma dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self.monsterScriptID = dictDat["Param1"]
		if len(dictDat["Param2"].strip()):
			self.enableSpace = dictDat["Param2"].strip().split("|")
		else:
			self.enableSpace = []


	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		params = {}
		params["owner"] = receiver.base
		params["enableSpace"] = list(self.enableSpace)
		params["spawnPos"] = tuple(Math.Vector3(receiver.position))
		params["spawnDir"] = tuple(Math.Vector3(receiver.direction))
		params["level"] = receiver.level
		
		spaceScriptID = receiver.getCurrentSpace().scriptID
		if spaceScriptID not in self.enableSpace and  len(self.enableSpace):
			_params = {}
			_params["monsterScriptID"] = self.monsterScriptID
			_params["enableSpace"] = list(self.enableSpace)
			effectData.setTempData("_params",_params)
			receiver.monsterExtCallParams.append(_params)
			return

		receiver.createMonsterExtCall( self.monsterScriptID, receiver.getCurrentSpace(), receiver.position, receiver.direction, params )
		


	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""

		receiver.removeCallMonsterByScriptID( self.monsterScriptID )
		
		_params = effectData.getTempData("_params")
		if _params and _params in receiver.monsterExtCallParams:
			receiver.monsterExtCallParams.remove(_params)
			
		HoldEffect.onEnd( self, effectData, receiver )




		

