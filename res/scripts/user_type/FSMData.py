# -*- coding: utf-8 -*-
import KBEngine

class FSMData(object):
	# FIXED_DICT dict
	def __init__( self ):
		self.fsm = None

	def init(self, fsm_script_id ):
		self.fsm_script_id = fsm_script_id
		if KBEngine.component == "cellapp" and self.fsm_script_id:
			from ConfigObject.MonsterAI.AIBase import AIMgr
			fsm = AIMgr.g_AIMgr.getFSM( self.fsm_script_id )
			self.fsm = fsm

	def getDictFromObj(self, obj):
		return { 'fsm_script_id':obj.fsm_script_id }

	def createObjFromDict(self, proDict):
		obj = self.__class__()
		obj.init( proDict[ 'fsm_script_id' ] )
		return obj

	def isSameType(self, obj):
		if obj is None: return False
		return isinstance(obj, FSMData)

g_inst = FSMData()