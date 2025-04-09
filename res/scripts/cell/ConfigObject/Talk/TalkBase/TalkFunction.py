# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import csstatus
from KBEDebug import *
from ConfigObject.Talk import TalkActions
from ConfigObject.Talk import TalkConditions
from ConfigObject.Talk import TalkExpenditures

class TalkFunction:
	def __init__(self, configData):
		self._actions = []
		self._conditions = []
		self._expenditures = []
		if configData:
			self.init(configData)

	def init(self, configData):
		for actData in configData["actions"]:
			self._actions.append(getattr(TalkActions, actData["key"])(actData))

		for conData in configData["conditions"]:
			self._conditions.append(getattr(TalkConditions, conData["key"])(conData))

		for expData in configData["expenditures"]:
			self._expenditures.append(getattr(TalkExpenditures, expData["key"])(expData))

	def __isCanDo(self, player, talkEntity, args):
		if player.actionForbidSign( csdefine.ACTION_FORBID_TALK ):
			if player.isState( csdefine.ENTITY_STATE_DEAD ):
				player.statusMessage( csstatus.TALK_FORBID_DEAD_STATE )
			elif player.isState( csdefine.ENTITY_STATE_PEAD ):
				player.statusMessage( csstatus.TALK_FORBID_PEAD_STATE )
			else:
				player.statusMessage( csstatus.TALK_FORBID_BY_STATE )
			return False
		for cond in self._conditions:
			if not cond.check(player, talkEntity, args):
				return False

		for exp in self._expenditures:
			if not exp.check( player, talkEntity, args ):
				return False
		
		return True

	def doAllActions(self, dlgKey, player, talkEntity, args):

		for act in self._actions:

			act.do(dlgKey, player, talkEntity, args)

	def do(self, dlgKey, player, talkEntity, args):
		if self.__isCanDo(player, talkEntity, args):
			self.doAllActions(dlgKey, player, talkEntity, args)

