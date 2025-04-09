# -*- coding: utf-8 -*-
import KBEDebug
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffParachuteLand( BuffHold ):
	"""
	跳伞降落
	"""
	def __init__( self):
		BuffHold.__init__( self )
		self._ModelId = {1:{}, 2:{}}

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if dictDat["Param1"]:
			strList = dictDat["Param1"].split("|")
			for indexI,Modelstr in enumerate(strList):
				self._ModelId[1][indexI+1] = Modelstr
		if dictDat["Param2"]:
			strList = dictDat["Param2"].split("|")
			for indexI,Modelstr in enumerate(strList):
				self._ModelId[2][indexI+1] = Modelstr

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return BuffHold.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffParachuteLand ):
				receiver.removeBuffByID( buffData.buffID )

		BuffHold.receiveSuccess( self, caster, receiver )

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ROLE_PARACHUTE, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_ROLE_PARACHUTE, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ROLE_PARACHUTE:
			receiver.removeBuffByIndex( buffData.index )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		receiver.allClients.CLIENT_ChangeShowPosture(self._ModelId[receiver.getGender()].get(receiver.getProfession(), ""), "", "")
		receiver.client.OnCampYCJMDLeaveBoat()

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		receiver.allClients.CLIENT_ChangeShowPosture(self._ModelId[receiver.getGender()].get(receiver.getProfession(), ""), "", "")
		BuffHold.doReload( self, receiver, buffData )

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		receiver.allClients.CLIENT_ChangeShowPosture( receiver.getActionNumber(), "", "")
		receiver.startFallingHeight = receiver.position.y
		receiver.client.OnCampYCJMDLeaveSkyDiving()
		BuffHold.doEnd( self, receiver, buffData, reason )