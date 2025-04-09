# -*- coding: utf-8 -*-
import time
import KBEngine
import KBEDebug

import KST
import KST_Config
from PlayerAI.State.CStateInterface import CStateBase

class CSpace_YXWZ(CStateBase):
	"""
	英雄王座
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		
	def enter(self):
		#开启英雄王座活动
		if "camp_YXWZ" not in KST.tempData:
			KST.tempData["camp_YXWZ"] = True
			self.ai.owner.GMCommand(self.ai.owner, "activity_control", "英雄王座 1")
			#所有玩家退出后，需要手动关闭相应的地图，不然又是在原来的基础上进入。
			KST.tempData["camp_space_need_close"] = True
		
		#报名
		self.ai.owner.GMCommand(self.ai.owner, "YXLMSignUp", "")
		
		#设置下次比赛开启时间为60min后
		KST.tempData["NEXT_CAMP_TIME"] = int(time.time()) + 60 * 60
	
	def leave(self):
		pass
		
		
class CSpace_LMZC(CStateBase):
	"""
	灵脉战场
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		
	def enter(self):
		#开启灵脉战场活动
		if "camp_LMZC" not in KST.tempData:
			KST.tempData["camp_LMZC"] = True
			self.ai.owner.GMCommand(self.ai.owner, "activity_control", "灵脉战场 1")
			#所有玩家退出后，需要手动关闭相应的地图，不然又是在原来的基础上进入。
			KST.tempData["camp_space_need_close"] = True
	
		#报名
		self.ai.owner.GMCommand(self.ai.owner, "LingMaiSignUp", "")
		
		#设置下次比赛开启时间为60min后
		KST.tempData["NEXT_CAMP_TIME"] = int(time.time()) + 60 * 60
		
	def leave(self):
		pass
		
		
class CSpace_JSSLC(CStateBase):
	"""
	晶石狩猎场
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0
		
	def enter(self):
		signFlag = KST.tempData.get("camp_JSSLC_Signup", False)
		if not signFlag:
			#开启报名
			KST.tempData["camp_JSSLC_Signup"] = True
			self.ai.owner.GMCommand(self.ai.owner, "activity_control", "晶石狩猎场报名 1")	
			#重置标志
			KST.tempData["camp_JSSLC_Enter"] = False
			
		self.ai.owner.GMCommand(self.ai.owner, "JSSLCSignUp", "") 	#报名
		
		#180S之后开启活动
		if self.callbackID == 0:
			KBEngine.callback(5 * 60, self.onCallBack)
		
	def leave(self):
		if self.callbackID:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
		
	def onCallBack(self):
		"""
		"""
		self.callbackID = 0
		enterFlag = KST.tempData.get("camp_JSSLC_Enter", False)
		if not enterFlag:
			#开启晶石狩猎场活动
			KST.tempData["camp_JSSLC_Enter"] = True
			self.ai.owner.GMCommand(self.ai.owner, "activity_control", "晶石狩猎场开始 1") 
			#重置标志
			KST.tempData["camp_JSSLC_Signup"] = False
			#所有玩家退出后，需要手动关闭相应的地图，不然又是在原来的基础上进入。
			KST.tempData["camp_space_need_close"] = True
			
		#进入
		self.ai.owner.GMCommand(self.ai.owner, "enterJSSLC", "")
		#设置下次比赛开启时间为60min后
		KST.tempData["NEXT_CAMP_TIME"] = int(time.time()) + 60 * 60 * 24 * 10
		
		
		