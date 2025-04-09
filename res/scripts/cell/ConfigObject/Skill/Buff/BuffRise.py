# -*- coding: utf-8 -*-


"""
usage:
	buff

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#engine
import KBEngine
from ConfigObject.Skill.Buff.BuffHit import BuffHit
import KBEDebug
import Const
import csdefine
import csstatus


class BuffRise( BuffHit ):
	"""
	击飞空中Buff
	"""
	def __init__( self ):
		BuffHit.__init__( self )
		self._actionID = [] 	# 击飞动作
		self._actionBeginTime = []
		self._hitSpeed = 0.0	# 击飞速度
		self._hitTime = 0.0		# 击飞时间
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHit.init( self, dictDat )
		actionInfos = dictDat["Param1"].split("|")
		for i in actionInfos:
			actionInfo = i.split(":")
			if len( actionInfo ) > 1:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( actionInfo[1] )			
			else:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( "0.0")

		if dictDat["Param2"]:
			self._hitSpeed = float(dictDat["Param2"])
		if dictDat["Param3"]:
			self._hitTime = float(dictDat["Param3"])
		if self._hitTime == 0.0:
			KBEDebug.ERROR_MSG("buff(id:%d) Param3 is error!!"%self.getID())

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff目前只适用于玩家
			return BuffHit.addBuffCheck( self, caster, receiver )
		return False

	def receive( self, caster, receiver ):
		"""
		用于给目标施加一个buff，所有的buff的接收都必须通过此接口，
		此接口必须判断接收者是否为realEntity，

		@param   caster: 施法者
		@type    caster: Entity
		@param receiver: 受击者，None表示不存在
		@type  receiver: Entity
		"""
		if not self.addBuffCheck( caster, receiver ):
			return False
		
		#罡气格挡击退
		#if self._actForbid == csdefine.ACTION_FORBID_BE_HIT_BACK and receiver.isInGangQiArmor():	# CST-2229:若玩法设定是“战斗玩法”（ActForbid＝ForbidBeHitback），且目标单位处于“罡气气盈/气短状态”，则拉扯Buff被替换成格挡Buff
		#	receiver.addBuff( caster, Const.BUFF_GANG_QI_BLOCK )
		#	return False
		
		#替换效果
		if self._replaceCondition.valid( caster, receiver, True ) == csstatus.SKILL_GO_ON:
			for effect in self._replaceEffectList:
				if effect.canEffect( self, caster, receiver ):
					effect.onReceive( self, caster, receiver )
			return False
		
		self.receiveSuccess( caster, receiver )
		return True

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		from ConfigObject.Skill.Buff.BuffHitBack import BuffHitBack
		from ConfigObject.Skill.Buff.BuffPull import BuffPull
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffRise ) or isinstance( buff, BuffHitBack ) or isinstance( buff, BuffPull ):		#移除其他同类buff
				receiver.removeBuffByID( buffData.buffID )
		
		BuffHit.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		receiver.effectStateInc( csdefine.EFFECT_STATE_HIT_BACK )
		receiver.setActionIndex()
		buffData.setTempData("actionIndex", receiver.actionIndex)
		receiver.allClients.OnRiseBegin( receiver.actionIndex, self._actionID, self._actionBeginTime, self._hitTime, self._hitSpeed )
		BuffHit.doBegin( self, receiver, buffData )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_HIT_BACK )
		receiver.allClients.OnRiseEnd(buffData.getTempData("actionIndex"),)
		BuffHit.doEnd( self, receiver, buffData,reason )
