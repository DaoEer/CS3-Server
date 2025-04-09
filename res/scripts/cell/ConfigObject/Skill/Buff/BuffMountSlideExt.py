# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#common
import csdefine
import csconst
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#cell
import Functions


class BuffMountSlideExt ( BuffHold ):
	""""
	骑上法宝(自动向前滑行，并只能控制左右 CST-9039)
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.delayTime = 0.0					# 延迟移动时间
		self.initSpeed = 0.0					# 初始速度
		self.maxSpeed = 1						# 最大速度
		self.accelerateSpeed = 5.0				# 加速度 m/s2
		self.modelID = ""
		self.InputYawScale = 5.0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if dictDat["Param1"]:
			self.delayTime = float(dictDat["Param1"])
		if dictDat["Param2"]:
			param2 = dictDat["Param2"].split("|")
			if len(param2) >= 2:
				self.initSpeed = float( param2[0] )
				self.maxSpeed = int(float( param2[1] ) * 100)
		if dictDat["Param3"]:
			self.accelerateSpeed = float(dictDat["Param3"])
		self.modelID = dictDat["Param4"]
		if dictDat["Param5"]:
			self.InputYawScale = float(dictDat["Param5"])
		

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
		from ConfigObject.Skill.Buff.BuffMountTalisman import BuffMountTalisman
		from ConfigObject.Skill.Buff.BuffChangeBody import BuffChangeBody
		from ConfigObject.Skill.Buff.BuffChangePosture import BuffChangePosture
		from ConfigObject.Skill.Buff.BuffChangeModelScale import BuffChangeModelScale
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffMountTalisman ) or isinstance( buff, BuffChangeBody ) or isinstance( buff, BuffChangePosture) \
			or isinstance( buff, BuffChangeModelScale):
				receiver.removeBuffByID( buffData.buffID )
		
		BuffHold.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doBegin( self, receiver, buffData )
		
		if self.delayTime:
			receiver.actCounterInc( csdefine.ACTION_FORBID_MOVE )
			receiver.addTimerCallBack( self.delayTime, "actCounterDec", (csdefine.ACTION_FORBID_MOVE,) )
		receiver.setTemp("tempSpeedBase", self.maxSpeed)
		receiver.tempSpeed = self.maxSpeed
		receiver.setSpeed((receiver.tempSpeed * csconst.RunRatio) / 100.0 )
		receiver.allClients.CLIENT_OnMountSlide( self.delayTime, self.initSpeed / self.maxSpeed, self.accelerateSpeed, self.modelID, self.InputYawScale, 1 )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doReload( self, receiver, buffData )
		
		if self.delayTime:
			receiver.actCounterInc( csdefine.ACTION_FORBID_MOVE )
			receiver.addTimerCallBack( self.delayTime, "actCounterDec", (csdefine.ACTION_FORBID_MOVE,) )
		receiver.setTemp("tempSpeedBase", self.maxSpeed)
		receiver.tempSpeed = self.maxSpeed
		receiver.setSpeed((receiver.tempSpeed * csconst.RunRatio) / 100.0 )
		receiver.allClients.CLIENT_OnMountSlide( self.delayTime, self.initSpeed / self.maxSpeed, self.accelerateSpeed, self.modelID, self.InputYawScale, 1 )


	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		
		receiver.allClients.CLIENT_OnDismountSlideExt()
		receiver.removeTemp("tempSpeedBase")
		receiver.tempSpeed = 0
		receiver.setSpeed((receiver.speed * csconst.RunRatio) / 100.0 )

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL:
			receiver.removeBuffByIndex( buffData.index )
			self.doInterrupt( receiver, buffData )

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffHold.onClientActorCreate( self, receiver, buffData, srcEntityID )
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )

		clientEntity.CLIENT_OnMountSlide( 0.0, 0.0, 0.0, self.modelID, self.InputYawScale, 1 )