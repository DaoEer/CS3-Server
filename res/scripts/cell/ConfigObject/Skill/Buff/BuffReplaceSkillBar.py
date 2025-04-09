# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
import json
from ConfigObject.Skill.SkillLoader import g_skills
from ItemFactory import ItemFactoryInst as g_itemFactory

class BuffReplaceSkillBar( BuffHold ):
	"""
	替换技能快捷栏
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._skillIDList = {}  	# {1:{"QbType":"2",ID:"10000000"}, 2:{"QbType":"2",ID:"10000000"}...}
		self.isAddBar = ""	#是否是叠加BUFF
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		
		skillIDStrList =  dictDat["Param1"].split("|") if dictDat["Param1"] else [] #["QbType:Id","","QbType:ID"]
		self.isAddBar =  dictDat["Param2"] if dictDat["Param1"] else ""
		if len( skillIDStrList ) > 9:
			skillIDStrList = skillIDStrList[:9]
			KBEDebug.ERROR_MSG( "buff(%i) cannot replace more skillBar(%i)!"%(self._id, len(skillIDStrList)) )
		for skillIDStr in skillIDStrList:
			if skillIDStr:
				data = {}
				index = skillIDStrList.index(skillIDStr)
				data["QbType"] = skillIDStr.split(":")[0]
				if int(data["QbType"]) == 0:
					continue
				data["ID"] = skillIDStr.split(":")[1]
				if int(data["QbType"]) == csdefine.QB_ITEM_SKILL:
					skillInstance = g_skills[int(data["ID"])]
					if not skillInstance:
						KBEDebug.ERROR_MSG( "buff (%i), SkillTable has not this skill (%s)" % (self._id, data["ID"]) )
				elif int(data["QbType"]) == csdefine.QB_ITEM_KITBAG:
					itemInstance = g_itemFactory.getItemData(int(data["ID"]))
					if not itemInstance:
						KBEDebug.ERROR_MSG( "buff (%i), ItemData has not this item (%s)" % (self._id, data["ID"]) )
				for skillData in self._skillIDList.values():
					if skillData["ID"] == data["ID"]:
						KBEDebug.ERROR_MSG("buff(%i) config cannot has the same ID(%s)"%(self._id, data["ID"]))
				self._skillIDList[index] = data
	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		if not self.isAddBar:
			from ConfigObject.Skill.Buff.BuffReSkillBarAndLoginTeleport import BuffReSkillBarAndLoginTeleport
			for buffData in list(receiver.getAttrBuffs().values()):
				buff = caster.getBuff( buffData.buffID )
				if isinstance( buff, BuffReplaceSkillBar ) or isinstance(buff, BuffReSkillBarAndLoginTeleport):		#移除其他同类buff
					receiver.removeBuffByID( buffData.buffID,  csdefine.BUFF_END_RESON_BY_REPLACE )
		
		BuffHold.receiveSuccess( self, caster, receiver )

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ADDITEM, buffData.index )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_REMOVEITEM, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_ADDITEM, buffData.index )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_REMOVEITEM, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ADDITEM or eventType == csdefine.SKILL_EVENT_REMOVEITEM:
			itemID = pDict.get("itemID",0)
			for index, skillDict in self._skillIDList.items():
				if int(skillDict["ID"]) == itemID:
					receiver.client.RefreshReplaceSkillBar(index)

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if self.isAddBar:
			receiver.client.AddReplaceSkillBar( json.dumps(self._skillIDList) )
		else:	
			receiver.client.ReplaceSkillBar( json.dumps(self._skillIDList) )
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		if self.isAddBar:
			receiver.client.AddReplaceSkillBar( json.dumps(self._skillIDList) )
		else:	
			receiver.client.ReplaceSkillBar( json.dumps(self._skillIDList) )
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.client.OnReplaceSkillBarEnd()