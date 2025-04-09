# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
from Singleton import Singleton
from Memoir.Memoir import Datas


class MemoirMgr( Singleton ):
	"""
	创世仙魔录
	"""
	def __init__( self ):
		self._datas = Datas

	def getMemoirData( self, entity, memoirID ):
		"""
		获得该记录数据
		"""
		return self._datas.get(memoirID,None)

	def getAllMemoirDatas( self, entity ):
		"""
		获得entity的所有数据s
		"""
		campData = {}
		camp = entity.getCamp()
		allDataKeys = list(self._datas.keys())
		for key in allDataKeys:
			if int(key.split("-")[0]) == camp:
				campData[key] = self._datas.get(key)
		return campData

	def getNextMemoirID( self, entity ):
		"""
		获得下一个显示的MemoirID
		"""
		memoirIDList = entity.getMemoirIDList()
		allMemoirIDList = list(self.getAllMemoirDatas(entity).keys())
		allMemoirIDList.sort()
		for memoirID in allMemoirIDList:
			if memoirID in memoirIDList:
				continue
			return memoirID
		return None

g_memoirMgr = MemoirMgr()