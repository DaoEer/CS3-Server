# -*- coding: utf-8 -*-

import csdefine
import Functions
from ConfigObject.Skill.Buff.BuffChangePosture import BuffChangePosture
import Math
import KBEngine


class BuffHoldJinDan( BuffChangePosture ):
	"""
	玩家抱金丹buff（灵岛危机副本）
	
	功能：
	1、头顶显示倒计时（时长取buff时长）；
	2、播放抱金丹表现（参考BuffHoldPet）；
	3、buff时间到使用爆炸技能。
	"""
	def __init__( self ):
		BuffChangePosture.__init__( self )
		self._petMeshTableId = ""						# 客户端HoldPetMeshTable表id
		self._bombSkill = 0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffChangePosture.init( self, dictDat )
		self._petMeshTableId = dictDat["Param2"]
		self._bombSkill = int( dictDat["Param3"] )
	
	def getNewBuffData( self, caster, receiver ):
		"""
		"""
		newBuffData = BuffChangePosture.getNewBuffData( self, caster, receiver )
		if caster and caster.isReal():
			newBuffData.holdTime = float(caster.getRemainLifeTime())	#这里施法者是金丹场景物件（SpellBoxJinDan），获取金丹剩余生命时长，赋值buff时长
			newBuffData.endTime = self.calculateEndTime( newBuffData.holdTime )
			newBuffData.setTempData("JinDanScriptID",caster.scriptID)
		return newBuffData
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffChangePosture.doBegin( self, receiver, buffData )
		buffRemainTime = self.getBuffRemainTime( buffData )
		receiver.setTemp("JinDanBuffID",buffData.buffID)
		receiver.allClients.HoldJinDan( self._petMeshTableId, buffRemainTime, 1.0 )		#抱金丹，金丹头顶显示倒计时，时长等于buff剩余时间，回调时间间隔1.0
		if receiver.client:
			receiver.client.ShowPutDownJinDanBtn()															#显示放下按钮
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffChangePosture.doReload( self, receiver, buffData )
		buffRemainTime = self.getBuffRemainTime( buffData )
		receiver.setTemp("JinDanBuffID",buffData.buffID)
		if receiver.allClients:
			receiver.allClients.HoldJinDan( self._petMeshTableId, buffRemainTime, 1.0 )
		if receiver.client:
			receiver.client.ShowPutDownJinDanBtn()
	
	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffChangePosture.onClientActorCreate( self, receiver, buffData, srcEntityID )
		
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )
		
		buffRemainTime = self.getBuffRemainTime( buffData )
		if clientEntity:
			clientEntity.HoldJinDan( self._petMeshTableId, buffRemainTime, 1.0 )
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffChangePosture.doEnd( self, receiver, buffData, reason )
		receiver.allClients.DownJinDan(self._petMeshTableId)
		receiver.client.HidePutDownJinDanBtn()
		if self.getBuffRemainTime( buffData ) > 0.2 or buffData.holdTime<0:
			JinDanScriptID = buffData.getTempData("JinDanScriptID")
			if JinDanScriptID:
				receiver.createSpellBox( JinDanScriptID, tuple(Math.Vector3(receiver.position)), receiver.direction, {"lifeTime":self.getBuffRemainTime( buffData )} )
		if reason == csdefine.BUFF_END_RESON_BY_TIME_OVER:	#只有时间到了导致的buff结束，才使用爆炸技能
			if self._bombSkill:
				receiver.addTimerCallBack( 0.2, "useSkillToEntity", ( self._bombSkill, receiver.id ) )	#0.2秒后再爆炸，避免头顶倒计时还没消失就爆炸
	