# -*- coding: utf-8 -*-


#python

#engine
import KBEngine
#common
import csdefine
import KBEDebug
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
from ConfigObject.Skill.SkillLoader import g_skills
import json


class BuffReSkillBarAndLoginTeleport(BuffHold):
	"""
	替换技能快捷栏，区别于BuffReplaceSkillBar，登录时拥有该buff的玩家会根据skillID读取数据传送，传送后自动移除
	"""
	def __init__( self ):
		BuffHold.__init__(self)
		self._replaceSkillID = ""
		self._teleportSkillID = ""
		self._replaceSkillIDDict = {} #{0:{"QbType":"1",ID:"10000000"}}
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		#Param1：替换技能ID（默认情况下该技能为传送判断技能，如果是传送技能，需要配置Param2）
		#Param2：传送技能ID（如果不配置，Param1则默认为传送判断技能）
		BuffHold.init( self, dictDat )
		self._replaceSkillID = int(dictDat["Param1"])
		self._replaceSkillIDDict[0] = {"QbType":"1","ID":str(self._replaceSkillID)} #这里这样处理的原因：由于这里只允许填一个技能ID，跟BuffReplaceSkillBar不一样，所以先临时处理下，后续策划商量完后再优化
		if dictDat["Param2"].strip():
			self._teleportSkillID = int(dictDat["Param2"])
		
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		from ConfigObject.Skill.Buff.BuffReplaceSkillBar import BuffReplaceSkillBar
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffReplaceSkillBar ) or isinstance( buff, BuffReSkillBarAndLoginTeleport ):		#移除其他同类buff
				receiver.removeBuffByID( buffData.buffID, csdefine.BUFF_END_RESON_BY_REPLACE )
		
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if self._replaceSkillID:
			receiver.client.ReplaceSkillBar( json.dumps(self._replaceSkillIDDict) )
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		if self._replaceSkillID:
			receiver.client.ReplaceSkillBar( json.dumps(self._replaceSkillIDDict) )
		
		if not self._replaceSkillID:
			receiver.removeBuffByID(self._id)
			return
			
		#上线时存在该buff的玩家将传送
		if self._teleportSkillID:		#替换技能为传送技能
			skillInstance = g_skills[self._teleportSkillID]
			if skillInstance:
				(spaceName, position, direction) = self.getSkillHitEffectData(skillInstance, "EffectTeleportSpace")
				receiver.gotoSpaceUE4( spaceName, position, direction )
			else:
				KBEDebug.CRITICAL_MSG( "buff (%i), skill (%i) not exist." % (self._id, self._teleportSkillID) )
		else:		#替换技能为传送判断技能
			skill = g_skills[self._replaceSkillID]
			if skill:
				(questIDs, skillIDs) = self.getSkillHitEffectData(skill, "EffectUseSkillByQuestID")
				if questIDs and skillIDs:
					for i,questID in enumerate(questIDs):
						if receiver.hasQuest( int(questID) ):
							if len(skillIDs)<i:
								break
							skillInstance = g_skills[int(skillIDs[i])]
							if skillInstance:
								if not self.getSkillHitEffectData(skillInstance, "EffectTeleportSpace"):
									break
								(spaceName, position, direction) = self.getSkillHitEffectData(skillInstance, "EffectTeleportSpace")
								if spaceName and (not position is None) and (not direction is None):
									receiver.gotoSpaceUE4( spaceName, position, direction )
							else:
								KBEDebug.CRITICAL_MSG( "buff (%i), skill (%i) not exist." % (self._id, skillInstance.getID()) )
							break
			else:
				KBEDebug.CRITICAL_MSG( "buff (%i), skill (%i) not exist." % (self._id, self._replaceSkillID) )
			
		#从玩家身上移除buff
		receiver.removeBuffByID(self._id)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		if self._replaceSkillID and reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.client.OnReplaceSkillBarEnd()
			
	def getSkillHitEffectData(self, skill, effectType = ""):
		"""
		"""
		from ConfigObject.Skill.Effect.EffectUseSkillByQuestID import EffectUseSkillByQuestID
		from ConfigObject.Skill.Effect.EffectTeleportSpace import EffectTeleportSpace
		hitInstance = skill.getHitInstance()
		for datas in hitInstance.getHitData().values():
			for instance in datas:
				effectList = instance.getEffectList()
				for effect in effectList:
					if effectType == "EffectUseSkillByQuestID" and isinstance(effect, EffectUseSkillByQuestID) :
						return(effect.questIDs, effect.skillIDs)
					elif effectType == "EffectTeleportSpace" and isinstance(effect, EffectTeleportSpace):
						return(effect._spaceName, effect._position, effect._direction)
				else:
					KBEDebug.CRITICAL_MSG( "get skill (%i) hit effet data error, type(%s)." % (skill.getID(), effectType) )
		