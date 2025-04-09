
import KBEDebug
import KBEngine
import ItemFactory
import time
import random
import csdefine

gItemFactory = ItemFactory.ItemFactoryInst

def testAddItem(role):
	"""
	添加物品测试
	"""
	return
	itemID = random.choice([i for i in range(1000, 1006)])
	amount = random.randint(1, 1)
	bindType = random.randint(0,1)
	params = {"id":itemID, "amount":amount, "bindType":bindType }
	KBEDebug.INFO_MSG( "testAddItem-----%s"%str(params) )
	itemInst = gItemFactory.createDynamicItem(itemID, amount, params)
	KBEDebug.INFO_MSG( "addItem[%d]"%itemInst.id )
	role.addItem(itemInst, csdefine.ITEM_ADD_BY_SYS)

def testRemoveItem(role, itemOrder):
	"""
	删除物品测试
	"""
	itemInst = role.getItemInstByOrder(itemOrder)
	if itemInst:
		role.removeItemByAmount(itemInst, itemInst.amount, csdefine.ITEM_REMOVE_BY_DROP)

def testUpdateProperty(role):
	"""
	属性变化测试
	"""
	pass


def clearItems():
	"""
	清空背包
	"""
	role = getRole()
	if not role:	return
	for item in role.itemList:
		testRemoveItem(role, item)

def testClear():
	"""
	清空背包
	"""
	role = getRole()
	if role:
		role.itemOrders = {}
		role.itemList = []

def getRole():
	"""
	获取服务器唯一玩家
	"""
	for entity in KBEngine.entities.values():
		if entity.__class__.__name__ == "Role":
			return entity



