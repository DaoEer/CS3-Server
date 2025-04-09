# -*- coding: utf-8 -*-

import math, time, json
import KST
import Math
import KBEDebug
import csdefine
import RoleBornPropertyConfig
import MonsterModelNumberCopyPlayer
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase

class EffectCreateFenShen( EffectSkillBase ):
	"""
	目标位置创建entity
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._scriptID = ""
		self._offsetFront = 0.0
		self._offsetLeft = 0.0
		self._enableSpace = ""
		self._lifeTime = 0.0
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._scriptID = dictDat["Param1"]
		
		if dictDat["Param2"]:
			offset = dictDat["Param2"].split("|")
			self._offsetFront = float( offset[0] )
			if len(offset) >= 2:
				self._offsetLeft = float( offset[1] )
				
		#不可在指定的地图创建
		if dictDat["Param3"]:
			self._enableSpace = dictDat["Param3"].strip()
			
		if dictDat["Param4"]:
			self._lifeTime = float(dictDat["Param4"])

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		params = {}
		params.update( {"scriptID":self._scriptID} )
		params.update( {"uname":receiver.getName()} )
		params.update( {"enableSpace":self._enableSpace} )
		params.update( {"offsetLeft":str(self._offsetLeft)} )
		params.update( {"offsetFront":str(self._offsetFront)} )
		params.update( {"HP": str(int(receiver.HP/receiver.HP_Max))} )
		params.update( {"MP": str(int(receiver.MP/receiver.MP_Max))} )
		params.update( {"lifeTime":str(int(time.time())+self._lifeTime)} )
		
		attrSkills = list(receiver.quick_attrSkills.values())
		skills = RoleBornPropertyConfig.Datas[str(receiver.getGender())][str(receiver.getCamp())][str(receiver.getProfession())]["skills"]
		if len(skills): 
			if skills[0] not in attrSkills:
				attrSkills.append(skills[0])
			
		params.update( {"attrSkills":json.dumps(attrSkills)} )
		receiver.monsterFenShenData.append(params)
		receiver.callFenShenMonster()
		
		