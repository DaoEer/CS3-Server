# -*- coding: utf-8 -*-



class RoleTitleInterface:
	"""
	玩家称号接口
	"""
	def __init__( self ):
		"""
		"""
		self.titles = self.cellData["titles"]
		
	def addTitle( self, titleID ):
		"""
		添加称号
		"""
		if titleID in self.titles:
			return
		
		self.titles.append(titleID)
		if self.tongMB: self.tongMB.updatePlayerTitle(self.databaseID, self.getTitles())

	def removeTitle( self, titleID ):
		"""
		移除称号
		"""
		if titleID not in self.titles:
			return
		
		self.titles.remove(titleID)
		if self.tongMB: self.tongMB.updatePlayerTitle(self.databaseID, self.getTitles())
		
	def getTitles(self):
		"""
		"""
		titleStr = ""
		for titleID in self.titles:
			if titleStr:
				titleStr += "|"
			titleStr += str(titleID)
		return titleStr
		
		