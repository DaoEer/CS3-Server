# -*- coding: utf-8 -*-

class CasterSkillEvent( dict ):
	def getDictFromObj(self, obj):
		""""""
		# must return original instance
		datas = {}
		datas["events"] = []
		for type, skills in obj.items():
			temp = {}
			temp["eventType"] = type
			temp["skillIDs"] = []
			for id in skills:
				temp["skillIDs"].append(id)
			datas["events"].append( temp )
		return datas

	def createObjFromDict(self, dict):
		Inst = CasterSkillEvent()
		for event in dict["events"]:
			Inst[event["eventType"]] = ( event["skillIDs"] )
			
		return Inst

	def isSameType(self, obj):
		return isinstance(obj, CasterSkillEvent)
		

class ReceiverSkillEvent( dict ):
	def getDictFromObj(self, obj):
		""""""
		# must return original instance
		datas = {}
		datas["events"] = []
		for type, ids in obj.items():
			temp = {}
			temp["eventType"] = type
			temp["skillIDs"] = []
			temp["casterIDs"] = []
			for casterID, skillID in ids:
				temp["casterIDs"].append(casterID)
				temp["skillIDs"].append(skillID)
			datas["events"].append( temp )
		return datas

	def createObjFromDict(self, dict):
		Inst = ReceiverSkillEvent()
		for event in dict["events"]:
			temp = []
			for index, casterID in enumerate( event["casterIDs"] ):
				temp.append( (casterID,event["skillIDs"][index]) )
			Inst[event["eventType"]] = temp
			
		return Inst

	def isSameType(self, obj):
		return isinstance(obj, ReceiverSkillEvent)


class CasterBuffEvent( dict ):
	def getDictFromObj(self, obj):
		""""""
		# must return original instance
		datas = {}
		datas["events"] = []
		for type, ids in obj.items():
			temp = {}
			temp["eventType"] = type
			temp["buffIndexs"] = []
			temp["receiverIDs"] = []
			for receiverID, buffIndex in ids:
				temp["receiverIDs"].append(receiverID)
				temp["buffIndexs"].append(buffIndex)
			datas["events"].append( temp )
		return datas

	def createObjFromDict(self, dict):
		Inst = CasterBuffEvent()
		for event in dict["events"]:
			temp = []
			for index, receiverID in enumerate( event["receiverIDs"] ):
				temp.append( (receiverID,event["buffIndexs"][index]) )
			Inst[event["eventType"]] = temp
			
		return Inst

	def isSameType(self, obj):
		return isinstance(obj, CasterBuffEvent)

class ReceiverBuffEvent( dict ):
	def getDictFromObj(self, obj):
		""""""
		# must return original instance
		datas = {}
		datas["events"] = []
		for type, buffIndexs in obj.items():
			temp = {}
			temp["eventType"] = type
			temp["buffIndexs"] = []
			for id in buffIndexs:
				temp["buffIndexs"].append(id)
			datas["events"].append( temp )
		return datas

	def createObjFromDict(self, dict):
		Inst = ReceiverBuffEvent()
		for event in dict["events"]:
			Inst[event["eventType"]] = ( event["buffIndexs"] )
			
		return Inst

	def isSameType(self, obj):
		return isinstance(obj, ReceiverBuffEvent)

casterInst = CasterSkillEvent()
receiverInst = ReceiverSkillEvent()
casterBuffInst = CasterBuffEvent()
receiverBuffInst = ReceiverBuffEvent()
