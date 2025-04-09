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



class EffectAction( EffectSkillBase ):
	"""
	受击表现效果（受击动作、光效、音效）
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._actionID = []
		self._actionBeginTime = []
		self._effectID = ""
		self._soundID = ""
		self._isLocal = False
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		
		# 动作ID1:起始帧时间1|动作ID2:起始帧时间2…（:冒号和|竖号分隔，起始帧时间缺省0秒）
		actionInfos = dictDat["Param1"].split("|")
		for i in actionInfos:
			actionInfo = i.split(":")
			if len( actionInfo ) > 1:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( actionInfo[1] )			
			else:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( "0.0")

		self._effectID = dictDat["Param2"]
		self._soundID = dictDat["Param3"]

		#标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
		if dictDat and dictDat["Param4"]:
			Param4 = dictDat["Param4"].split("|")
			for i in Param4:
				List = i.split(":")
				if List[0] == "IsLocal":	# “IsLocal”代表“只有施法者可见”
					self._isLocal = True

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		casterID = 0
		if caster:
			casterID = caster.id
		receiver.setActionIndex()
		
		if self._isLocal:
			receiver.client.BeHitPlayEffectLocal( casterID, receiver.id, receiver.actionIndex, self._actionID, self._effectID, self._soundID, self._actionBeginTime )
		else:
			receiver.allClients.BeHitPlayEffect(  casterID, receiver.id, receiver.actionIndex, self._actionID, self._effectID, self._soundID, self._actionBeginTime )



