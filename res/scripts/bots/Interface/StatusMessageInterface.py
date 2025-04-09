# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
class StatusMessageInterface:
	
	def __init__(self):
		pass
		
	def statusMessage(self, id, params):
		#KBEDebug.ERROR_MSG("id:%d[%i:%s]" % (self.id, id, params))
		pass
	
	def inquireMessage(self, statusMessageType, statusMessageArg, replyMethod, methodArge ):
		if hasattr(self, methodArge):
			mb = getattr(self, methodArge)
			if hasattr(mb, "replyMessage"):
				func = getattr(mb, "replyMessage")
				func(replyMethod, True)
	
	def ShowCountDown(self, CDTime):
		pass
		
	def ShowExtraTime(self, time):
		pass
		
	def ShowSpaceCopyIntroduction(self, time, bunchName, spaceName, msg):
		pass
	
	def HideStatusMessage( self, p1 ):
		pass
