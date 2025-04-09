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
import csdefine
import KBEDebug

class EffectAddBuffByProfession( EffectSkillBase ):
	"""
	根据职业 添加buff效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._fighterBuffID = {}						# 战士Buff
		self._swordmanBuffID = {}						# 剑客buff
		self._archerBuffID = {}							# 链刃buff
		self._mageBuffID = {}							# 法师buff
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"] == "" or dictDat["Param2"] == "" or dictDat["Param3"] == "" or dictDat["Param4"] == "":
			KBEDebug.CRITICAL_MSG( "skillID: %s Buffer config error!! ( %s )"%( skill._id, str( dictDat ), ) )
			return
		fighterBuffIDs = dictDat["Param1"].split("|")
		self._fighterBuffID[1] =  int(fighterBuffIDs[0])
		self._fighterBuffID[2] = self._fighterBuffID[1]
		if len(fighterBuffIDs) > 1:
			self._fighterBuffID[2] = int(fighterBuffIDs[1])
		swordmanBuffIDs = dictDat["Param2"].split("|")
		self._swordmanBuffID[1] =  int(swordmanBuffIDs[0])
		self._swordmanBuffID[2] = self._swordmanBuffID[1]
		if len(swordmanBuffIDs) > 1:
			self._swordmanBuffID[2] = int(swordmanBuffIDs[1])
		archerBuffIDs = dictDat["Param3"].split("|")
		self._archerBuffID[1] =  int(archerBuffIDs[0])
		self._archerBuffID[2] = self._archerBuffID[1]
		if len(archerBuffIDs) > 1:
			self._archerBuffID[2] = int(archerBuffIDs[1])
		mageBuffIDs = dictDat["Param4"].split("|")
		self._mageBuffID[1] =  int(mageBuffIDs[0])
		self._mageBuffID[2] = self._mageBuffID[1]
		if len(mageBuffIDs) > 1:
			self._mageBuffID[2] = int(mageBuffIDs[1])

	def canEffect( self, skill, caster, receiver  ):
		"""
		效果添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		
		return EffectSkillBase.canEffect( self, skill, caster, receiver )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		profession = receiver.getProfession()
		gender = receiver.getGender()
		buffID = 0
		if profession == csdefine.CLASS_FIGHTER:
			buffID = self._fighterBuffID.get(gender, 0)
		elif profession == csdefine.CLASS_SWORDMAN:
			buffID = self._swordmanBuffID.get(gender, 0)
		elif profession == csdefine.CLASS_ARCHER:
			buffID = self._archerBuffID.get(gender, 0)
		elif profession == csdefine.CLASS_MAGE:
			buffID = self._mageBuffID.get(gender, 0)
		if buffID:
			receiver.addBuff( caster,  buffID)


