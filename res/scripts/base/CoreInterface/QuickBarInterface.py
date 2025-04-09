import csdefine
import Const
import KBEDebug
from QuickBarItemData import QuickBarItemData
from RoleBornPropertyLoader import g_roleBornProLoader


class QuickBarInterface:
	def __init__( self ):
		self.__dictQBItems = {0:{}, 1:{}}
		for item in self.qbItems:
			self.__dictQBItems[item.page][item.index] = item

	# ----------------------------------------------------------------
	# public
	# ----------------------------------------------------------------
	def qb_initializeOnCreateRole( self ):
		"""
		角色被创建后初始化快捷栏
		"""
		#技能选项
		skills = g_roleBornProLoader.getQuickBarSkills( self.camp, self.profession, self.gender )
		if not skills:
			return
		self.setQuickBarInitialSkill(0, skills)
		self.setQuickBarInitialSkill(1, skills)

	def initClientData( self ) :
		if hasattr(self, "client") and self.client:
			for item in self.qbItems:
				self.client.CLIENT_OnUpdateQBItem( item.index, item.qbtype, item.id, item.bindType, item.quickID, item.page, str(item.petUid) )

	# ----------------------------------------------------------------
	# called by client
	# ----------------------------------------------------------------
	def BASE_qb_updateItem( self, index, qbtype, id ,bindType, quickID, page, petUid ):
		"""
		<Exposed method>
		修改一个快捷项
		"""
		if not self.validateClientCall():
			return

		if index < 0 : return
		for indexKey,itemValues in self.__dictQBItems[page].items():        # 遍历快捷栏
			if itemValues.qbtype == csdefine.QB_ITEM_SKILL and int(itemValues.id/1000) == int(id/1000):
				self.BASE_qb_removeItem( indexKey, page )
				break
			if (itemValues.qbtype == qbtype and itemValues.id == id):  # 搜索是否有一样得
				self.BASE_qb_removeItem( indexKey, page )                         # 有重复得删掉
				break

		if index in self.__dictQBItems[page].keys():			# 如果快捷格已经存在
			item = self.__dictQBItems[page][index]					# 则提取存在的快捷格（用以更新）
		else :													# 否则
			item = QuickBarItemData()							# 重新创建一个
			item.page = page
			self.qbItems.append( item )							# 添加到快捷列表中
			self.__dictQBItems[page][index] = item
		item.index = index										# 更新快捷格各属性
		item.qbtype = qbtype
		item.bindType = bindType
		item.id = id
		item.quickID = quickID
		item.page = page
		if petUid:
			item.petUid = int(petUid)
		self.client.CLIENT_OnUpdateQBItem(item.index, item.qbtype, item.id, item.bindType, item.quickID, item.page, str(item.petUid))

	def qb_exchangeItem( self, srcIndex, dstIndex, page ) :
		"""
		<Exposed method>
		交换快捷项
		"""
		if not self.validateClientCall():
			return
		if srcIndex == dstIndex : return
		if srcIndex < 0 : return
		if dstIndex < 0 : return
		if srcIndex in self.__dictQBItems[page].keys():
			srcItem = self.__dictQBItems[page].pop( srcIndex )
			self.client.CLIENT_OnRemoveQBItem( page, srcIndex )
			if dstIndex in self.__dictQBItems[page].keys():
				self.__dictQBItems[page][srcIndex] = self.__dictQBItems[page][dstIndex]
				self.__dictQBItems[page][srcIndex].index = srcIndex
				self.client.CLIENT_OnRemoveQBItem( page, dstIndex )  # 客户端有删除重复功能,所以先删除原来的,再移动  CST-4231
				self.client.CLIENT_OnUpdateQBItem( srcIndex, self.__dictQBItems[page][srcIndex].qbtype, self.__dictQBItems[page][srcIndex].id, self.__dictQBItems[page][srcIndex].bindType, self.__dictQBItems[page][srcIndex].quickID, page, str(self.__dictQBItems[page][srcIndex].petUid))	
			self.__dictQBItems[page][dstIndex] = srcItem
			self.__dictQBItems[page][dstIndex].index = dstIndex
			self.client.CLIENT_OnUpdateQBItem(dstIndex, srcItem.qbtype, srcItem.id, srcItem.bindType, srcItem.quickID, page, str(srcItem.petUid))

	def BASE_qb_removeItem( self, index, page ):
		"""
		<Exposed method>
		移除快捷项
		"""
		if not self.validateClientCall():
			return
		if index < 0 : return
		if index in self.__dictQBItems[page].keys():
			item = self.__dictQBItems[page].pop( index )
			self.qbItems.remove( item )
			self.client.CLIENT_OnRemoveQBItem( page, index )

	def setQuickBarInitialSkill(self, page, skills):
		for skillInfo in skills:
			index = skillInfo[0]
			skillID = skillInfo[1]
			quickID = 0
			if len(skillInfo) > 2:
				quickID = skillInfo[2]
			
			qbData = QuickBarItemData()
			qbData.index = index
			qbData.qbtype = csdefine.QB_ITEM_SKILL
			qbData.id = skillID
			qbData.page = page
			qbData.quickID = quickID
			self.__dictQBItems[page][ index ] = qbData
			self.qbItems.append( qbData )

	def removeItemByPetUid(self, petUid):
		"""
		通过幻兽uid移除快捷项
		"""
		removeList = []
		for page, itemValues in self.__dictQBItems.items():
			for index, item in itemValues.items():
				if item.petUid == petUid:
					removeList.append((page, index))
		self.removeItemPagesAndIndexs(removeList)

	def removeItemByPetUidAndSkillID(self, petUid, skillID):
		"""
		通过幻兽uid和skillID移除快捷项
		"""
		removeList = []
		for page, itemValues in self.__dictQBItems.items():
			for index, item in itemValues.items():
				if item.petUid == petUid and item.id == skillID:
					removeList.append((page, index))

		self.removeItemPagesAndIndexs(removeList)

	def removeShenTongItemBySkillID(self, skillID):
		"""
		通过skillID移除神通技能快捷项
		"""
		removeList = []
		for page, itemValues in self.__dictQBItems.items():
			for index, item in itemValues.items():
				if item.qbtype == csdefine.QB_ITEM_SHENTONG_SKILL and item.id == skillID:
					removeList.append((page, index))

		self.removeItemPagesAndIndexs(removeList)

	def removeItemPagesAndIndexs(self, removeList):
		"""
		通过page和index列表一移除快捷项
		"""
		for i in removeList:
			page = i[0]
			index = i[1]
			item = self.__dictQBItems[page].pop( index )
			self.qbItems.remove( item )
			self.client.CLIENT_OnRemoveQBItem( page, index )

	def updateItemByUpgradeSkillID(self, oldSkill, newSkill):
		"""
		升级技能修改快捷栏
		"""
		for item in self.qbItems:
			if int(item.id/1000) == int(newSkill/1000) and item.id < newSkill:
				self.BASE_qb_updateItem( item.index, item.qbtype, newSkill ,item.bindType, item.quickID, item.page, item.petUid )