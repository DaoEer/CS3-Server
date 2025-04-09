# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyStory import SpaceCopyStory
import KBEDebug
import Math

class SpaceCopyCangGongDian( SpaceCopyStory ):
	"""
	藏功殿
	"""
	def __init__( self ):
		SpaceCopyStory.__init__( self )
		self.monsterIDList = []
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopyStory.initData( self, configData )
		self.scrollScriptID = configData["SpaceData"].get( "scrollScriptID", "" )		# 书卷的SpellBox的ScriptID以及对应的位置
		self.wordScriptID = configData["SpaceData"].get( "wordScriptID", 0 )			# 字的SpellBox的SCriptID
		self.spawnGroup = configData["SpaceData"].get( "spawnGroup", "" )				# 批次
		self.randomBuffIDList = configData["SpaceData"].get( "randomBuffIDList", "" )	# 随机Buff池
		self.promptBuff = configData["SpaceData"].get( "promptBuff", "" )				# 提示BuffID
		self.delayTime = float(configData["SpaceData"].get( "delayTime", 0.0 ))			# 延时销毁场上的entity
		self.nextTime = float(configData["SpaceData"].get( "nextTime", 0.0 ))			# 延时开始下一道答题
		self.wordNum = int(configData["SpaceData"].get( "wordNum" , 0 ))				# 字数
		monsterIDList = configData["SpaceData"].get( "monsterIDList", "" )
		if monsterIDList:
			self.monsterIDList = monsterIDList.split("|")								# 怪物的ScriptID列表
		self.voiceID = configData["SpaceData"].get( "voiceID", "" )						# 回答错误的语音提示
		self.totalQuestionsNum = int(configData["SpaceData"].get( "totalQuestionsNum" , 0 ))				# 送题数
		
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyStory.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.scrollScriptID, self.wordScriptID, self.spawnGroup, self.randomBuffIDList, \
			self.promptBuff, self.voiceID, self.delayTime, self.nextTime, self.wordNum, self.monsterIDList, self.totalQuestionsNum )
