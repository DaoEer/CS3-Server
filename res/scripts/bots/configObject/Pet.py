# -*- coding: utf-8 -*-

class Pet:
	
	def __init__(self):
		self.uid = ""
		self.scriptID = ""
		
	def init(self,data):
		self.uid = data[ "uid" ]
		self.scriptID = data[ "scriptID" ]