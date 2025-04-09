# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *
import csstatus

from ConfigObject.Talk.TalkBase import NPCTalkLoader
g_npcTalk = NPCTalkLoader.NPCTalkLoader.instance()


class NPCTalkInterface:
	"""
	NPC对话接口
	"""
	def __init__(self):
		pass

	def talkWith(self, srcEntityID, dlgKey, args):
		"""
		<Exposed method>
		NPC和客户端对话
		@param dlgKey: 对话关键字
		@param args: 对话参数(暂定为字符串型 后面需修改为自定义数据类型)
		"""
		# playerEntity:说话的玩家 type:Entity
		playerEntity = KBEngine.entities.get(srcEntityID)
		if playerEntity is None:
			ERROR_MSG("NPCTalkInterface::talkWith: Can't find entity %i" % srcEntityID)
			return
		
		playerEntity.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id, {"requestType" : csdefine.SKILL_EVENT_ACTION_TYPE_TALK})
		
		npcID = self.scriptID

		dialogManager = g_npcTalk.get(npcID)

		if dialogManager is None:
			playerEntity.statusMessage( csstatus.TALK_CANNOT_FIND_DIALOG,"")
			return

		dialogManager.doTalk( dlgKey, playerEntity, self, args )