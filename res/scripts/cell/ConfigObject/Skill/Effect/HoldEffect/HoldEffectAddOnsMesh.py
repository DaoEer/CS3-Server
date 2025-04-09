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


class HoldEffectAddOnsMesh( HoldEffect ):
	"""
	持有效果：抱起幻兽
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._petMeshTableId = ""						# 客户端HoldPetMeshTable表id
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self._petMeshTableId = dictDat["Param1"]

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.allClients.CLIENT_BindDisplayObject(self._petMeshTableId)

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.CLIENT_UnbindDisplayObject(self._petMeshTableId)
		HoldEffect.onEnd( self, effectData, receiver )
		
	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		HoldEffect.onClientActorCreate( self, effectData, receiver, srcEntityID )
		receiver.allClients.CLIENT_BindDisplayObject(self._petMeshTableId)
