# -*- coding: utf-8 -*-

#common
import KBEDebug
import LoadModule
from Singleton import Singleton

class JsonInstance(Singleton):
	def __init__(self):
		self.teleportStoneDatas = LoadModule.openJsonCfg("TeleportPointData.json")

g_JsonData = JsonInstance()