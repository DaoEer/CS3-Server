# -*- coding: utf-8 -*-
#
import Const
import csdefine
import csstatus
import KBEngine
import csstatus
from KBEDebug import *
from ConfigObject.Talk.TalkBase import BaseNPCTalkCondition


class TCLevel(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	满足等级条件
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.needLevel = int( conditionData[ "param1" ] )

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.getLevel() < self.needLevel:
			player.statusMessage(csstatus.LEVEL_CANNOT_SATISFY,self.needLevel)
			return False
		else:
			return True

class TCCamp(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	满足阵营条件
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.needCamp = int( conditionData[ "param1" ] )

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return self.needCamp == player.getFinalCamp() or self.needCamp == csdefine.CMAP_NONE

		
class TCProfession(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	满足职业条件
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.needProfession = int( conditionData[ "param1" ] )

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return self.needProfession == player.getProfession()
		
class TCEnterBunchSpaceBase(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	进副本串条件判断
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.bunchSpace = conditionData["param1"]
		self.needLevel = int( conditionData[ "param2" ] )
		self.maxPlayer = 0
		if conditionData[ "param3" ]:
			self.maxPlayer = int(conditionData[ "param3" ])
		self.activityType = csdefine.ACTIVITY_TYPE_UNKNOWN
		if conditionData["param4"]:
			self.activityType =  int(conditionData["param4"])

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		globalRecord = KBEngine.globalData["BunchSpaceGlobalRecord"]
		if player.isInTeam():
			belongType = csdefine.SPACE_BELONG_TEAM
			spaceKey = str( player.teamMailbox.id )
			if ( self.bunchSpace in globalRecord ) and \
				( belongType in globalRecord[ self.bunchSpace ] ) and \
				( spaceKey in globalRecord[ self.bunchSpace ][ belongType ] ):	# 存在副本
				return True

			if self.maxPlayer:
				if len(player.teamMembers) > self.maxPlayer:
					player.statusMessage(csstatus.SPACE_ENTER_MEM_NUM_MANY,self.maxPlayer ,self.maxPlayer)#队伍人数超过
					return False

			if not player.isTeamCaptain():
				player.statusMessage( csstatus.SPACE_ENTER_NOT_CAPTAIN )
				return False
			
			if player.getLevel() < self.needLevel:
				player.statusMessage( csstatus.SPACE_ENTER_LEVEL_LACK )
				return False
			
			if player.isExceedActivityDegree( self.activityType ):
				player.statusMessage( csstatus.SPACE_ENTER_EXCEED_JOIN_DEGREE )
				return False
			
			# 有人不在范围内
			idList = player.getNotInRangeTeammateDBID( Const.TEAM_ENTER_SPACE_RANGE )
			if len( idList ):
				player.statusMessage( csstatus.SPACE_ENTER_MEM_EXCEED_RANGE )
				return False
			
			inRangeMem = player.getInRangeTeammate( Const.TEAM_ENTER_SPACE_RANGE )
			
			# 有人等级不够
			levelList = []
			exceedList = []
			for mem in inRangeMem:
				if mem.getLevel() < self.needLevel:
					levelList.append( mem.id )
				if mem.isExceedActivityDegree( self.activityType ):
					exceedList.append( mem.id )
			
			if len( levelList ):
				player.statusMessage( csstatus.SPACE_ENTER_MEM_LEVEL_LACK )
				return False
			
			if len( exceedList ):
				player.statusMessage( csstatus.SPACE_ENTER_MEM_EXCEED_JOIN_DEGREE )
				return False
		
		else:
			belongType = csdefine.SPACE_BELONG_PERSON
			spaceKey = str( player.playerDBID )
			if ( self.bunchSpace in globalRecord ) and \
				( belongType in globalRecord[ self.bunchSpace ] ) and \
				( spaceKey in globalRecord[ self.bunchSpace ][ belongType ] ):	# 存在副本
				return True
			
			if player.getLevel() < self.needLevel:
				player.statusMessage( csstatus.SPACE_ENTER_LEVEL_LACK )
				return False
			
			if player.isExceedActivityDegree( self.activityType ):
				player.statusMessage( csstatus.SPACE_ENTER_EXCEED_JOIN_DEGREE )
				return False
		
		return True

class TCEnterPotentailBunch( TCEnterBunchSpaceBase ):
	"""
	进潜能副本串条件
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		TCEnterBunchSpaceBase.__init__(self, conditionData)
		#self.activityType = csdefine.ACTIVITY_TYPE_POTENTAIL_SPACE

class TCEnterChuanChengBunch( TCEnterBunchSpaceBase ):
	"""
	进传承副本串条件
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		TCEnterBunchSpaceBase.__init__(self, conditionData)
		#self.activityType = csdefine.ACTIVITY_TYPE_CHUANCHENG_SPACE

class TCHLDCanOpen(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	能否点击欢乐鼎
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return talkEntity.queryCanTalk()

class TCKillingValueIsZero(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	杀气值小于0（用于监狱传送员）
	"""
	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.killingValue > 0:
			player.statusMessage( csstatus.KILLING_VALUE_TO_MUCH )
			return False
		return True


class TCEnterMagicMazeSpace(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	进幻阵迷宫副本条件判断
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.mainSpace = conditionData["param1"]
		self.needLevel = int( conditionData[ "param2" ] )
		self.maxPlayer = 0
		if conditionData[ "param3" ]:
			self.maxPlayer = int(conditionData[ "param3" ])
		self.activityType = csdefine.ACTIVITY_TYPE_UNKNOWN
		if conditionData["param4"]:
			self.activityType = int(conditionData["param4"])

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		globalRecord = KBEngine.globalData["MagicMazeParentSpaceGlobalRecord"]
		roleGlobalRecord = KBEngine.globalData["MagicMazeParentRecordPlayers"]
		if player.isInTeam():
			belongType = csdefine.SPACE_BELONG_TEAM
			spaceKey = str( player.teamMailbox.id )
			scriptID = ""
			for key,mainScriptID in globalRecord.items():
				if spaceKey == key[1]:
					scriptID = mainScriptID
					break

			if (belongType,spaceKey,scriptID) in roleGlobalRecord:
				if player.playerDBID not in roleGlobalRecord[(belongType,spaceKey,scriptID)]:
					player.statusMessage( csstatus.CANNOT_ENTER_MAGICMAZESPACE_FORBIG_PLAYEAMOUNT,"" )
					return False
				else:
					return True
			
			if self.maxPlayer:
				if len(player.teamMembers) > self.maxPlayer:
					player.statusMessage(csstatus.SPACE_ENTER_MEM_NUM_MANY,self.maxPlayer,self.maxPlayer)#队伍人数超过
					return False

			if not player.isTeamCaptain():
				player.statusMessage( csstatus.SPACE_ENTER_NOT_CAPTAIN )
				return False
			
			if player.getLevel() < self.needLevel:
				player.statusMessage( csstatus.SPACE_ENTER_LEVEL_LACK )
				return False
			
			if player.isExceedActivityDegree( self.activityType ):
				player.statusMessage( csstatus.SPACE_ENTER_EXCEED_JOIN_DEGREE )
				return False
			
			# 有人不在范围内
			idList = player.getNotInRangeTeammateDBID( Const.TEAM_ENTER_SPACE_RANGE )
			if len( idList ):
				player.statusMessage( csstatus.SPACE_ENTER_MEM_EXCEED_RANGE )
				return False
			
			inRangeMem = player.getInRangeTeammate( Const.TEAM_ENTER_SPACE_RANGE )
			
			# 有人等级不够
			levelList = []
			exceedList = []
			for mem in inRangeMem:
				if mem.getLevel() < self.needLevel:
					levelList.append( mem.id )
				if mem.isExceedActivityDegree( self.activityType ):
					exceedList.append( mem.id )
			
			if len( levelList ):
				player.statusMessage( csstatus.SPACE_ENTER_MEM_LEVEL_LACK )
				return False
			
			if len( exceedList ):
				player.statusMessage( csstatus.SPACE_ENTER_MEM_EXCEED_JOIN_DEGREE )
				return False
		
		else:
			belongType = csdefine.SPACE_BELONG_PERSON
			spaceKey = str( player.playerDBID )
			
			if player.getLevel() < self.needLevel:
				player.statusMessage( csstatus.SPACE_ENTER_LEVEL_LACK )
				return False
			
			if player.isExceedActivityDegree( self.activityType ):
				player.statusMessage( csstatus.SPACE_ENTER_EXCEED_JOIN_DEGREE )
				return False
		
		return True

class TCQuestStatus(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	任务状态限制对话选项可见性
	CST-4116
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.questInfoList = []		
		for questInfo in conditionData["param1"].split("|"):
			questInfo = questInfo.split(";")
			if len(questInfo) >= 1:
				questData = {}
				questData["questID"] = int(questInfo[0].split(":")[0])
				questData["questStatus"] = int(questInfo[0].split(":")[1])
				questData["taskInfo"] = []
				if len(questInfo) >= 2:
					taskData = {}
					for i in range(1, len(questInfo)):
						taskInfo = questInfo[i].split(":")
						taskData["taskID"] = int(taskInfo[0])
						taskData["taskStatus"] = int(taskInfo[1])
						questData["taskInfo"].append(taskData)
				self.questInfoList.append(questData)
			else:
				ERROR_MSG("npctalk config error: '%s'" % questInfo)
	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		for questInfo in self.questInfoList:
			if player.queryQuestStatus(questInfo["questID"]) == questInfo["questStatus"]:
				if questInfo["taskInfo"]:
					for taskInfo in questInfo["taskInfo"]:
						if player.queryTaskStatus(questInfo["questID"], taskInfo["taskID"]) != taskInfo["taskStatus"]:
							break
					else:
						return True
				else:
					return True
		player.statusMessage( csstatus.SPACE__NOT_QUEST_CONDITION )
		return False
		
class TCEnterTongSpaceCopy(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	进入帮会副本条件判断（判断进入次数）
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.tongMB is None:
			player.statusMessage( csstatus.TONG_SPACE_COPY_NOT_IN_TONG )
			return False
		if player.isExceedActivityDegree( csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY ):
			player.statusMessage( csstatus.TONG_SPACE_COPY_NOT_ENOUGHT_TIME )
			return False
		return True
		
class TCPlayerHasTong(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	玩家是否有帮会
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.tongMB is None:
			player.statusMessage( csstatus.TONG_SPACE_COPY_NOT_IN_TONG )
			return False
		return True

class TCSignUpBunchZhiZunZhenBa(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	报名至尊争霸
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.minLevel = int(conditionData["param1"])
		self.maxLevel = int(conditionData["param2"])

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.level < self.minLevel or player.level > self.maxLevel:
			player.statusMessage( csstatus.ZHIZUNZHENBA_LIMIT_LEVEL )
			return False
		if player.isInTeam():
			player.statusMessage( csstatus.ZHIZUNZHENBA_SIHN_UP_LIMIT_TEAM )
			return False

		return True

class TCSYDXHasBuff(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	神乐雕像
	玩家有指定buff
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.buffID = int(conditionData["param1"])

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return len(talkEntity.findBuffsByBuffID(self.buffID))

class TCSYDXNotHasBuff(BaseNPCTalkCondition.BaseNPCTalkCondition):
	"""
	神乐雕像
	玩家没有指定buff 多个buff用“|”隔开
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.buffIDs = [int(buffID) for buffID in  conditionData["param1"].strip().split("|")]

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		for buffID in self.buffIDs:
			if len(talkEntity.findBuffsByBuffID(buffID)):
				return False
		return True

class TCPlayerHasItem( BaseNPCTalkCondition.BaseNPCTalkCondition ):
	"""
	玩家是否有某物品
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.itemID = int(conditionData["param1"])

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		itemList = player.getItemInstsByID( self.itemID )
		if len(itemList):
			return True
		return False


class TCPlayerHasTongGrade( BaseNPCTalkCondition.BaseNPCTalkCondition ):
	"""
	玩家是否有某帮会权限
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.grade = int(conditionData["param1"])

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return player.tongHasGrade(self.grade)
		

class TCBelongSide( BaseNPCTalkCondition.BaseNPCTalkCondition ):
	"""
	满足攻守方条件
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.belongSide = int( conditionData[ "param1" ] )

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return self.belongSide == player.getBelongSide()

class TCLbcTaskProcesses( BaseNPCTalkCondition.BaseNPCTalkCondition ):
	"""
	练兵场任务剩余次数大于零
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		if conditionData["param1"]:
			self.messageID = int(conditionData["param1"])
		else:
			self.messageID = 0

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.getLbcTaskProcesses()<=0 and self.messageID:
			player.statusMessage(self.messageID)
		return player.getLbcTaskProcesses()>0
		
class TCMysteriousShop( BaseNPCTalkCondition.BaseNPCTalkCondition ):
	"""
	对话NPC是自身创建出来的（神秘商人）
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return player.playerDBID == talkEntity.ownerDBID
		
class TCIsMatchFastTeam( BaseNPCTalkCondition.BaseNPCTalkCondition ):
	"""
	是否正在快速组队
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass

	def check(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.getIsMatchFastTeam(): 
			player.statusMessage( csstatus.FAST_TEAM_IS_MATCH_FAST_TEAM )
			return False
		return True