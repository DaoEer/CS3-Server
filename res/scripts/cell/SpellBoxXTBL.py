# -*- coding: utf-8 -*-

import SpellBox

class SpellBoxXTBL( SpellBox.SpellBox ):
	"""
	玄天宝录副本 专属SpellBox
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)
		

	def CELL_onClientReady(self, srcEntityID):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		self.setSyncPosClient(srcEntityID)

	def syncPosToServer( self, srcEntityID, clientPos ):
		"""
		<Exposed Method>
		发送位置到服务器
		"""
		pass
