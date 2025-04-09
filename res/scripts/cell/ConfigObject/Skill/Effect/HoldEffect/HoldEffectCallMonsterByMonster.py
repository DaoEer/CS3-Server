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


class HoldEffectCallMonsterByMonster( HoldEffect ):
	"""
	持有效果：召唤monster （在一定范围内的指定monster的位置创建一个callMonster并且销毁原先的monster）
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.scriptIDDict = {}
		self.radius = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@parma dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		scriptIDList = dictDat["Param1"].split("|")
		for scriptStr in scriptIDList:
			key, value = scriptStr.split(":")
			self.scriptIDDict[key] = value
		self.radius = float(dictDat["Param2"])


	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		entities = receiver.entitiesInRangeExt(self.radius, "Monster")
		for entity in entities:
			if entity.scriptID not in self.scriptIDDict.keys():
				continue
			params = {}
			params["owner"] = receiver.base
			params["enableSpace"] = receiver.spaceScriptID
			params["spawnPos"] = tuple(Math.Vector3(entity.position))
			params["spawnDir"] = tuple(Math.Vector3(entity.direction))
			params["level"] = entity.level
		
			receiver.createMonsterExtCall( self.scriptIDDict[entity.scriptID], receiver.getCurrentSpace(), params["spawnPos"], params["spawnDir"], params )
			entity.destroySelf()
		

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		for scriptID in self.scriptIDDict.values():
			receiver.removeCallMonsterByScriptID( scriptID )
		self.scriptIDDict = {}
		HoldEffect.onEnd( self, effectData, receiver )
		




		


