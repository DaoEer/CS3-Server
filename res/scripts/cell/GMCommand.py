# -*-coding: utf-8 -*-
import Math
import sys, os
import random
import time
import weakref
import math

import KBEngine
import KBEDebug
import KBEMath
from ConfigObject.ConfigLoader import g_configLoader
import ItemFactory
from ObjectScript.ObjectScriptFactory import g_objFactory
from ConfigObject.BunchChildStrategy.StrategyLoader import g_bunchChildStrategyLoader
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader
from ConfigObject.Reward.RewardBase import RewardMgr
from CoreInterface import RoleKitBagInterface
from LoadJsonData import g_JsonData
from ConfigObject.JiYuanCfgLoader import g_jiYuanCfgLoader
import LoadModule
import Settings
from KSTProfile import KST_Profile
import QuestEventDefine
import ItemTypeEnum

import Vector
import csstatus
import csdefine
import Functions
import Const
import re
import csarithmetic

g_gmCommandDict = {}
VALUE_TYPE_REASON = {
	csdefine.REWARD_TYPE_MONEY: csdefine.MONEY_ADD_REASON_USE_GIFT_ITEM,  # 金币奖励
	csdefine.REWARD_TYPE_EXP: csdefine.EXP_ADD_REASON_USE_GIFT_ITEM,  # 经验奖励
	csdefine.REWARD_TYPE_XIUWEI: csdefine.XIUWEI_ADD_REASON_USE_GIFT_ITEM,  # 修为奖励
	csdefine.REWARD_TYPE_POTENTIAL: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,  # 潜能奖励
	csdefine.REWARD_TYPE_BANGGONG: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,  # 帮贡奖励
	csdefine.REWARD_TYPE_TONG_MONEY: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,  # 帮会资金奖励
	csdefine.REWARD_TYPE_FEATS: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,  # 功勋奖励
	csdefine.REWARD_TYPE_MORALE: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,  # 气运奖励
	csdefine.REWARD_TYPE_PSIONIC: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,  # 灵能奖励
	csdefine.REWARD_TYPE_LINGSHI : csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, # 灵石奖励
	csdefine.REWARD_TYPE_XUANSHI : csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, # 玄石奖励
	csdefine.REWARD_TYPE_XIANSHI : csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, # 仙石奖励
	csdefine.REWARD_TYPE_EXPLOIT: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, 	# 军功奖励
}
		
def gmCommandClone( srcEntity, dstEntity, args ):
	"""
	克隆一个entity
	"""
	direction = srcEntity.direction
	position  = srcEntity.position	
	argList = args.split(None)
	if len(argList) < 1:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return
	
	try:
		count = int( argList[1] )
	except:
		count = 1
	if count > Const.CLONE_MONSTER_MAX_COUNT:
		srcEntity.statusMessage( csstatus.GM_CLONE_NEM_ERR )
		return
	
	createDict = {}
	try:
		createDict[ "level" ] = int( argList[2] )
	except:
		pass
	
	if srcEntity.parent:
		createDict[ "parent" ] = srcEntity.parent
		createDict[ "spawnPos" ] = Math.Vector3( srcEntity.localPosition )
	else:
		createDict[ "spawnPos" ] = Math.Vector3( srcEntity.position )
	
	for i in range( 0, count ):
		Obj = None
		if argList[0].startswith("1"):
			Obj = srcEntity.createNPC(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("2"):
			createDict[ "spawnDir" ] = tuple(Math.Vector3(direction))
			Obj = srcEntity.createMonster(argList[0], tuple(Math.Vector3(position)), direction, createDict)	
		elif argList[0].startswith("3"):
			Obj = srcEntity.createTrap(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("4"):
			Obj = srcEntity.createSpellBox(argList[0], tuple(Math.Vector3(position)), direction,  {} )
		else:
			Obj = srcEntity.createEntityByScriptID(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		if not Obj:
			srcEntity.statusMessage( csstatus.GM_SCRIPTID_DONT_EXIST,"")

def gmCommandClone1( srcEntity, dstEntity, args ):
	"""
	指定坐标 克隆一个entity
	4个参数为 scriptID + 坐标
	5个参数为 scriptID + 坐标 + 数量
	7个参数为 scriptID + 坐标 + 朝向
	8个参数为 scriptID + 坐标 + 朝向 + 数量
	"""
	validLen = [4,5,7,8]
	count = 1
	direction = srcEntity.direction
	position  = srcEntity.position	
	argList = args.split(None)
	if len(argList) not in validLen:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return

	_position = Math.Vector3( float( argList[1] ), float( argList[2] ), float( argList[3] ) )
	if _position:
		position = KBEMath.Unreal2KBEnginePosition(_position)
	
	if len(argList) == 5:
		count = int(argList[4])
	if len(argList)>5:
		direction = Math.Vector3( float(argList[4])*3.14/180, float(argList[5])*3.14/180, float(argList[6])*3.14/180 )
	if len(argList) > 7:
		count = int(argList[7])

	if count > Const.CLONE_MONSTER_MAX_COUNT:
		srcEntity.statusMessage( csstatus.GM_CLONE_NEM_ERR )
		return
	
	createDict = {}

	createDict[ "spawnPos" ] = position
	
	for i in range( 0, count ):
		Obj = None
		if argList[0].startswith("1"):
			Obj = srcEntity.createNPC(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("2"):
			createDict[ "spawnDir" ] = tuple(Math.Vector3(direction))
			Obj = srcEntity.createMonster(argList[0], tuple(Math.Vector3(position)), direction, createDict)	
		elif argList[0].startswith("3"):
			Obj = srcEntity.createTrap(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("4"):
			Obj = srcEntity.createSpellBox(argList[0], tuple(Math.Vector3(position)), direction,  {} )
		else:
			Obj = srcEntity.createEntityByScriptID(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		if not Obj:
			srcEntity.statusMessage( csstatus.GM_SCRIPTID_DONT_EXIST,"")


def gmCommandClone2( srcEntity, dstEntity, args ):
	"""
	指定坐标 克隆一个entity
	4个参数为 scriptID + 坐标
	5个参数为 scriptID + 坐标 + 数量
	7个参数为 scriptID + 坐标 + 朝向
	8个参数为 scriptID + 坐标 + 朝向 + 数量
	"""
	validLen = [4,5,7,8]
	count = 1
	direction = srcEntity.direction
	position  = srcEntity.position	
	argList = args.split(None)
	if len(argList) not in validLen:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return

	X, Y, Z = argList[1:4]

	_pos = srcEntity.localPosition

	v1 = Math.Vector3(math.sin(srcEntity.direction.z), 0, math.cos(srcEntity.direction.z))
	v1len = float(X)/100.0
	v2 = Math.Vector3(v1.z, 0, -v1.x)
	v2len = float(Y)/100.0
	v3 = Math.Vector3(0.0, 1.0, 0.0)
	v3len = float(Z)/100.0
	position = _pos + v1*v1len + v2*v2len + v3*v3len

	if len(argList) == 5:
		count = int(argList[4])
	if len(argList)>5:
		direction = Math.Vector3( float(argList[4])*3.14/180 + srcEntity.direction.x, float(argList[5])*3.14/180 +srcEntity.direction.y, float(argList[6])*3.14/180 + srcEntity.direction.z)
	if  len(argList) > 7:
		count = int(argList[7])

	if count > Const.CLONE_MONSTER_MAX_COUNT:
		srcEntity.statusMessage( csstatus.GM_CLONE_NEM_ERR )
		return
	
	createDict = {}
	if srcEntity.parent:
		createDict[ "parent" ] = srcEntity.parent
	createDict[ "spawnPos" ] = position

	for i in range( 0, count ):
		Obj = None
		if argList[0].startswith("1"):
			Obj = srcEntity.createNPC(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("2"):
			createDict[ "spawnDir" ] = tuple(Math.Vector3(direction))
			Obj = srcEntity.createMonster(argList[0], tuple(Math.Vector3(position)), direction, createDict)	
		elif argList[0].startswith("3"):
			Obj = srcEntity.createTrap(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("4"):
			Obj = srcEntity.createSpellBox(argList[0], tuple(Math.Vector3(position)), direction,  {} )
		else:
			Obj = srcEntity.createEntityByScriptID(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		if not Obj:
			srcEntity.statusMessage( csstatus.GM_SCRIPTID_DONT_EXIST,"")

def gmCommandCClone( srcEntity, dstEntity, args ):
	"""
	克隆一个C entity
	"""
	direction = srcEntity.direction
	position  = srcEntity.position	
	argList = args.split(None)
	if len(argList) < 1:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return
	
	try:
		count = int( argList[1] )
	except:
		count = 1
	if count > Const.CLONE_MONSTER_MAX_COUNT:
		srcEntity.statusMessage( csstatus.GM_CLONE_NEM_ERR )
		return
	
	createDict = {}
	try:
		createDict[ "level" ] = int( argList[2] )
	except:
		pass
	
	if srcEntity.parent:
		createDict[ "parent" ] = srcEntity.parent
		createDict[ "spawnPos" ] = Math.Vector3( srcEntity.localPosition )
	else:
		createDict[ "spawnPos" ] = Math.Vector3( srcEntity.position )
	createDict["controlEntityID"] = srcEntity.id
	
	for i in range( 0, count ):
		Obj = None
		if argList[0].startswith("1"):
			Obj = srcEntity.createNPC(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("2"):
			createDict[ "spawnDir" ] = tuple(Math.Vector3(direction))
			Obj = srcEntity.createMonster(argList[0], tuple(Math.Vector3(position)), direction, createDict)	
		elif argList[0].startswith("3"):
			Obj = srcEntity.createTrap(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		elif argList[0].startswith("4"):
			Obj = srcEntity.createSpellBox(argList[0], tuple(Math.Vector3(position)), direction,  {} )
		else:
			Obj = srcEntity.createEntityByScriptID(argList[0], tuple(Math.Vector3(position)), direction,  createDict )
		if not Obj:
			srcEntity.statusMessage( csstatus.GM_SCRIPTID_DONT_EXIST,"")


def gmCommandCreateBaseMonster( srcEntity, dstEntity, args ):
	"""
	克隆带base部分的怪物
	"""
	direction = srcEntity.direction
	position  = srcEntity.position	
	argList = args.split(None)
	if len(argList) < 1:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return
	
	try:
		count = int( argList[1] )
	except:
		count = 1
	if count > Const.CLONE_MONSTER_MAX_COUNT:
		srcEntity.statusMessage( csstatus.GM_CLONE_NEM_ERR )
		return
	try:
		level = int( argList[2] )
	except:
		level = srcEntity.getLevel()

	for i in range( 0, count ):
		obj = srcEntity.base.createBaseMonster( argList[0], srcEntity.getCurrentSpace(), tuple(Math.Vector3(position)), direction , { "spawnPos":tuple(Math.Vector3( position )), "level":level} )
	if not obj:
		srcEntity.statusMessage( csstatus.GM_SCRIPTID_DONT_EXIST,"")


def gmCommandAddItem( srcEntity, dstEntity, args ):
	"""
	添加物品
	"""
	try:
		argList = list(map(int,args.split()))
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"" )
		return
	argLen = len(argList)

	if argLen == 1:
		amount = 1
		bindType = 0
	elif argLen == 2:
		amount = argList[1]
		bindType = 0
	elif argLen == 3:
		amount = argList[1]
		bindType = argList[2]
	else:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/addItem itemID [amount] " ))
		return

	itemID = argList[0]
	itemFactory = ItemFactory.ItemFactoryInst
	itemInst = itemFactory.createDynamicItem( itemID )
	if not itemInst:
		srcEntity.statusMessage( csstatus.GM_ITEMID_DONT_EXIST,"" )
		return
	tempAmount = amount
	while itemInst.getMaxAmount() < tempAmount:
		if itemInst.overlyingType == csdefine.ITEM_OVERLYING_TYPE_STACK:
			tempAmount -= itemInst.getMaxAmount()
			itemInst.amount = itemInst.getMaxAmount()
		else:
			tempAmount -= 1
		if bindType == 1:
			itemInst.setBindType( srcEntity )
		elif bindType == 2:
			itemInst.setBindType( srcEntity, ItemTypeEnum.BIND_NONT_STATE )
		reason = srcEntity.addItem( itemInst, csdefine.ITEM_ADD_BY_GM_COMMAND )
		if reason != csstatus.ITEM_GO_ON:
			dstEntity.statusMessage(reason, "")
		itemInst = itemFactory.createDynamicItem( itemID )
	if itemInst.overlyingType == csdefine.ITEM_OVERLYING_TYPE_STACK:
		itemInst.amount = tempAmount
	KBEDebug.INFO_MSG( "%s(%i): addItem %s(amount:%d)" % (srcEntity.getName(), srcEntity.id, argList[0],itemInst.amount) )
	if bindType == 1:
		itemInst.setBindType( srcEntity )
	elif bindType == 2:
		itemInst.setBindType( srcEntity, ItemTypeEnum.BIND_NONT_STATE )
	reason = srcEntity.addItem( itemInst, csdefine.ITEM_ADD_BY_GM_COMMAND )
	if reason != csstatus.ITEM_GO_ON:
		srcEntity.statusMessage( reason,"" )

def gmCommandAddReward(srcEntity, dstEntity, args):
	"""
	添加奖励给其他玩家
	"""
	try:
		argList = list(map(int, args.split()))
	except ValueError:
		srcEntity.statusMessage(csstatus.GM_ARGS_TYPE_ERROR, "")
		return

	packDictArgs = {}

	argLen = len(argList)

	if argLen == 1:
		rewardID = argList[0]
		packDictArgs["player"] = srcEntity
	elif argLen == 2:
		rewardID = argList[0]
		screenCon = argList[1]
		packDictArgs["screenCon"] = screenCon
	else:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS, str("/addRewardSelf rewardID or /addRewardSelf rewardID screenCon "))
		return

	if not dstEntity or srcEntity == dstEntity or dstEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
		return

	KBEngine.cellAppData["DEBUG_REWARD_FLG"] = 1
	KBEDebug.DEBUG_MSG_FOR_REWARD("Reward test(addReward, rewardID({})) begin!".format(rewardID))
	rewardDatas = RewardMgr.g_rewardMgr.getReward(str(rewardID), packDictArgs)
	KBEDebug.DEBUG_MSG_FOR_REWARD("Final reward set is:")
	for data in rewardDatas:
		KBEDebug.DEBUG_MSG_FOR_REWARD(str(data))
	KBEDebug.DEBUG_MSG_FOR_REWARD("Reward test(addReward, rewardID({})) over!".format(rewardID))
	KBEDebug.DEBUG_MSG_FOR_REWARD("<*************************************************>")
	for data in rewardDatas:
		type = data["type"]
		if type == csdefine.REWARD_TYPE_NOTHING:
			continue
		elif type == csdefine.REWARD_TYPE_ITEM:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(data["goodsid"], data["amount"])
			if not itemInst:
				dstEntity.statusMessage(csstatus.GM_ITEMID_DONT_EXIST, "")
				return

			reason = dstEntity.addItem(itemInst, csdefine.ITEM_ADD_BY_GM_COMMAND)
			if reason != csstatus.ITEM_GO_ON:
				dstEntity.statusMessage(reason, "")
		elif type == csdefine.REWARD_TYPE_TITLE:  # 增加称号选项
			RewardMgr.g_rewardMgr.doReward(data, dstEntity.id, "title")
		else:
			RewardMgr.g_rewardMgr.doReward(data, dstEntity.id, VALUE_TYPE_REASON[data["type"]])


def gmCommandAddRewardSelf(srcEntity, dstEntity, args):
	"""
	添加奖励给自己
	"""
	try:
		argList = list(map(int, args.split()))
	except ValueError:
		srcEntity.statusMessage(csstatus.GM_ARGS_TYPE_ERROR, "")
		return

	packDictArgs = {}

	argLen = len(argList)

	if argLen == 1:
		rewardID = argList[0]
		packDictArgs["player"] = srcEntity
	elif argLen == 2:
		rewardID = argList[0]
		screenCon = argList[1]
		packDictArgs["screenCon"] = screenCon
	else:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS, str("/addRewardSelf rewardID or /addRewardSelf rewardID screenCon"))
		return

	if not srcEntity:
		return

	KBEngine.cellAppData["DEBUG_REWARD_FLG"] = 1
	KBEDebug.DEBUG_MSG_FOR_REWARD("Reward test(addRewardSelf, rewardID({})) begin!".format(rewardID))
	rewardDatas = RewardMgr.g_rewardMgr.getReward(str(rewardID), packDictArgs)
	KBEDebug.DEBUG_MSG_FOR_REWARD("Final reward set is:")
	for data in rewardDatas:
		KBEDebug.DEBUG_MSG_FOR_REWARD(str(data))
	KBEDebug.DEBUG_MSG_FOR_REWARD("Reward test(addRewardSelf, rewardID({})) over!".format(rewardID))
	KBEDebug.DEBUG_MSG_FOR_REWARD("<*************************************************>")
	for data in rewardDatas:
		type = data["type"]
		if type == csdefine.REWARD_TYPE_NOTHING:
			continue
		elif type == csdefine.REWARD_TYPE_ITEM:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(data["goodsid"], data["amount"])
			if not itemInst:
				srcEntity.statusMessage(csstatus.GM_ITEMID_DONT_EXIST, "")
				return

			reason = srcEntity.addItem(itemInst, csdefine.ITEM_ADD_BY_GM_COMMAND)
			if reason != csstatus.ITEM_GO_ON:
				srcEntity.statusMessage(reason, "")
		elif type == csdefine.REWARD_TYPE_TITLE:  # 增加称号选项
			RewardMgr.g_rewardMgr.doReward(data, srcEntity.id, "title")
		else:
			RewardMgr.g_rewardMgr.doReward(data, srcEntity.id, VALUE_TYPE_REASON[data["type"]])

def gmCommandGotoSpace( srcEntity, dstEntity, args ):
	"""
	地图传送
	"""
	argList = args.split(None)
	argLen = len(argList)
	try:
		if argLen == 7:																										#已输入spacename、position、direction
			position  = KBEMath.Unreal2KBEnginePosition((float(argList[1]) , float(argList[2]) , float(argList[3])))
			direction = KBEMath.Unreal2KBEngineDirection((float(argList[4]), float(argList[5]), float(argList[6])))
		elif argLen == 4:																									#只输入spacename，position
			position  = KBEMath.Unreal2KBEnginePosition((float(argList[1]) , float(argList[2]) , float(argList[3])))
			direction = (0.0,0.0,0.0)
		elif argLen == 1:																									#只输入spacename，position、direction默认
			direction = (0.0,0.0,0.0)
			position  = (0.0,0.0,0.0)
		else:
			srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/goto spaceKey [px py pz] [dx dy dz]"))													#没有输入任何参数
			return
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return

	#if srcEntity.getCurrentSpaceClassName() == argList[0]:
	#	srcEntity.position = position
	#	return
	#ERROR_MSG("position=%s,direction=%s"%(position,direction))
	spaceObj = g_objFactory.getSpaceObject( argList[0] )
	if not spaceObj:
		srcEntity.statusMessage( csstatus.GM_ARGS_SPACE_VALUE_ERROR,"")
		return
	if hasattr( spaceObj, "isBunchChildSpace" ) and spaceObj.isBunchChildSpace() and srcEntity.spaceScriptID != argList[0]:	# 是副本串子副本且不是同地图传送
		srcEntity.statusMessage( csstatus.GM_GOTO_BUNCHSPACE,"")
		return
	KBEDebug.INFO_MSG( "%s(%i): goto %s" % (srcEntity.getName(), srcEntity.id, argList[0]) )
	srcEntity.gotoSpace( argList[0], tuple(Math.Vector3(position)), direction )

def gmCommandGotoPoint( srcEntity, dstEntity, args ):
	"""
	传送NPCPointDatasTable中点的位置。
	"""
	#args格式：sapceScriptID|X=213 Y=456 Z=789
	argList = args.strip().split("|")

	try:																					
		spaceScriptID = argList[0]
		vector = argList[1].split()
		x,y,z = [float(v.split("=")[1]) for v in vector ]
		position = KBEMath.Unreal2KBEnginePosition((x,y,z))
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return

	spaceObj = g_objFactory.getSpaceObject( argList[0] )
	if not spaceObj:
		srcEntity.statusMessage( csstatus.GM_ARGS_SPACE_VALUE_ERROR,"")
		return
	if hasattr( spaceObj, "isBunchChildSpace" ) and spaceObj.isBunchChildSpace() and srcEntity.spaceScriptID != argList[0]:	# 是副本串子副本且不是同地图传送
		srcEntity.statusMessage( csstatus.GM_GOTO_BUNCHSPACE,"")
		return
	KBEDebug.INFO_MSG( "%s(%i): goto %s" % (srcEntity.getName(), srcEntity.id, argList[0]) )
	direction = (0.0,0.0,0.0)
	srcEntity.gotoSpace( argList[0], tuple(Math.Vector3(position)), (direction) )

def gmCommandGotoSpaceUseServerPos( srcEntity, dstEntity, args ):
	"""
	地图传送，使用服务器坐标
	"""
	argList = args.split(None)
	argLen = len(argList)
	try:
		if argLen == 7:																										#已输入npcID、position、direction
			position  = (float(argList[1]) , float(argList[2]) , float(argList[3]))
			direction = (float(argList[4]), float(argList[5]), float(argList[6]))
		elif argLen == 4:																									#只输入npcID，position
			position  = (float(argList[1]) , float(argList[2]) , float(argList[3]))
			direction = (0.0,0.0,0.0)
		elif argLen == 1:																									#只输入npcID，position、direction默认
			direction = (0.0,0.0,0.0)
			position  = (0.0,0.0,0.0)
		else:
			srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/GOTO spaceKey [px py pz] [dx dy dz]"))													#没有输入任何参数
			return
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return

	#if srcEntity.getCurrentSpaceClassName() == argList[0]:
	#	srcEntity.position = position
	#	return
	#ERROR_MSG("position=%s,direction=%s"%(position,direction))
	spaceObj = g_objFactory.getSpaceObject( argList[0] )
	if not spaceObj:
		srcEntity.statusMessage( csstatus.GM_ARGS_SPACE_VALUE_ERROR,"")
		return
	if hasattr( spaceObj, "isBunchChildSpace" ) and spaceObj.isBunchChildSpace() and srcEntity.spaceScriptID != argList[0]:	# 是副本串子副本且不是同地图传送
		srcEntity.statusMessage( csstatus.GM_GOTO_BUNCHSPACE,"")
		return
	KBEDebug.INFO_MSG( "%s(%i): goto %s" % (srcEntity.getName(), srcEntity.id, argList[0]) )
	srcEntity.gotoSpace( argList[0], tuple(Math.Vector3(position)), direction )

def gmCommandEnterPlane( srcEntity, dstEntity, args ):
	"""
	进（出）位面
	"""
	argList = args.split(None)
	if len(argList) == 0:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/enterPlane spaceKey"))	
		return
	spaceObj = g_objFactory.getSpaceObject( argList[0] )
	if not spaceObj:
		srcEntity.statusMessage( csstatus.GM_ARGS_SPACE_VALUE_ERROR,"")
		return
	curSpaceScript = srcEntity.getCurrentSpace().scriptID
	
	from ObjectScript.Space.SpacePlane import SpacePlane
	if isinstance( spaceObj, SpacePlane ):
		if argList[0].split("_Planes")[0] == curSpaceScript:
			KBEDebug.INFO_MSG( "%s(%i): gotoSpacePlane %s" % (srcEntity.getName(), srcEntity.id, argList[0]) )
			srcEntity.gotoSpacePlane( argList[0] )
		else:
			srcEntity.statusMessage( csstatus.GM_CANT_ENTER_TARGET_SPACE, "" )
	else:
		if curSpaceScript.split("_Planes")[0] == argList[0]:
			KBEDebug.INFO_MSG( "%s(%i): leaveSpacePlane %s" % (srcEntity.getName(), srcEntity.id, argList[0]) )
			srcEntity.leaveSpacePlane( argList[0] )
		else:
			srcEntity.statusMessage( csstatus.GM_CANT_ENTER_TARGET_SPACE, "" )
	
def gmCommandGotoPlane( srcEntity, dstEntity, args ):
	"""
	传送到位面入口
	"""
	argList = args.split(None)
	if len(argList) == 0:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/enterPlane spaceKey"))	
		return
	spaceObj = g_objFactory.getSpaceObject( argList[0] )
	if not spaceObj:
		srcEntity.statusMessage( csstatus.GM_ARGS_SPACE_VALUE_ERROR,"")
		return
	
	enterSpace,enterPos,enterDir = spaceObj.getReviveToExitInfo( srcEntity )
	srcEntity.gotoSpaceUseArg( enterSpace, enterPos, enterDir, {} )

def gmCommandGotoBunchSpace( srcEntity, dstEntity, args ):
	"""
	进副本串，可指定开始子地图
	"""
	argList = args.split(None)
	argLen = len(argList)
	if argLen == 0:
		return
	bunchSpace = argList[0]
	bunchObj = g_objFactory.getBunchSpaceObject( bunchSpace )
	destSpace = g_bunchChildStrategyLoader.getFirstSpace( bunchObj, srcEntity )	#CST-1938 按策略随机第一个子副本
	
	if srcEntity.isInTeam():
		globalRecord = KBEngine.globalData["BunchSpaceGlobalRecord"]
		belongType = csdefine.SPACE_BELONG_TEAM
		spaceKey = str( srcEntity.teamMailbox.id )

		if ( bunchSpace in globalRecord ) and \
			( belongType in globalRecord[ bunchSpace ] ) and \
			( spaceKey in globalRecord[ bunchSpace ][ belongType ] ):	# 存在副本
			if argLen > 1:
				srcEntity.gotoBunchSpace( bunchSpace, { "packBelongType": belongType, "bunchLevel": srcEntity.getLevel(), "destChildSpace": argList[1] } )
			else:
				srcEntity.gotoBunchSpace( bunchSpace, { "packBelongType": belongType, "bunchLevel": srcEntity.getLevel(), "destChildSpace": destSpace } )
		else:
			if not srcEntity.isTeamCaptain():	# 副本不存在的情况下，这里一定要队长执行指令
				KBEDebug.ERROR_MSG("Player is not captain!", srcEntity.id)
				return
			teammates = []
			for memMB in srcEntity.getAllTeamMemberMB():
				if memMB.id != srcEntity.id:
					teammates.append( memMB )
			if argLen > 1:
				srcEntity.gotoBunchSpace( bunchSpace, { "packBelongType": belongType, "bunchLevel": srcEntity.getLevel(), "destChildSpace": argList[1], "teammates": teammates } )
			else:
				srcEntity.gotoBunchSpace( bunchSpace, { "packBelongType": belongType, "bunchLevel": srcEntity.getLevel(), "destChildSpace": destSpace, "teammates": teammates } )

	else:
		belongType = csdefine.SPACE_BELONG_PERSON
		if argLen > 1:
			srcEntity.gotoBunchSpace( bunchSpace, { "packBelongType": belongType, "bunchLevel": srcEntity.getLevel(), "destChildSpace": argList[1] } )
		else:
			srcEntity.gotoBunchSpace( bunchSpace, { "packBelongType": belongType, "bunchLevel": srcEntity.getLevel(), "destChildSpace": destSpace } )
	
	KBEDebug.INFO_MSG( "%s(%i): gotoBunch %s" % (srcEntity.getName(), srcEntity.id, args) )

def gmCommandSetNextSpace( srcEntity, dstEntity, args ):
	"""
	副本串，设置下一个子副本
	"""
	argList = args.split(None)
	spaceEntity = srcEntity.getCurrentSpace()
	if spaceEntity:
		spaceEntity.remoteScriptCall( "spaceBunch_setNextSpaceGM", ( argList[0], ) )

def gmCommandClearBunchRecord( srcEntity, dstEntity, args ):
	"""
	清除副本串参与记录
	"""
	srcEntity.clearActivityDegree( csdefine.ACTIVITY_TYPE_POTENTAIL_SPACE )
	srcEntity.clearActivityDegree( csdefine.ACTIVITY_TYPE_CHUANCHENG_SPACE )
	srcEntity.clearActivityDegree( csdefine.ACTIVITY_TYPE_MAGIC_MAZE_SPACE )

def gmCommandSetAttr( srcEntity, dstEntity, args ):
	"""
	设置entity的属性
	"""
	argList = args.split()
	if len(argList)!=2:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/set_attr attrkey value"))
		return
	KBEDebug.INFO_MSG( "%s(%i): set_attr %s" % (srcEntity.getName(), srcEntity.id, args) )
	if argList[0] == "level":
		gmCommandSetLevel( srcEntity, dstEntity, argList[1] )
		return
	setattr( dstEntity, argList[0], eval( argList[1] ) )

def gmCommandQueryAttr( srcEntity, dstEntity, args ):
	"""
	查询entity的属性
	"""
	argList = args.split()
	if len(argList)!=1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/query_attr attrkey"))
		return
	if not hasattr( dstEntity, argList[0] ):
		srcEntity.statusMessage( csstatus.GM_ATTR_NOT_EXIST)
		return
	result = getattr( dstEntity, argList[0] )
	if argList[0] == "position" :
		position = KBEMath.KBEngine2UnrealPosition((round(result[0],2),round(result[1],2),round(result[2],2)))
		result = str(position[0]) + " " + str(position[1]) + " " + str(position[2])
	elif argList[0] == "direction":
		direction = KBEMath.KBEngine2UnrealDirection((round(result[0],2),round(result[1],2),round(result[2],2)))
		result = str(direction[0]) + " " + str(direction[1]) + " " + str(direction[2])
	else:		#去掉字典{}符号，因为客户端的参数使用{}转义，如果参数中含{}字符串则不成功
		if type( result ) is list:
			resultStr = ""
			for subResult in result:
				reSubResult = re.search( "(?<=\{).+?(?=\})", str(subResult) )
				if reSubResult:		#列表成员为字典
					resultStr += "(%s)"%reSubResult.group()
			if len( resultStr ) > 0:
				result = resultStr
		else:
			reResult = re.search( "(?<=\{).+?(?=\})", str(result) )
			if reResult:
				result = "(%s)"%reResult.group()
	srcEntity.statusMessage( csstatus.GM_QUERY_RESULT,str(result))

def gmCommandReviveOnOrigin( srcEntity, dstEntity, args ):
	"""
	原地复活
	"""
	KBEDebug.INFO_MSG( "%s(%i): revive %s" % ( srcEntity.getName(), srcEntity.id, srcEntity.getName()) )
	srcEntity.reviveOnOrigin()

def gmCommandDropBox( srcEntity, dstEntity, args ):
	"""
	掉落箱子
	"""
	try:
		argList = list(map(int,args.split()))
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"" )
		return
	argsLen = len( argList )
	if argsLen == 1:
		amount = 1
	elif argsLen == 2:
		amount = int( argList[1] )
	else:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/dropBox itemID [amount]"))
		return
	itemID = argList[0]
	itemFactory = ItemFactory.ItemFactory()
	itemInst = itemFactory.createDynamicItem( itemID, amount )
	if  not itemInst:
		srcEntity.statusMessage( csstatus.GM_DROP_BOX_ITEM_LIST_NONE )
		return
	position = srcEntity.position
	position[0] += 5.0
	direction = srcEntity.direction
	
	KBEDebug.INFO_MSG( "%s(%i): dropBox %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	dropBox = srcEntity.createEntityNear( "DropBox", tuple(Math.Vector3(position)), direction, {"modelNumber":"SM_DropBox", "modelScale":0.2, "ownershipIDs":[srcEntity.playerDBID], "allocationItems": {srcEntity.playerDBID: [itemInst]}, "notAllocationItems": [], "allocation": 1} )
	dropBox.parent = srcEntity.parent
	if not dropBox:
		srcEntity.statusMessage( csstatus.GM_DROP_BOX_FAIL )
		return

def gmCommandSpell( srcEntity, dstEntity, args ):
	"""
	玩家向目标施法
	"""
	argList = args.split()
	try:
		skillID = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/spell skillID"))
		return
		
	skill = srcEntity.getSkill( skillID )
	if skill is None:
		KBEDebug.EXCEHOOK_MSG( "%i: skill %i not exist." % ( srcEntity.id, skillID ) )
		srcEntity.statusMessage( csstatus.SKILL_NOT_EXIST, "")
		return
	if dstEntity:
		if not dstEntity.isCombatEntity():
			srcEntity.statusMessage( csstatus.SKILL_CAST_ENTITY_ONLY )
			return
	targetID = dstEntity.id
	srcEntity.useSkillToEntityGM( srcEntity, skillID, targetID )

def gmCommandSpellSelf( srcEntity, dstEntity, args ):
	"""
	目标向玩家施法
	"""
	argList = args.split()
	try:
		skillID = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/spellSelf skillID"))
		return
	if not dstEntity:
		dstEntity = srcEntity
	if not dstEntity.isCombatEntity():
		srcEntity.statusMessage( csstatus.SKILL_CAST_ENTITY_ONLY )
		return
		
	skill = srcEntity.getSkill( skillID )
	dstEntity.useSkillToEntityGM( srcEntity, skillID, srcEntity.id )

def gmCommandSpellItself( srcEntity, dstEntity, args ):
	"""
	目标自己对自己施法
	"""
	argList = args.split()
	try:
		skillID = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/spellItself skillID"))
		return
	if not dstEntity.isCombatEntity():
		srcEntity.statusMessage( csstatus.SKILL_CAST_ENTITY_ONLY )
		return
	dstEntity.useSkillToEntityGM( srcEntity, skillID, dstEntity.id )

def gmCommandAddEffect( srcEntity, dstEntity, args ):
	"""
	玩家向目标添加技能效果
	"""
	succeedList = []
	failedList	= []
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addEffect EffectIDs" ))
		return
	for EffectID in argList:
		if dstEntity.addFixIDEffect( srcEntity, int(EffectID)):
			succeedList.append( EffectID )
		else:
			failedList.append(EffectID)

	if len(succeedList):
		s = " ["
		for x in succeedList:
			s+=str(x)+"，"
		srcEntity.statusMessage(csstatus.GM_ADD_EFFECT_SUCCEED, s+"]")
	if len(failedList):
		s = " ["
		for x in failedList:
			s+=str(x)+"，"
		srcEntity.statusMessage( csstatus.GM_ADD_EFFECT_FAILED, s+"]" )


def gmCommandAddEffectSelf( srcEntity, dstEntity, args ):
	"""
	目标向玩家添加技能效果
	"""
	succeedList = []
	failedList	= []
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addEffectSelf EffectIDs" ))
		return
	for EffectID in argList:
		if srcEntity.addFixIDEffect( dstEntity, int(EffectID)):
			succeedList.append( EffectID )
		else:
			failedList.append(EffectID)

	if len(succeedList):
		s = " ["
		for x in succeedList:
			s+=str(x)+"，"
		srcEntity.statusMessage(csstatus.GM_ADD_EFFECT_SUCCEED, s+"]")
	if len(failedList):
		s = " ["
		for x in failedList:
			s+=str(x)+"，"
		srcEntity.statusMessage( csstatus.GM_ADD_EFFECT_FAILED, s+"]" )


def gmCommandAddEffectItSelf( srcEntity, dstEntity, args ):
	"""
	目标自己对自己添加技能效果
	"""
	succeedList = []
	failedList	= []
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addEffectItSelf EffectIDs" ))
		return
	for EffectID in argList:
		if dstEntity.addFixIDEffect( dstEntity, int(EffectID)):
			succeedList.append( EffectID )
		else:
			failedList.append(EffectID)

	if len(succeedList):
		s = " ["
		for x in succeedList:
			s+=str(x)+"，"
		srcEntity.statusMessage(csstatus.GM_ADD_EFFECT_SUCCEED, s+"]")
	if len(failedList):
		s = " ["
		for x in failedList:
			s+=str(x)+"，"
		srcEntity.statusMessage( csstatus.GM_ADD_EFFECT_FAILED, s+"]" )


def gmCommandSetMoney( srcEntity, dstEntity, args ):
	"""
	设置金币数量
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/set_money value"))
		return
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	amount = value - dstEntity.getMoney()
	KBEDebug.INFO_MSG( "%s(%i): set_money %s" % ( srcEntity.getName(), srcEntity.id, value) )
	if amount>0:
		dstEntity.addMoney( amount, csdefine.MONEY_ADD_REASON_GM_COMMAND )
	else:
		dstEntity.subMoney( -amount, csdefine.MONEY_SUB_REASON_GM_COMMAND )
	srcEntity.statusMessage( csstatus.GM_SET_ATTR_SUCCESS )

def gmCommandSetBindMoney( srcEntity, dstEntity, args ):
	"""
	设置绑定金币数量
	"""
	argList = args.split()
	try:
		value = int(argList[0])
	except:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS, str("/setBindMoney value"))
		return
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return

	amount = value - dstEntity.getBindMoney()
	KBEDebug.INFO_MSG("%s(%i): setBindMoney %s" % (srcEntity.getName(), srcEntity.id, value))
	if amount > 0:
		dstEntity.addBindMoney(amount, csdefine.MONEY_ADD_REASON_GM_COMMAND)
	else:
		dstEntity.subBindMoney(-amount, csdefine.MONEY_SUB_REASON_GM_COMMAND)
	srcEntity.statusMessage(csstatus.GM_SET_ATTR_SUCCESS)

def gmCommandSetPotential( srcEntity, dstEntity, args ):
	"""
	设置潜能
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setPotential value"))
		return
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	changeValue = value - dstEntity.potential
	if changeValue>0:
		dstEntity.addPotential( changeValue, csdefine.POTENTIAL_ADD_REASON_GMCOMMAND )
	elif changeValue<0:
		dstEntity.subPotential( changeValue, csdefine.POTENTIAL_ADD_REASON_GMCOMMAND )
		
def gmCommandSetLevel( srcEntity, dstEntity, args ):
	"""
	设置等级
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/set_level value"))
		return
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	KBEDebug.INFO_MSG( "%s(%i): set_level %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	dstEntity.setLevel( value )

def gmCommandSetXiuwei( srcEntity, dstEntity, args ):
	"""
	设置修为
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/add_xiuwei value"))
		return
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	amount = value - dstEntity.getXiuwei()
	KBEDebug.INFO_MSG( "%s(%i): set_xiuwei %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	dstEntity.addXiuwei( amount, csdefine.XIUWEI_ADD_REASON_GMCOMMAND )

def gmCommandSetExploit( srcEntity, dstEntity, args ):
	"""
	设置军功
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setExploit value"))
		return
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	amount = value - dstEntity.getExploit()
	KBEDebug.INFO_MSG( "%s(%i): setExploit %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	dstEntity.addExploit( amount )

def gmCommandSetMaxMilitaryRank( srcEntity, dstEntity, args ):
	"""
	设置历史最大的军衔等级
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setMaxMilitaryRank value value in 1 ~ 16 "))
		return
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	if value < 1 or value > 16:
		return
	KBEDebug.INFO_MSG( "%s(%i): setMaxMilitaryRank %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	dstEntity.setMaxMilitaryRank( value )


def gmCommandRemoveCompletedQuest( srcEntity, dstEntity, args ):
	"""
	清除任务完成记录
	value = 0 :清除所有的任务标记以及任务下保存的AIIDS
	value != 0 :清除指定任务标记以及指定任务下保存的AIIDS
	"""
	argList = args.split()
	if len(argList)==0:
		value = 0
	else:
		value = int( argList[0] )

	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	if value == 0:
		dstEntity.questLogger.clear()
		dstEntity.client.onClearQuestLog()
		dstEntity.clearQuestReordAIIDS()
		dstEntity.loopQuest["loopQuestList"] = []
		dstEntity.loopQuest["isAbandonQuest"] = False
		dstEntity.loopQuest["loopQuestNum"] = 0
		dstEntity.loopQuestProgress = 0
		KBEngine.globalData["RingTaskSpaceMgr"].setCurrentProgress( str(dstEntity.playerDBID), srcEntity.loopQuestProgress )
		dstEntity.removeQuestType( csdefine.QUEST_TYPE_LOOP )
		srcEntity.statusMessage( csstatus.GM_ALL_REQUEST_SIGN_REMOVE )
	else:
		dstEntity.questLogger.erase(value)
		dstEntity.client.onRemoveQuestLog(value)
		dstEntity.removeQuestRecordAIIDS(value)
		srcEntity.statusMessage( csstatus.GM_REQUESTID_SIGN_REMOVE, str(value))

def gmCommandAcceptQuest( srcEntity, dstEntity, args ):
	"""
	设置接受任务
	"""
	argList = args.split()
	try:
		questID = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/accept_quest questID"))
		return

	params = {}
	KBEDebug.INFO_MSG( "%s(%i): accept_quest %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	questScript = g_QuestLoader.getScript(questID)
	if questScript is None:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS, "quest:%d dosen't exist"%questID )
		return False

	srcEntity.addQuest(questID)
	questScript.acceptedBy(srcEntity, params)
	# 通知客户端(一些任务在接取后，就已经满足了任务完成条件，并且任务配置为了自动提交)
	if questID in srcEntity.questTable and srcEntity.client is not None:
		dataStream = srcEntity.getQuestDataByQuestID(questID)
		# ERROR_MSG("Role[%d] onAcceptQuest [%d]" %(srcEntity.id, questID))
		srcEntity.client.onAcceptQuest(dataStream)
	questScript.afterClientAccepted(srcEntity, params)


def gmCommandCompleteQuest( srcEntity, dstEntity, args ):
	"""
	设置任务完成
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/complete_quest questID"))
		return

	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	quest = dstEntity.questTable.get( value )
	if quest is not None:
		quest.setDone( dstEntity )
	KBEDebug.INFO_MSG( "%s(%i): complete_quest %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	
def gmCommandAcceptLoopQuest( srcEntity, dstEntity, args ):
	"""
	设置接受环任务
	"""
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	argList = args.split()
	if argList[0].isdigit() :
		questID = int( argList[0])
	else:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/acceptLoopQuest questID [num]"))
		return

	num = 0
	if len(argList) >= 2:
		num = int( argList[1] ) - 1
		
	dstEntity.loopQuest["loopQuestList"] = []
	dstEntity.loopQuest["isAbandonQuest"] = False
	dstEntity.loopQuest["loopQuestNum"] = 0
	dstEntity.loopQuest["taskCompleteNum"] = 0
	dstEntity.loopQuestProgress = 0
	dstEntity.questLogger.clearLoopQuest()
	dstEntity.client.onRemoveQuestLogByType("QuestLoop")
	dstEntity.removeQuestType( csdefine.QUEST_TYPE_LOOP )
	dstEntity.randomLoopQuest()
	if questID in dstEntity.loopQuest["loopQuestList"]:
		if dstEntity.loopQuest["loopQuestList"].index(questID) != num:
			dstEntity.loopQuest["loopQuestList"].remove( questID )
			dstEntity.loopQuest["loopQuestList"].insert( num, questID )
	else:
		dstEntity.loopQuest["loopQuestList"].insert( 0, questID )

	KBEDebug.INFO_MSG( "%s(%i): acceptLoopQuest %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )
	dstEntity.acceptQuest( dstEntity.loopQuest["loopQuestList"][0] )
	
	
def gmCommandSetAQuestFlag( srcEntity, dstEntity, args ):
	"""
	设置任务可否放弃
	"""
	argList = args.split()
	try:
		flag = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setAQuestFlag 0 or 1"))
		return
	if not flag in (0, 1):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setAQuestFlag 0 or 1"))
		return

	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		dstEntity = srcEntity
	dstEntity.setAbandonPrimaryFlag( flag )			#0为不可放弃，1为可以放弃
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS )

def gmCommandCompleteAutoQuest( srcEntity, dstEntity, args ):
	"""
	设置自动交接任务
	"""
	argList = args.split()
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/complete_autoQuest questID"))
		return

	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	quest = dstEntity.questTable.get( value )
	if quest is not None:
		quest.setDone( dstEntity )
		dstEntity.questAuto( int(value) )
	KBEDebug.INFO_MSG( "%s(%i): complete_quest %s" % ( srcEntity.getName(), srcEntity.id, argList[0] ) )

def gmCommandCompleteTask( srcEntity, dstEntity, args ):
	"""
	完成任务目标: /completeTask 任务ID 任务目标ID 次数
	"""
	progress = 0
	argList = args.split()
	if len( argList ) <= 2:
		progress = 1
	else:
		progress = int(argList[2])
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/completeTask questID taskID number"))
		return

	if len(argList) <= 1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/completeTask questID taskID number"))
		return

	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	quest = dstEntity.questTable.get( value )
	if quest is not None:
		isDone = quest.gmSetTaskDone( dstEntity, value, int(argList[1]), progress )
		if isDone:
			srcEntity.statusMessage( csstatus.GM_QUEST_TASK_USE_SUCCESS )

def gmCommandCompleteStageTask( srcEntity, dstEntity, args ):
	"""
	完成阶段目标: /completeStageTask 阶段ID 阶段目标ID 次数
	"""
	progress = 0
	argList = args.split()
	if len( argList ) < 2:
		progress = 1
	else:
		progress = int(argList[1])
	try:
		value = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/completeStageTask stageID number"))
		return

	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return

	spaceEntity = dstEntity.getCurrentSpace()
	isDone = spaceEntity.getScript().spaceStage_gmCompleteStageTask( spaceEntity, value, progress )
	if isDone:
		srcEntity.statusMessage( csstatus.GM_QUEST_TASK_STAGE_USE_SUCCESS )
	else:
		srcEntity.statusMessage( csstatus.GM_QUEST_TASK_STAGE_USE_FAILURE )

def gmCommandSetDebugFlag( srcEntity, dstEntity, args ):
	"""
	设置Debug Flag,以方便进行调试信息的打印。
	"""
	argList = args.split()
	flag = int( argList[0] )
	if not dstEntity:
		dstEntity = srcEntity
	
	if flag <= 0:
		dstEntity.setDebugFlag( 0 )
	else:
		dstEntity.addDebugFlag( flag )

def gmCommandSendAI( srcEntity, dstEntity, args ):
	"""
	向目标发送AI命令
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/sendAI commandID"))
		return

	cmd = argList[0]
	
	if len(argList) == 1:
		if dstEntity and dstEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			dstEntity.monsterAIOnCommand( srcEntity.id, "Role", cmd )
	elif len(argList) == 2:
		radius = int( argList[1])
		entities = dstEntity.entitiesInRangeExt( radius )
		for e in entities:
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				e.monsterAIOnCommand( srcEntity.id, "Role", cmd )

def gmCommandTriggerEvent( srcEntity, dstEntity, args ):
	"""
	触发某个事件
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/triggerEvent eventID"))
		return

	eventID = int( argList[0] )
	
	if dstEntity and dstEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
		dstEntity.triggerEvent( eventID , "" )

def gmCommandSmash( srcEntity, dstEntity, args ):
	"""
	销毁目标entity
	销毁选中dstEntity,不触发销毁事件（不填或填0不触发销毁事件，填1触发Entity的销毁事件）
	"""
	argList = args.split()

	if  dstEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
		return

	if len(argList) > 0 and argList[0] == "1" and dstEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
		dstEntity.triggerEvent(csdefine.ENTITY_EVENT_DESTORY_SELF,"")
	if dstEntity.getEntityFlag()==csdefine.ENTITY_FLAG_MONSTER:
		dstEntity.resetEnemyList()
	dstEntity.destroy()
	
def gmCommandSetSpeed( srcEntity, dstEntity, args ):
	"""
	设置目标的移动速度
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/setSpeed speedValue"))
		return

	if not hasattr(dstEntity,"setSpeed"):
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return

	try :
		speed = float( argList[0] )
	except :
		srcEntity.statusMessage( csstatus.GM_ARGS_MUST_INT)
		return

	dstEntity.setSpeed(speed)
	
def gmCommandAddFlag( srcEntity, dstEntity, args ):
	"""
	增加标志位
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/addFlag flag"))
		return

	for flag in argList:
		try :
			flag = int(flag)
		except :
			srcEntity.statusMessage( csstatus.GM_ARGS_MUST_INT )
			return

		dstEntity.addFlag(flag)
	
def gmCommandDelFlag( srcEntity, dstEntity, args ):
	"""
	移除标志位
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/delFlag flag"))
		return

	for flag in argList:
		try :
			flag = int(flag)
		except :
			srcEntity.statusMessage( csstatus.GM_ARGS_MUST_INT)
			return

		dstEntity.removeFlag(flag)

def gmCommandSetModel( srcEntity, dstEntity, args ):
	"""
	设置目标的模型编号
	"""
	if dstEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
		dstEntity.disMountPet()
	argList = args.split()
	modelNumber = ""
	modelScale = 1.0
	actionID = ""
	
	if  len(argList)>=3:
		modelNumber = argList[0]
		modelScale = float(argList[1])
		actionID = argList[2]
	if len(argList) == 2:
		modelNumber = argList[0]
		modelScale = float(argList[1])
	if len(argList) == 1:
		modelNumber = argList[0]
	dstEntity.setInitActionId(actionID)
	dstEntity.setExtraModelNumber( modelNumber )
	dstEntity.setModelScale(modelScale)
	if dstEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			dstEntity.withdrawPetByReason( csdefine.PET_WITHDRAW_CHANGE_BODY )
			dstEntity.client.OnChangeBodyStart()

def gmCommandSetScale( srcEntity, dstEntity, args ):
	"""
	设置目标的模型大小
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/setScale modelScale"))
		return

	modelScale = None
	try:
		modelScale = float(argList[0])
	except Exception as e:
		KBEDebug.ERROR_MSG("error:%s"%e)
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR )
	if modelScale:	
		dstEntity.modelScale = modelScale
		srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS )

def gmCommandSetPos( srcEntity, dstEntity, args ):
	"""
	/setPos XXX 设置目标Entity的坐标，空格分隔坐标参数，填客户端坐标
	"""
	argList = args.split()
	if len(argList)<3:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setPos X Y Z ") )
		return

	try:
		position = KBEMath.Unreal2KBEnginePosition((float(argList[0]) , float(argList[1]) , float(argList[2])))
		dstEntity.position = Math.Vector3(position)
		srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS )
	except Exception as e:
		srcEntity.statusMessage( csstatus.GM_CMMAND_FAILED )
		KBEDebug.ERROR_MSG("error:%s"%e)

def gmCommandSetDir( srcEntity, dstEntity, args ):
	"""
	/setDir XXX 设置目标Entity的朝向，空格分隔坐标参数，填客户端坐标
	"""
	argList = args.split()
	if len(argList)<3:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setDir X Y Z ") )
		return

	try:
		direction = KBEMath.Unreal2KBEngineDirection((float(argList[0]) , float(argList[1]) , float(argList[2])))
		dstEntity.direction = Math.Vector3(direction)
		srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS )
	except Exception as e:
		srcEntity.statusMessage( csstatus.GM_CMMAND_FAILED )
		KBEDebug.ERROR_MSG("error:%s"%e)
		


def gmCommandWatch( srcEntity, dstEntity, args ):
	"""
	玩家进入/离开观察者模式
	"""
	if srcEntity.hasFlag( csdefine.ROLE_FLAG_WATCHER ):
		srcEntity.removeFlag( csdefine.ROLE_FLAG_WATCHER )
		srcEntity.effectStateDec( csdefine.EFFECT_STATE_INVINCIBLE )
	else:
		srcEntity.addFlag( csdefine.ROLE_FLAG_WATCHER )
		srcEntity.effectStateInc( csdefine.EFFECT_STATE_INVINCIBLE )
		srcEntity.withdrawPetByReason( csdefine.PET_WITHDRAW_GMWATCHER )

def gmCommandShowInvisible( srcEntity, dstEntity, args ):
	"""
	显示范围内的隐身单位，并使其可选
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/showInvisible range" ) )
		return

	try:
		range = float( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR )
		return

	entities = srcEntity.entitiesInRangeExt( range )
	for entity in entities:
		entity.allClients.CLIENT_ShowInvisible()

def gmCommandHideInvisible( srcEntity, dstEntity, args ):
	"""
	恢复范围内的隐藏单位，并且不可选
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/hideInvisible range" ) )
		return

	try:
		range = float( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR )
		return

	entities = srcEntity.entitiesInRangeExt( range )
	for entity in entities:
		entity.allClients.CLIENT_HideInvisible()

def gmReloadAI( srcEntity, dstEntity, args ):
	"""
	ai热更新
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/reloadAI scriptID" ) )
		return

	from ConfigObject.MonsterAI.AIBase import AIMgr
	result = AIMgr.g_AIMgr.reloadMonsterAI( argList[0] )
	if result:
		srcEntity.statusMessage( csstatus.GM_RELOAD_SUCCEED, "AI",argList[0] )
	else:
		srcEntity.statusMessage( csstatus.GM_RELOAD_FAILED, "AI",argList[0] )

def gmReloadQuest( srcEntity, dstEntity, args ):
	"""
	quest热更新
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/reloadQuest questID" ) )
		return
	
	from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
	questID = int( argList[0] )
	result = g_QuestLoader.reloadQuestConfig( questID )
	if result:
		if srcEntity.hasQuest( questID ):
			srcEntity.abandonQuest( questID )
			srcEntity.acceptQuest( questID )
		srcEntity.statusMessage( csstatus.GM_RELOAD_SUCCEED, "Quest", argList[0] )
	else:
		srcEntity.statusMessage( csstatus.GM_RELOAD_FAILED, "Quest", argList[0] )
		
def gmReloadTalk( srcEntity, dstEntity, args ):
	"""
	npcTalk热更新
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/reloadTalk scriptID" ) )
		return

	from ConfigObject.Talk.TalkBase.NPCTalkLoader import NPCTalkLoader
	result = NPCTalkLoader.instance().reloadTalkConfig( argList[0] )
	if result:
		srcEntity.statusMessage( csstatus.GM_RELOAD_SUCCEED, "NPCTalk",argList[0] )
	else:
		srcEntity.statusMessage( csstatus.GM_RELOAD_FAILED, "NPCTalk",argList[0] )
		
def gmReloadEntity( srcEntity, dstEntity, args ):
	"""
	entity热更新
	"""
	import HotUpdate
	HotUpdate.reloadEntity()
	srcEntity.statusMessage( csstatus.GM_RELOADENTITY_SUCCEED )
	
def gmReloadScript( srcEntity, dstEntity, args ):
	"""
	Python脚步热更新
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/reloadScript ModuleName" ) )
		return
	
	import HotUpdate
	import os
	for i in os.walk( "res/scripts/cell" ):
		if argList[0]+".py" in i[2]:
			if len(i[0]) == 16:									# 说明在cell目录下
				path = argList[0]
			else:
				path = i[0][17:].replace('/','.').replace("\\",".") + '.' + argList[0]
			KBEDebug.ERROR_MSG("----->>>",i[0],path,len(i[0]),i[1],i[2])
			HotUpdate.reloadByPath( path )
			srcEntity.statusMessage( csstatus.GM_RELOADSCRIPT_SUCCEED, argList[0] )
			return
	srcEntity.statusMessage( csstatus.GM_RELOADSCRIPT_FAILED, argList[0] )
	
#	def reloadFile( path, file ):
#		isReloadFile = False
#		for fileName in os.listdir(path):
#			fp = os.path.join( path, fileName )
#			if os.path.isfile(fp) and file in fp:
##				filePath = fp
#				KBEDebug.ERROR_MSG("----->>>",fp)
#				isReloadFile = True
#				path = fp[17:][:-3].replace('/','.').replace("\\",".")
#				HotUpdate.reloadByPath( path )
#				srcEntity.statusMessage( csstatus.GM_RELOADSCRIPT_SUCCEED, argList[0] )
#				return
#			elif os.path.isdir(fp):
#				reloadFile( fp, file )
				
#		if  not isReloadFile:
#			srcEntity.statusMessage( csstatus.GM_RELOADSCRIPT_FAILED, argList[0] )
				
#	filePath = ""
#	searchFile( "res/scripts/cell", argList[0] )
#	if filePath:
#		path = filePath[17:][:-3].replace('/','.').replace("\\",".")
#		HotUpdate.reloadByPath( path )
#		srcEntity.statusMessage( csstatus.GM_RELOADSCRIPT_SUCCEED, argList[0] )
#	else:
#	reloadFile( "res/scripts/cell", argList[0] )
	
def gmReloadConfig( srcEntity, dstEntity, args ):
	"""
	配置热更新
	"""
	result = g_configLoader.reloadConfig()
	
	if result == 1:
		srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_SUCCESS )
	else:
		srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_FAIL, result )

def gmCommandPlaySound ( srcEntity, dstEntity, args ):
	"""
	/playSound XXX 播放指定编号的语音并显示半身像界面(参数填Game/Miscs/ContentConfig/VoiceConfig表的id)
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/playSound  VoiceID" ) )
		return

	srcEntity.showMessagePlaySound(argList[0])
	srcEntity.statusMessage(csstatus.GM_COMMAND_SUCCESS)

def gmCommandQueryFlag ( srcEntity, dstEntity, args ):
	"""
	/queryFlag 查询目标Entity的标识位，在聊天框显示，有多个标识位则空格分隔并从小到大排列
	"""
	flagString = ""
	for i in range(1,64):
		if dstEntity.hasFlag( i ):
			flagString = flagString + str(i) + " "
	
	if flagString == "":
		srcEntity.statusMessage(csstatus.GM_QUERY_RESULT,"None")
	else:
		srcEntity.statusMessage(csstatus.GM_QUERY_RESULT,flagString)

def gmCommandAddBuff ( srcEntity, dstEntity, args ):
	"""
	/addBuff XXX XXX 给目标增加BUFF，无目标则给玩家自己加BUFF，填buffID（Game/Miscs/ContentConfig/BuffTable），支持增加多个。
	"""
	succeedList = []
	failedList	= []
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addBuff  BuffIDs" ))
		return
	if not hasattr(dstEntity,"addBuff"):
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return
	for buffID in argList:
		if dstEntity.addBuff( srcEntity, int(buffID)):
			succeedList.append( buffID )
		else:
			failedList.append(buffID)

	if len(succeedList):
		s = " ["
		for x in succeedList:
			s+=str(x)+"，"
		srcEntity.statusMessage(csstatus.GM_ADD_BUFF_SUCCEED, s+"]")
	if len(failedList):
		s = " ["
		for x in failedList:
			s+=str(x)+"，"
		srcEntity.statusMessage( csstatus.GM_ADD_BUFF_FAILED, s+"]" )

def gmCommandAddBuffSelf( srcEntity, dstEntity, args ):
	"""
	/addBuffSelf XXX 目标给玩家增加BUFF，填buffID（Game/Miscs/ContentConfig/BuffTable），支持增加多个。
	"""
	succeedList = []
	failedList	= []
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addBuffSelf BuffIDs" ))
		return
	for buffID in argList:
		if srcEntity.addBuff( dstEntity, int(buffID)):
			succeedList.append( buffID )
		else:
			failedList.append(buffID)

	if len(succeedList):
		s = " ["
		for x in succeedList:
			s+=str(x)+"，"
		srcEntity.statusMessage(csstatus.GM_ADD_BUFF_SUCCEED, s+"]")
	if len(failedList):
		s = " ["
		for x in failedList:
			s+=str(x)+"，"
		srcEntity.statusMessage( csstatus.GM_ADD_BUFF_FAILED, s+"]" )

def gmCommandAddBuffItSelf( srcEntity, dstEntity, args ):
	"""
	/addBuffItSelf XXX 目标自己给自己增加BUFF，填buffID（Game/Miscs/ContentConfig/BuffTable），支持增加多个。
	"""
	succeedList = []
	failedList	= []
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addBuffItSelf BuffIDs" ))
		return
	if not hasattr(dstEntity,"addBuff"):
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return
	for buffID in argList:
		if dstEntity.addBuff( dstEntity, int(buffID)):
			succeedList.append( buffID )
		else:
			failedList.append(buffID)

	if len(succeedList):
		s = " ["
		for x in succeedList:
			s+=str(x)+"，"
		srcEntity.statusMessage(csstatus.GM_ADD_BUFF_SUCCEED, s+"]")
	if len(failedList):
		s = " ["
		for x in failedList:
			s+=str(x)+"，"
		srcEntity.statusMessage( csstatus.GM_ADD_BUFF_FAILED, s+"]" )

def gmCommandClearBuff ( srcEntity, dstEntity, args ):
	"""
	/clearBuff XXX XXX     清除目标的BUFF，无目标则清除自身的BUFF。参数（buffID）不填则清除所有BUFF，参数填了则清除指定BUFF，支持删除多个。
	"""
	succeedList = []
	failedList	= []
	argList = args.split()
	if not hasattr(dstEntity,"getAttrBuffs"):
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return
	attrBuffs = list(dstEntity.getAttrBuffs().values())
	if not len( argList ):
		if not len(attrBuffs):
			srcEntity.statusMessage( csstatus.GM_REMOVE_BUFF_SUCCEED, "all buffs" )
		for buffData in attrBuffs:
			if dstEntity.removeBuffByID( buffData.buffID ):
				succeedList.append(buffData.buffID)
			else:
				failedList.append(buffData.buffID)

	else:
		for buffID in argList:
			if dstEntity.removeBuffByID( int(buffID) ):
				succeedList.append(buffID)
			else:
				failedList.append(buffID)

	if len(succeedList):
		s = " ["
		for x in succeedList:
			s+=str(x)+"，"
		srcEntity.statusMessage(csstatus.GM_REMOVE_BUFF_SUCCEED, s+"]")
	if len(failedList):
		s = " ["
		for x in failedList:
			s+=str(x)+"，"
		srcEntity.statusMessage( csstatus.GM_REMOVE_BUFF_FAILED, s+"]" )



def gmCommandQueryBuff ( srcEntity, dstEntity, args ):
	"""
	/queryBuff  查询目标身上的buff，无目标则查询玩家自身buff，在聊天框显示buffID和剩余时间。显示格式为[buffID,剩余时间] [buffID,剩余时间] [buffID,剩余时间]。
	"""
	if not hasattr(dstEntity,"getAttrBuffs"):
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return
	outPutString = ""
	attrBuffs = dstEntity.getAttrBuffs()
	for buffData in attrBuffs.values():
		s = "["+str(buffData.buffID)+"，"+str(round( Functions.convertTime( buffData.getRemainingTime() ) ,1))+"]"
		outPutString += s

	srcEntity.statusMessage(csstatus.GM_QUERY_BUFF,outPutString)
	

def gmCommandFull ( srcEntity, dstEntity, args ):
	"""
	/full 设置目标HP MP为系统限定最大值，无目标则设置自身，即同时设置/set_attr HP_MAX、HP、MP_MAX、MP为最大值。
	"""

	dstEntity.HP_Max = csdefine.MAX_HP_FOR_GM
	dstEntity.HP = csdefine.MAX_HP_FOR_GM
	dstEntity.MP_Max = csdefine.MAX_MP_FOR_GM
	dstEntity.MP = csdefine.MAX_MP_FOR_GM
	srcEntity.statusMessage(csstatus.GM_COMMAND_SUCCESS)

def gmCommandClearBag ( srcEntity, dstEntity, args ):
	"""
	/clearBag 用于清除指定背包的全部物品
	"""
	messages = {0: csstatus.GM_CLEAR_EQUIPBAG_INFO,
				1:	csstatus.GM_CLEAR_COMMONBAG_INFO,
				2: csstatus.GM_CLEAR_QUESTBAG_INFO,
				3: csstatus.GM_CLEAR_SPARBAG_INFO,
				4: csstatus.GM_CLEAR_STORE_INFO,
		}
	bagtypeslist = []
	if args == "":
		bagtypeslist = [1,2,3]
	else:
		bagtypeslist = [int(item) for item in args.split()]
	for bagtype in bagtypeslist:
		itemlist = srcEntity.getItemListByKBType(bagtype)
		if itemlist:
			for item in itemlist:
				srcEntity.removeItemByAmount(item, item.getAmount(), csdefine.ITEM_REMOVE_BY_GM)
		message = messages.get(bagtype, -1)
		if message > 0:
			srcEntity.statusMessage( message, "" )
			
def gmCommandAddSkill( srcEntity, dstEntity, args ):
	"""
	添加技能
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addSkill  SkillID" ))
		return
	skill = srcEntity.getSkill( int(argList[0]) )
	if skill is None:
		srcEntity.statusMessage( csstatus.SKILL_NOT_EXIST )
		return
	if srcEntity.addSkill( int(argList[0]) ):
		srcEntity.statusMessage( csstatus.ADD_SKILL_SUCESS )
	else:
		srcEntity.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )

def gmCommandAddSkillForQuest( srcEntity, dstEntity, args ):
	"""
	添加技能
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addSkill  SkillID" ))
		return
	skill = srcEntity.getSkill( int(argList[0]) )
	if skill is None:
		srcEntity.statusMessage( csstatus.SKILL_NOT_EXIST )
		return
	if srcEntity.addSkill( int(argList[0]) ):
		srcEntity.triggerQuestEvent( QuestEventDefine.EVENT_LEARN_SKILL, int(argList[0]) )
		srcEntity.statusMessage( csstatus.ADD_SKILL_SUCESS )
	else:
		srcEntity.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )

def gmCommandRemoveSkill( srcEntity, dstEntity, args ):
	"""
	移除技能
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/removeSkill  SkillID" ))
		return
	skillID = int(argList[0])
	if skillID == 0:
		for index in range(len(srcEntity.attrSkills)-1,-1,-1):
			srcEntity.removeSkill( srcEntity.attrSkills[index] )
		return
	srcEntity.removeSkill( skillID )

def gmCommandPlayAction( srcEntity, dstEntity, args ):
	"""
	/playAction 用于播放指定动作
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/playAction actionID"))
		return
	dstEntity.allClients.CLIENT_OnPlayAction(argList[0],-1.0)
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )

def gmCommandPlayRandomAction( srcEntity, dstEntity, args ):
	"""
	播放指定动作（带指定随机种子）
	"""
	argList = args.split()
	if not len(argList):
		RandomNumber = random.randint( 0, pow( 2, 16 ) )
		dstEntity.allClients.PlayRandomAction( RandomNumber )
		srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )
		return
	try:
		RandomNumber = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_ARGS_MUST_INT)
		return
	dstEntity.allClients.PlayRandomAction( RandomNumber )
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )
	
def gmCommandStopAction( srcEntity, dstEntity, args ):
	"""
	/stopAction 用于停止动作
	"""
	dstEntity.allClients.CLIENT_StopAction()
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )

def gmCommandStopFrontAction( srcEntity, dstEntity, args ):
	"""
	/stopAction 用于停止前景动作
	"""
	dstEntity.allClients.CLIENT_StopFrontAction()
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )

def gmCommandPlayOneByOneAction( srcEntity, dstEntity, args ):
	"""
	/CLIENT_PlayOneByOneAction 用于播放连续动作
	"""
	if args == "":
		return
	actionList = [actionId for actionId in args.split()]
	actionIdList = []
	actionStartTimeList = []
	for action in actionList:
		data = action.split("|")
		actionIdList.append(data[0])
		if len(data) == 2:
			actionStartTimeList.append(data[1])
		else:
			actionStartTimeList.append("0")
	if not hasattr(dstEntity,"actionIndex"):
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return
	dstEntity.setActionIndex()
	dstEntity.allClients.CLIENT_PlayOneByOneAction(dstEntity.actionIndex, actionIdList, actionStartTimeList)
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )

def gmCommandQueryRelation( srcEntity, dstEntity, args ):
	"""
	查询战斗关系
	"""
	relChineseDict = { csdefine.COMBAT_RELATION_DEFAULT:"未定义", csdefine.COMBAT_RELATION_NORMAL:"友好", csdefine.COMBAT_RELATION_ENEMY:"敌对", \
						csdefine.COMBAT_RELATION_NEUTRALLY:"中立", csdefine.COMBAT_RELATION_NONE:"无关" }
	
	positiveRel = srcEntity.queryRelation( dstEntity )
	reverseRel = dstEntity.queryRelation( srcEntity )
	srcEntity.statusMessage( csstatus.GM_QUERY_RELATION, relChineseDict[positiveRel], positiveRel, relChineseDict[reverseRel], reverseRel )

def gmCommandPlayParticle( srcEntity, dstEntity, args ):
	"""
	播放粒子光效
	"""
	effectID = ""
	slotName = ""
	scale = -1.0
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/playParticle EffectID SlotName Scale"))
		return
	if len(args.split())==1:
		effectID = argList[0]
	elif len(args.split())==2:
		effectID = argList[0]
		slotName = argList[1]
	elif len(args.split())>=3:
		effectID = argList[0]
		slotName = argList[1]
		scale = float(argList[2])
	srcEntity.allClients.CLIENT_OnPlayParticles(dstEntity.id,effectID,slotName,scale,Math.Vector3(0,0,0))
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )


def gmSetHP( srcEntity, dstEntity, args ):
	"""
	按百分比设置血量
	"""
	argList = args.split()
	if len(argList)!=1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/set_HP percent"))
		return
	KBEDebug.INFO_MSG( "%s(%i): set_HP %s" % (srcEntity.getName(), srcEntity.id, args) )
	dstEntity.HP = int( dstEntity.HP_Max *  ( int( argList[0])/100 ) )


def gmAddTitle( srcEntity, dstEntity, args ):
	"""
	玩家添加称号
	"""
	argList = args.strip().split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/addTitle titleID"))
		return
	KBEDebug.INFO_MSG( "%s(%i): addTitle %s" % (srcEntity.getName(), srcEntity.id, args) )
	srcEntity.addTitle(int(argList[0]))

def gmRemoveTitle( srcEntity, dstEntity, args ):
	"""
	玩家删除称号
	"""
	argList = args.strip().split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/removeTitle titleID"))
		return
	KBEDebug.INFO_MSG( "%s(%i): removeTitle %s" % (srcEntity.getName(), srcEntity.id, args) )
	srcEntity.removeTitle(int(argList[0]))
	
def gmCommandSetAdult(srcEntity, dstEntity, args):
	argList = args.strip().split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/setAdult 0 or 1"))
		return
	srcEntity.gmSetAgeState(int(argList[0]))
	
def gmCommandTongCreate(srcEntity, dstEntity, args):
	argList = args.strip().split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/tongCreate name"))
		return
	srcEntity.base.createTong( argList[0] )
	
def gmCommandTongQuit(srcEntity, dstEntity, args):
	if srcEntity.tongDBID:
		srcEntity.base.tongQuit()
	
def gmCommandTongDisMiss(srcEntity, dstEntity, args):
	if srcEntity.tongDBID:
		srcEntity.base.tongDismiss()

def gmCommandActivity_control( srcEntity, dstEntity, args ):
	"""
	打开/关闭 活动
	"""
	argList = args.strip().split()
	if len(argList) > 1:
		tempInfo = activity_dict.get(argList[0],None)
		if not tempInfo or len(tempInfo) <= 1:
			return
		if argList[1] == "0":
			getattr(KBEngine.globalData[tempInfo[0]],"GMCommand")(tempInfo[2])
		else:
			getattr(KBEngine.globalData[tempInfo[0]],"GMCommand")(tempInfo[1])

def gmCommandEliminateCD( srcEntity, dstEntity, args ):
	"""
	/clearCD 清除目标的所有CD，无目标则清除自身的所有CD
	"""
	if not hasattr(dstEntity,"getCooldown"):
		srcEntity.statusMessage(csstatus.GM_SET_ENTITY_ERROR)
		return		
	dstCooldownList = dstEntity.getCooldown()
	if dstCooldownList and dstEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
		dstEntity.attrCooldowns = []
		dstEntity.clearCooldown( True )
		srcEntity.statusMessage( csstatus.GM_REMOVE_CD_SUCCEED )
	else:
		dstEntity.attrCooldowns = []
		srcEntity.statusMessage( csstatus.GM_REMOVE_CD_SUCCEED )

def gmCommandClearPetSleep( srcEntity, dstEntity, args ):
	"""
	/clearPetSleep 清除幻兽睡眠时间
	"""
	srcEntity.base.removePetSleeptime()
	srcEntity.statusMessage( csstatus.GM_REMOVE_CD_SUCCEED )
		
def gmCommandGotoMagicMazeChild( srcEntity, dstEntity, args ):
	"""
	/gotoMagicMazeChild 进入幻阵迷宫子副本
	"""
	argList = args.split()
	if len(argList) < 2:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/gotoMagicMazeChild spaceNum spaceKey "))
		return
	spaceData = argList[0]
	childSpace = argList[1]
	spaceLevel = srcEntity.getLevel()
	teammates={}
	if srcEntity.isInTeam():
		belongType = csdefine.SPACE_BELONG_TEAM
		spaceKey = str( srcEntity.teamMailbox.id )
		for memMB in srcEntity.getAllTeamMemberMB():
			memPlayer = KBEngine.entities.get( memMB.id, None )
			if memPlayer:
				teammates[ memPlayer.playerDBID ] = memMB		
	else:
		belongType = csdefine.SPACE_BELONG_PERSON
		spaceKey = str( srcEntity.playerDBID )
		teammates[srcEntity.playerDBID]=srcEntity.base

	dataCfg = LoadModule.openJsonCfg("MagicMazeConfig/MagicMazeConfig.json")
	mainScriptID = dataCfg.get( spaceData,{} ).get("mainSpace","")
	pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "players": teammates, "mainSpace":spaceData,"mainScriptID":mainScriptID}
	KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeSpace(belongType, spaceKey, pickArg)
	KBEngine.globalData["MagicMazeSpaceManager"].setNextLevelLoading(belongType, spaceKey, srcEntity.base, 0, 0,mainScriptID)
	srcEntity.gotoSpaceEnterPos(childSpace, pickArg)
	
def gmCommandSetMagicMazeChild( srcEntity, dstEntity, args ):
	"""
	/setMagicMazeChild 进入幻阵迷宫主副本后，设置幻阵迷宫子副本
	"""
	if srcEntity.isInTeam() and srcEntity.isTeamCaptain():
		belongType = csdefine.SPACE_BELONG_TEAM
		spaceKey = str( srcEntity.teamMailbox.id )
	else:
		belongType = csdefine.SPACE_BELONG_PERSON
		spaceKey = str( srcEntity.playerDBID )
	
	argList = args.strip().split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/setMagicMazeChild progress"))
		return
		
	spaceEntity = srcEntity.getCurrentSpace()
	if spaceEntity:
		spaceEntity.progress = int(argList[0])
		KBEngine.globalData["MagicMazeSpaceManager"].setSpaceProgress(belongType, spaceKey, int(argList[0]),spaceEntity.createArgs["mainScriptID"])
		spaceEntity.getScript().onStartTeleportToChild(spaceEntity, srcEntity, belongType )
		
def gmCommandSetTongAttr(srcEntity, dstEntity, args):
	entity = dstEntity or srcEntity
	if entity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
		if entity.tongMB is None:
			entity.statusMessage( csstatus.TONG_SPACE_COPY_NOT_IN_TONG )
			return
			
		argList = args.strip().split()
		if not argList:
			srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/setTongAttr [exp, contribution, level, activity, grow, money, skill] value"))
			return
		if argList[0] != "skill" and len(argList) < 2:
			srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS,str("/setTongAttr [exp, contribution, level, activity, grow, money, skill] value"))
			return
		entity.tongMB.GM_CommandSetAttr( entity.playerDBID, argList[0], int( argList[1] ) )
	
def gmCommandRelaodFaZhenCf( srcEntity, dstEntity, args ):
	"""
	更新法阵配置
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/reloadFaZhenCf scriptID" ) )
		return

	from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase.SpellBoxAdvancedStateMgr import g_spellBoxAdvancedStateMgr
	result = g_spellBoxAdvancedStateMgr.reloadSpellBoxAdvancedState( argList[0] )
	if result:
		srcEntity.statusMessage( csstatus.GM_RELOAD_SUCCEED, "FaZhenCf",argList[0] )
	else:
		srcEntity.statusMessage( csstatus.GM_RELOAD_FAILED, "FaZhenCf",argList[0] )
		
def gmCommandShowRole( srcEntity, dstEntity, args ):
	"""
	查询当前服务器中玩家人数
	"""
	def _onCallBack( entity, result, rows, insertid, errstr):
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		
		if len(result) <= 0: return
		amount = int(result[0][0])
		entity.client.statusMessage( csstatus.GM_SHOW_BASEAPP_ROLE, "Server|role num:[{}]".format(amount) )
		
	entity = srcEntity
	if not entity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
		entity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	entity.base.showBaseAppAllRole()
	
	role = monster = space = curSpaceRole = 0
	for e in KBEngine.entities.values():
		if e.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			role += 1
			
			if e.spaceID == srcEntity.spaceID:
				curSpaceRole += 1
		elif e.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
			monster += 1
		elif e.isEntityFlag( csdefine.ENTITY_FLAG_SPACE ):
			space += 1
	
	cid = os.getenv("KBE_COMPONENTID")
	srcEntity.client.statusMessage( csstatus.GM_SHOW_BASEAPP_ROLE, "Cell[{}]|role:[{}], monster:[{}], space:[{}], curSpaceRole:[{}]".format(cid, role, monster, space, curSpaceRole) )
	KBEngine.globalData[ csdefine.GLOBAL_CHANNEL_KEY_RECORD_ENTITY_NUM ] = weakref.proxy(srcEntity)
	
	sql = "select count(*) from kbe_entitylog where entityType = 3;"
	KBEngine.executeRawDatabaseCommand(sql, Functions.Functor(_onCallBack, srcEntity))
	
def gmCommandSetRoleSpaceRelationRule( srcEntity, dstEntity, args ):
	"""
	设置角色关系规则
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setRoleSpaceRelationRule rule" ) )
		return
		
	if not srcEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	srcEntity.setSpaceRelationRule(int(args[0]))
	
def gmCommandSetXianShi( srcEntity, dstEntity, args ):
	"""
	设置角色 仙石
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setXianShi num" ) )
		return
		
	srcEntity.base.setXianShi( int(argList[0]), csdefine.CHANGE_XIANSHI_GM_SET)
	
def gmCommandSetLingShi( srcEntity, dstEntity, args ):
	"""
	设置角色 灵石
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setLingShi num" ) )
		return
		
	srcEntity.base.setLingShi( int(argList[0]), csdefine.CHANGE_XIANSHI_GM_SET)
	
	
def gmCommandSetXuanShi( srcEntity, dstEntity, args ):
	"""
	设置角色 玄石
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setXuanShi num" ) )
		return
		
	srcEntity.base.setXuanShi( int(argList[0]), csdefine.CHANGE_XUANSHI_GM_SET)
	
def gmCommandSetSyncPosToOtherClient( srcEntity, dstEntity, args ):
	"""
	机器人使用(释放完带位移的技能后，同步一次位置)
	同步位置数据给其他客户端
	"""
	argList = args.split()
	if len(argList) < 6:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/setSyncPosToOtherClient px py pz dx dy dz" ))
		return
		
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	try:	#已输入position、direction
		position  = Math.Vector3((float(argList[0]) , float(argList[1]) , float(argList[2])))
		direction = Math.Vector3((float(argList[3]), float(argList[4]), float(argList[5])))
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"")
		return

	srcEntity.setPositionForOthers(position)
	srcEntity.setDirectionForOthers(direction)
	
def gmCommandCreateTeam( srcEntity, dstEntity, args ):
	"""
	创建队伍
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	srcEntity.base.createSelfTeamLocally()
	
def getRandPosInCircle( centerPos, radius, num, entity ):
	"""
	在圆内获得随机点坐标
	"""
	posList = []
	while num:
		x = centerPos[2]+random.uniform(-1,1)*radius
		y = centerPos[0]+random.uniform(-1,1)*radius
		posList.append(Math.Vector3( y, entity.position[1], x ))
		num-=1
	return posList	

def gmCommandTestMonsterFight( srcEntity, dstEntity, args ):
	"""
	创建Monster，互相攻击
	"""	
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	argList = args.split()
	if len(argList) != 2:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/testMonsterFight radius amount" ))
		return
	
	radius = int(argList[0])
	amount = int(argList[1])
	centerPos = Math.Vector3( srcEntity.position )
	posList = getRandPosInCircle( centerPos, radius, int(amount / 2), srcEntity )
	
	targetDirection = Math.Vector3( srcEntity.direction )
	for targetPosition in posList:
		newEntity = srcEntity.createEntityByScriptID("20012296", Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection )})
		newEntity = srcEntity.createEntityByScriptID("20012297", Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection )})

def gmCommandCheckMemLeak( srcEntity, dstEntity, args ):
	"""
	查看内存泄漏
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	cid = os.getenv("KBE_COMPONENTID")
	srcEntity.client.statusMessage( csstatus.GM_CHECK_INFO, "Cell[{}]内存泄漏{}".format(cid, len(KBEngine.entities.garbages)) )
	KBEngine.globalData[ csdefine.GLOBAL_CHANNEL_KEY_MEMORY_LEAK ] = weakref.proxy(srcEntity)
	
def gmCommandCreateMonsterInCircle( srcEntity, dstEntity, args ):
	"""
	在一定范围内创建怪物
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	argList = args.split()
	if len(argList) != 3:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/createMonsterInCircle scriptID radius amount" ))
		return
	
	scriptID = argList[0]
	radius = int(argList[1])
	amount = int(argList[2])
	centerPos = Math.Vector3( srcEntity.position )
	posList = getRandPosInCircle( centerPos, radius, amount, srcEntity )
	
	targetDirection = Math.Vector3( srcEntity.direction )
	for targetPosition in posList:
		newEntity = srcEntity.createEntityByScriptID(scriptID, Math.Vector3(targetPosition), targetDirection,{ "spawnPos":Math.Vector3( targetPosition ) ,"spawnDir":Math.Vector3( targetDirection )})

def gmCommandOpenTeleportPoint( srcEntity, dstEntity, args ):
	"""
	激活所有传送点
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	for data in g_JsonData.teleportStoneDatas:
		if srcEntity.teleportPointNPCs == "":
			srcEntity.teleportPointNPCs += data["Name"]
		elif srcEntity.isOpenTeleportPoint(data["Name"]) == False:
			srcEntity.teleportPointNPCs += ("|" + data["Name"])
			
def gmCommandDisbandAllTong( srcEntity, dstEntity, args ):
	"""
	解散所有帮会
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	KBEngine.globalData["TongMgr"].disbandAllTong()
	
def gmCommandSetJumpData( srcEntity, dstEntity, args ):
	"""
	/setJumpData 用于设置跳跃相关数据
	"""
	argList = args.split(" ")
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str("/setJumpData jumpType...."))
		return
	
	InJumpZVelocity = 0.0
	InGravityScale = 0.0
	InBrakingDecelerationFalling = 0.0
	InMaxWalkSpeed = 0.0
	if len(argList) > 1:
		InJumpZVelocity = float(argList[1])
	if len(argList) > 2:
		InGravityScale = float(argList[2])
	if len(argList) > 3:
		InBrakingDecelerationFalling = float(argList[3])
	if len(argList) > 4:
		InMaxWalkSpeed = float(argList[4])
	
	dstEntity.allClients.OnSetJumpData(int(argList[0]), InJumpZVelocity, InGravityScale, InBrakingDecelerationFalling, InMaxWalkSpeed)
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS,"" )	
	
def gmCommandTurnToPos( srcEntity, dstEntity, args ):
	"""
	修改朝向
	"""	
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	argList = args.split()
	if len(argList) != 1:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/turnToPos z" ))
		return
	
	z = float(argList[0])
	direction = srcEntity.direction
	direction.z = z
	srcEntity.changeDirection(direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
	

@KST_Profile
def gmCommandStartAITick( srcEntity, dstEntity, args ):
	"""
	Monster执行一次AI tick
	"""	
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	dstEntity.monsterAITick()
	
@KST_Profile
def gmCommandSpell2( srcEntity, dstEntity, args ):
	"""
	玩家向目标施法
	"""
	gmCommandSpell(srcEntity, dstEntity, args)
	
def gmCommandFullAll( srcEntity, dstEntity, args ):
	"""
	设置当前space的玩家及怪物都满血
	"""	
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	for id, entity in KBEngine.entities.items():
		if not hasattr(entity, "getEntityFlag"):
			continue
			
		if entity.spaceID != srcEntity.spaceID:
			continue
			
		if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or entity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			entity.HP_Max = 999999999
			entity.HP = 999999999
			entity.hpModifyRatio = 1333333.32

def gmCommandYXLMSignUp( srcEntity, dstEntity, args ):
	"""
	"""
	KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_reqPerson( srcEntity.base, srcEntity.playerDBID, srcEntity.getCamp(), srcEntity.getLevel(), srcEntity.getName() )

def gmCommandQueryLayer( srcEntity, dstEntity, args ):
	"""
	查询所在导航层
	"""
	curLayer = 0
	layerMax = dstEntity.getCurrentSpace().getScript().getNavmeshLayers()
	if (layerMax - 1):
		for i in range(layerMax):
			PositionList = KBEngine.collideVertical(dstEntity.spaceID, i, dstEntity.position, 2, -2 )
			if PositionList and len(PositionList):
				curLayer = i
				break
	srcEntity.statusMessage(csstatus.GM_QUERY_RESULT,str(curLayer))

def gmCommandSetCampSwitch( srcEntity, dstEntity, args ):
	"""
	设置阵营开关
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setCampSwitch num" ) )
		return
	KBEngine.globalData["CampMgr"].setCampSwitch(int(argList[0]))
	
def gmCommandSetLingMaiSignUp( srcEntity, dstEntity, args ):
	"""
	灵脉战场报名
	"""
	srcEntity.base.signInLingMai()
	
def gmCommandSetJSSLCSignUp( srcEntity, dstEntity, args ):
	"""
	晶石狩猎场报名
	"""
	KBEngine.globalData["SparHunTingManager"].activeSignUp( srcEntity, srcEntity.playerDBID, srcEntity.getLevel() ,srcEntity.getCamp() )
	
def gmCommandSetJSSLCEnter( srcEntity, dstEntity, args ):
	"""
	晶石狩猎场进入
	"""
	pos = Math.Vector3(0,0,0)
	if srcEntity.getCamp() == csdefine.CAMP_TAOSIM:
		pos = (-40523, 35682, 9)
	else:
		pos = (-41315, -19230, 52)
	pos = KBEMath.Unreal2KBEnginePosition( pos )
	KBEngine.globalData["SparHunTingManager"].requestEnter( srcEntity ,Math.Vector3(pos),Math.Vector3(0,0,0),srcEntity.getLevel() )
	
def gmCommandSetWXHJ( srcEntity, dstEntity, args ):
	"""
	五行画卷属性设置
	"""
	try:
		argList = args.split()
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR, "" )
		return
	argsLen = len( argList )
	if argsLen != 1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setWXHJ key"))
		return
	
	dstEntity.setTemp("attributeType", argList[0])
	
def gmCommandQueryWXHJ( srcEntity, dstEntity, args ):
	"""
	五行画卷属性查询
	"""
	srcEntity.statusMessage( csstatus.GM_QUERY_RESULT, dstEntity.queryTemp("attributeType"))
	
def gmCommandSetVIP( srcEntity, dstEntity, args ):
	"""
	设置账号为VIP账号
	"""	
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	argList = args.split()
	if len(argList) != 1:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/setVIP value" ))
		return
	
	srcEntity.base.setAccountVIP(int(argList[0]))

def gmCommandQuerySceneObjectName( srcEntity, dstEntity, args ):
	"""
	查询移动平台Uname
	"""
	srcEntity.statusMessage( csstatus.GM_QUERY_RESULT,dstEntity.getScript().uname)
	
def gmCommandSetSpaceDebugFlag( srcEntity, dstEntity, args ):
	"""
	设置Debug Flag,以方便进行调试信息的打印。
	"""
	argList = args.split()
	if len(argList) != 2:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/setSpaceDebugFlag spaceScriptID value" ))
		return
	
	spaceScriptID = argList[0]
	flag = int( argList[1] )
	
	space = srcEntity.getCurrentSpace()
	key = "SPACE_DEBUG_FLAG_{}".format(spaceScriptID)
	if flag > 0:
		KBEngine.cellAppData[key] = True
		return
	
	if key in KBEngine.cellAppData:
		del KBEngine.cellAppData[key]
		
def gmCommandQuerySpace( srcEntity, dstEntity, args ):
	"""
	查询当前在哪个space
	"""
	srcEntity.statusMessage( csstatus.GM_QUERY_RESULT, srcEntity.getCurrentSpaceScriptID())

def gmCommandClearAllActivityRecord( srcEntity, dstEntity, args ):
	"""
	清除玩家副本和活动的参加记录
	"""
	for activityType in csdefine.ACTIVITY_TYPE_LIST:
		srcEntity.clearActivityDegree( activityType )
	srcEntity.statusMessage( csstatus.GM_CLEAR_ACTIVITY_DEGREE,"" )
	
def gmCommandSetMiniMapScale( srcEntity, dstEntity, args ):
	"""
	设置小地图可视范围的默认缩放倍数
	"""
	argsList = args.split()
	if srcEntity.getClient():
		srcEntity.client.CLIENT_SetMiniMapViewDefaultScale(float(argsList[0]))
		
def gmCommandClearRejoinTongForbidTime( srcEntity, dstEntity, args ):
	"""
	清除限制申请帮会时间
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	srcEntity.base.clearRejoinTongForbindTime()

def gmCommandGotoSpaceRingTask( srcEntity, dstEntity, args ):
	"""
	地图传送
	"""
	argList = args.split()
	belongType = csdefine.SPACE_BELONG_PERSON
	spaceKey = str( srcEntity.playerDBID )
	pickArg = { "packBelongType": belongType, "spaceKey":spaceKey }
	if argList[0] == "cycle_L_HRWMJ01":
		srcEntity.loopQuestProgress = 0
	if argList[0] == "cycle_L_HRWMJ02":
		srcEntity.loopQuestProgress = 6
	if argList[0] == "cycle_L_HRWMJ03":
		srcEntity.loopQuestProgress = 12
	KBEngine.globalData["RingTaskSpaceMgr"].setRingTaskItem( spaceKey )
	KBEngine.globalData["RingTaskSpaceMgr"].setIsInMainScene( spaceKey, True )
	KBEngine.globalData["RingTaskSpaceMgr"].setCurrentProgress( spaceKey, srcEntity.loopQuestProgress )
	if srcEntity.loopQuest["loopQuestList"]:
		questID = str(srcEntity.loopQuest["loopQuestList"][0])
		KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( srcEntity.base, spaceKey, str(questID), 0 )
		srcEntity.gotoRingTaskSpace( argList[0], questID, pickArg, True )
	else:
		if srcEntity.randomLoopQuest():
			questID = str(srcEntity.loopQuest["loopQuestList"][0])
			KBEngine.globalData["RingTaskSpaceMgr"].setPreloadSpace( srcEntity.base, spaceKey, str(questID), 0 )
			srcEntity.gotoRingTaskSpace( argList[0], questID, pickArg, True )
			
def gmCommandSetOnlineTime( srcEntity, dstEntity, args ):
	"""
	设置在线时长
	"""
	try:
		argList = args.split()
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR, "" )
		return
	argsLen = len( argList )
	if argsLen != 1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setOnlineTime t"))
		return
	
	srcEntity.base.gmSetOnlineTime(int(argList[0]))
	
def gmCommandSetOfflineTime( srcEntity, dstEntity, args ):
	"""
	设置离线时长
	"""
	try:
		argList = args.split()
	except ValueError:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR, "" )
		return
	argsLen = len( argList )
	if argsLen != 1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setOnlineTime t"))
		return
	
	srcEntity.base.gmSetOfflineTime(int(argList[0]))
	
def gmCommandAddFoe( srcEntity, dstEntity, args ):
	"""
	添加仇人
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE or dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	if srcEntity.id == dstEntity.id:
		return
	
	srcEntity.base.addFoe(dstEntity.playerName)

def gmCommandQuyerNavLayer(srcEntity, dstEntity, args):
	"""
	"""
	layers = dstEntity.getCurrentSpace().getScript().getNavmeshLayers()
	targetLayerList = []
	for i in range(layers):
		#垂直取点 判断是否在此layer上
		positionList = KBEngine.collideVertical(dstEntity.spaceID, i, dstEntity.position, 2, -2 )
		#找到目标所在layer
		if positionList:
			targetLayerList.append(i)
			
	srcEntity.statusMessage(csstatus.GM_QUERY_RESULT, targetLayerList)
	
def gmCommandFollow(srcEntity, dstEntity, args):
	"""
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	argList = args.split()
	if len(argList) == 0:
		position = KBEMath.Unreal2KBEnginePosition((float(26473) , float(-60183) , float(-1297)))
		srcEntity.gotoSpace( "fu_ben_bigmap", tuple(Math.Vector3(position)), srcEntity.direction )
	elif len(argList) >= 1:
		line = 1
		row = 0
		lst = [0, 1, -1, 2, -2]
		pos = srcEntity.position
		dir = srcEntity.direction
		spaceEntity = srcEntity.getCurrentSpace()
		
		syncPos = int(argList[1]) if len(argList) > 1 else 0
		amount = int(argList[0])
		for i in range(amount):
			if row >= len(lst):
				line += 1
				row = 0
			
			position = (pos.x + 1 * line, pos.y, pos.z + 1 * lst[row])
			entity = spaceEntity.createEntityByScriptID("20012231", position, dir, {"spawnPos":position, "spawnDir": dir, "controlEntityID": srcEntity.id, "syncPos" : syncPos })
			entity.moveSpeed = srcEntity.getSpeed()
		
			i += 1
			row += 1
	
def gmCommandCleanEntity(srcEntity, dstEntity, args):
	"""
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	temp = []
	for _, entity in KBEngine.entities.items():
		if entity.spaceID != srcEntity.spaceID:
			continue
		
		if entity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			temp.append(entity)
		
	while len(temp):
		entity = temp.pop(0)
		entity.destroySelf()
	
def gmCommandqueryEntityCount(srcEntity, dstEntity, args):
	"""
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	role = 0
	monster = 0
	for _, e in KBEngine.entities.items():
		if e.spaceID == srcEntity.spaceID:
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				monster += 1
			elif e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				role += 1
	
	srcEntity.statusMessage( csstatus.GM_SHOW_BASEAPP_ROLE, "role:{}|monster:{}".format(role, monster) )

def gmCommandCatchEntity( srcEntity, dstEntity, args ):
	"""
	将玩家或者怪物 拉到自己身边
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/catch scriptID or /catch playerName"))
		return
	spaceEntity = srcEntity.getCurrentSpace()
	if not spaceEntity:
		return

	if argList[0].isdigit():
		entities = spaceEntity.getEntityMailBoxRecord( argList[0] )
		for entity in entities:
			entity.setPosition( srcEntity.position )
	else:
		for role in spaceEntity._spaceRoles:
			if role.getName() == argList[0]:
				role.gotoSpace( spaceEntity.scriptID,srcEntity.position, role.direction  )


def gmCommandEquipArms( srcEntity, dstEntity, args ):
	"""
	士兵列阵，添加兵力
	"""
	argList = args.split()
	if len(argList) != 4 :
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/equipArms soldierScriptID number leftGuardScriptID rightGuardScriptID"))
		return
	
	srcEntity.equipArms( argList[ 0 ], int( argList[1] ), argList[2], argList[3] )

def gmCommandCreateArms( srcEntity, dstEntity, args ):
	"""
	士兵列阵，创建兵力
	"""
	argList = args.split()
	if len(argList) <1 :
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/createArms groupID"))
		return
	
	srcEntity.callRoleArmySoldier(int(argList[0]))

def gmCommandRemoveArms( srcEntity, dstEntity, args ):
	"""
	士兵列阵，创建兵力
	"""
	argList = args.split()
	if len(argList) < 1 :
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/removeArms"))
		return
	
	srcEntity.roleDestroyArms()


def gmCommandLeadArms( srcEntity, dstEntity, args ):
	"""
	士兵列阵 领兵 /leadArms modelList
	"""
	argsList = args.split()

	dstEntity.setArmyModelList(argsList)

def gmCommandCreateSoldiers( srcEntity, dstEntity, args ):
	"""
	士兵列阵 领兵 /leadArms modelList
	"""
	argsList = args.split()
	if len(argsList)<2:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/createSoldiers scriptID amount"))

	if(dstEntity.getEntityFlagExt()!=csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("target must be MonsterCommander"))
	dstEntity.createSoldiers(argsList[0], argsList[1])
	
def gmCommandFinishCompose( srcEntity, dstEntity, args ):
	"""
	完成工具、乾坤鼎的打造
	"""
	srcEntity.GM_finishCompose()

def gmCommandClearPetCDTime( srcEntity, dstEntity, args ):
	"""
	移除幻兽喂养时间
	"""
	KBEngine.globalData["SpaceLunHuiMiJinMgr"].GM_clearPetCDTime( srcEntity, srcEntity.playerDBID )

def gmCommandMove_CST_9506Cmd(srcEntity, dstEntity, args):
	"""
	测试用
	"""
	argList = args.split()
	yawBase = csarithmetic.getYawByVector3(dstEntity.position-srcEntity.position)
	theta=60
	if len(argList)==3:
		moveTime, radius, theta = argList[:3]
		dstEntity.move_CST_9506(yawBase, float(theta), float(moveTime), float(radius))
	else:
		dstEntity.move_CST_9506(yawBase, theta)
		
def gmCommandFindRole(srcEntity, dstEntity, args ):
	"""
	查找entity在哪个base和cell中
	"""
	try:
		argList = args.split()
		id = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/findRole id"))
		return
		
	if id in KBEngine.entities:
		cid = os.getenv("KBE_COMPONENTID")
		srcEntity.statusMessage( csstatus.GM_CHECK_INFO, "role[{}]在cell[{}]".format(id, cid) )
	KBEngine.globalData[ csdefine.GLOBAL_CHANNEL_KEY_FIND_ROLE ] = [weakref.proxy(srcEntity), id]


def gmCommandTestEffect(srcEntity, dstEntity, args ):
	"""
	查找角色在哪个base和cell中
	"""
	try:
		argList = args.split()
		effectType = argList[0]
		effectIsOpen = int( argList[1] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/TestEffect type isOpen"))
		return
		
	for e in srcEntity.getCurrentSpace().getSpaceRoles():
		e.client.GMTestOpenEffect( effectType, effectIsOpen )

def gmReloadHotConst( srcEntity, dstEntity, args ):
	"""
	HotConst热更新
	"""
	import HotUpdate
	import HotConst
	HotUpdate.reloadByModule( HotConst )
	value = KBEngine.globalData.get(csdefine.GLOBAL_CHANNEL_KEY_HOT_CONST, False)
	KBEngine.globalData[ csdefine.GLOBAL_CHANNEL_KEY_HOT_CONST ] = not value
	srcEntity.statusMessage( csstatus.GM_RELOADSCRIPT_SUCCEED )

def gmNotifyDeclareWarPlayer( srcEntity, dstEntity, args ):
	"""
	GM 命令 提示玩家参加争夺战
	"""
	dstEntity.gmNotifyDeclareWarPlayer()


def gmClimb( srcEntity, dstEntity, args ):
	"""
	士兵攀爬 测试指令
	"""
	srcEntity.roleCmdClimb()

def gmSignUpBHZB( srcEntity, dstEntity, args ):
	"""
	报名帮会争霸
	"""
	srcEntity.gmSignUpBHZB()

def gmEnterBHZBHomeBarracks( srcEntity, dstEntity, args ):
	"""
	进入帮会争霸大本营
	"""
	KBEngine.globalData["BHZBManager"].enterBHZBHomeBarracks( srcEntity.getCamp(),srcEntity.tongDBID,srcEntity.playerDBID,srcEntity.base )
	
def gmSendMail( srcEntity, dstEntity, args ):
	"""
	发送邮件
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	try:
		argList = args.split()
		itemID = int(argList[0])
		amount = int( argList[1] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/sendMail ItemID, amount"))
		return
		
	itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount, {})
	if not itemInst:
		srcEntity.statusMessage( csstatus.GM_ITEMID_DONT_EXIST,"" )
		return
	
	srcEntity.sendRemainItemWithMail([itemInst], csdefine.REMAIN_ITEM_DROPBOX, csdefine.ITEM_ADD_BY_PICKUP)
	
def gmAddPetExp( srcEntity, dstEntity, args ):
	"""
	添加出战幻兽经验
	"""
	try:
		argList = args.split()
		exp = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/addPetExp exp"))
		return
	srcEntity.addPetExp( exp, csdefine.EXP_ADD_REASON_GM_SET )
	
def gmSetPetStep( srcEntity, dstEntity, args ):
	"""
	设置出战幻兽介次
	"""
	try:
		argList = args.split()
		step = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setPetStep step"))
		return
	srcEntity.setPetStep( step )

def gmOccupyTrainGround( srcEntity, dstEntity, args ):
	"""
	占领某个练兵场
	"""
	argList = args.split()
	if not len( argList ):
		return

	KBEngine.globalData["TrainSoldierGroundManager"].addOccupyTrainSoldierGroundDatas( int(argList[0]),int(argList[1]),srcEntity.playerDBID,srcEntity.getName(),srcEntity.getProfession(),srcEntity.base )

def gmClearOccupyTrainGround( srcEntity, dstEntity, args ):
	"""
	清除某个练兵场
	"""
	argList = args.split()
	if not len( argList ):
		return

	KBEngine.globalData["TrainSoldierGroundManager"].addOccupyTrainSoldierGroundDatas( int(argList[0]),int(argList[1]),0,"",0,srcEntity.base )

def gmSetYCJMDBossLevel( srcEntity, dstEntity, args ):
	"""
	设置勇闯绝命岛boss等级
	"""
	argList = args.split()
	if not len( argList ):
		return
	dstEntity.setYCJMDBossLevel( int(argList[0]) )
	
def gmAddTongMember( srcEntity, dstEntity, args ):
	"""
	增加帮会成员
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	try:
		argList = args.split()
		amount = int( argList[0] )
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/addTongMember amount"))
		return
	
	if srcEntity.tongMB is None:
		return
	
	srcEntity.tongMB.gmAddMember(amount, srcEntity)
	
def gmSendMailByID( srcEntity, dstEntity, args ):
	"""
	发送邮件通过邮件ID
	"""
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	try:
		argList = args.split()
		mailID = argList[0]
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/sendMailByID mailID"))
		return
	
	g_mailContentDataLoader._sendMail(mailID, dstEntity.getName())
	
def gmClearTTT( srcEntity, dstEntity, args ):
	"""
	清理通天塔任务
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	srcEntity.isChallenge = 0
	srcEntity.clearAbandonQuest()

def gmStatusMsg( srcEntity, dstEntity, args ):
	"""
	发送消息提示
	"""
	argList = args.split()
	if not len( argList ):
		return
	srcEntity.statusMessage( int(argList[0]),"" )
	
def gmSetDongFuGroup( srcEntity, dstEntity, args ):
	"""
	设置需要寻找的洞府group
	"""
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	
	try:
		argList = args.split()
		group = argList[0]
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/setDongFuGroup group"))
		return
	lineNumber = srcEntity.getCurrentSpace().spaceKey
	KBEngine.globalData["SpaceLunHuiMiJinMgr"].gmSetOccupiedFoundation( srcEntity, int(lineNumber), int(group) )

def gmClearBuildTime( srcEntity, dstEntity, args ):
	"""
	设置需要寻找的洞府group
	"""
	if dstEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
	for buildType in srcEntity.buildUpgradeTime.keys():
		srcEntity.upgradeBuildSuccess( buildType )
		
def gmOpenWin( srcEntity, dstEntity, args ):
	"""
	打开/关闭界面
	这个没必要加服务器的，客户端强烈要加
	"""
	try:
		argList = args.split()
		winID = argList[0]
		isopen = int(argList[1])
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/openWin winID 0/1"))
		return
	
	srcEntity.client.OnOpenWindow(winID, isopen)

def gmAddequip( srcEntity, dstEntity, args ):
	"""
	手写装备自定义强化星级
	"""
	strList = args.split()
	itemID = 0	
	posture = 0
	goldStar = 0
	silverStar = 0
	copperStar = 0
	ironStar = 0
	mainValueRange = 0
	try:
		itemID = int(strList[0])
		if len(strList) > 1:
			posture = int(strList[1])
		if len(strList) > 2:
			starList = strList[2].split("|")
			goldStar = int(starList[0])
			if len(starList) > 1:
				silverStar = int(starList[1])
			if len(starList) > 2:
				copperStar = int(starList[2])
			if len(starList) > 3:
				ironStar = int(starList[3])
		if len(strList) > 3:
			mainValueRange = int(strList[3])
		if mainValueRange > 3 or mainValueRange < 0:
			raise Exception("out of range")
	except:
		srcEntity.statusMessage( csstatus.GM_ARGS_TYPE_ERROR,"" )
		return	
	posture = posture if posture !=0 else random.choice([1,2])
	srcEntity.customIntensifyEquip( itemID, posture, goldStar, silverStar, copperStar, ironStar, mainValueRange )

def gmAddPassiveSkill( srcEntity, dstEntity, args ):
	"""
	学习主动技能
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/addPassiveSkill  SkillID" ))
		return
	skill = srcEntity.getSkill( int(argList[0]) )
	if skill is None:
		srcEntity.statusMessage( csstatus.SKILL_NOT_EXIST )
		return
	if srcEntity.learnPassiveSkill( int(argList[0]) ):
		srcEntity.statusMessage( csstatus.ADD_SKILL_SUCESS )
	else:
		srcEntity.statusMessage( csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR )

def gmRemovePassiveSkill( srcEntity, dstEntity, args ):
	"""
	遗忘主动技能
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/removePassiveSkill  SkillID" ))
		return
	skill = srcEntity.getSkill( int(argList[0]) )
	if skill is None:
		srcEntity.statusMessage( csstatus.SKILL_NOT_EXIST )
		return
	if srcEntity.forgetPassiveSkill( int(argList[0]) ):
		srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS )
		
def gmGotoMagicMainSpace( srcEntity, dstEntity, args ):
	"""
	进入指定的幻阵迷宫主副本
	"""
	try:
		argList = args.split()
		needLevel = int(argList[0])
		indexStr = argList[1]
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/gotoMagicMainSpace level index"))
		return
	
	if srcEntity.getLevel() < needLevel:
		return
	
	spaceLevel = min( needLevel+19, srcEntity.getLevel() )	#怪物等级上限为副本开放等级+19级（CST-2880）
	dataCfg = LoadModule.openJsonCfg("MagicMazeConfig/MagicMazeConfig.json")
	mainScriptID = dataCfg.get( indexStr,{} ).get("mainSpace","")
	if srcEntity.isInTeam():
		globalRecord = KBEngine.globalData["MagicMazeParentSpaceGlobalRecord"]
		belongType = csdefine.SPACE_BELONG_TEAM
		spaceKey = str( srcEntity.teamMailbox.id )
		if (belongType, spaceKey,mainScriptID) in globalRecord:	# 存在副本
			pickArg = { "packBelongType": belongType, "spaceKey":spaceKey, "players":{ srcEntity.playerDBID: srcEntity.base },"mainScriptID":mainScriptID }
			KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeSpace(belongType, spaceKey, pickArg)
		else:
			if not srcEntity.isTeamCaptain():	# 副本不存在的情况下，这里一定是队长对话
				ERROR_MSG("player is not captain!")
				return
			teammates = {}
			for memMB in srcEntity.getAllTeamMemberMB():
				memPlayer = KBEngine.entities.get( memMB.id, None )
				if memPlayer:
					teammates[ memPlayer.playerDBID ] = memMB
			pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "players": teammates, "mainSpace":indexStr,"mainScriptID":mainScriptID}
			KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeSpace(belongType, spaceKey, pickArg)
	else:
		belongType = csdefine.SPACE_BELONG_PERSON
		spaceKey = str( srcEntity.playerDBID )
		pickArg = { "packBelongType": belongType, "packSpaceLevel": spaceLevel, "spaceKey":spaceKey, "players":{ srcEntity.playerDBID: srcEntity.base },"mainSpace":indexStr,"mainScriptID":mainScriptID}
		KBEngine.globalData["MagicMazeSpaceManager"].gotoMagicMazeSpace(belongType, spaceKey, pickArg)	
		
def gmEnterBHZBStandMap( srcEntity, dstEntity, args ):
	"""
	"""
	srcEntity.requestGotoStandMapPoint( srcEntity.id, (0,0,0) )

def gmControlActivity( srcEntity, dstEntity, args ):
	"""
	控制 活动管理器
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/activity  scriptID" ))
		return
	scriptID = argList[0]
	KBEngine.globalData["CrondManager"].callSchemeByScriptID( scriptID )
	
def gmCompleteLoopQuestBefore( srcEntity, dstEntity, args ):
	"""
	完成指定环任务队列中某任务之前的任务
	"""
	try:
		argList = args.split()
		questID = int(argList[0])
	except:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS, str("/completeLoopQuestBefore questID"))
		return
	
	while True:
		if len(srcEntity.loopQuest["loopQuestList"]) <= 0:
			break
		
		id = srcEntity.loopQuest["loopQuestList"][0]
		
		if id not in srcEntity.questTable:
			srcEntity.acceptQuest( id )
			
		if id == questID:
			break
		
		quest = srcEntity.questTable.get( id )
		if quest is None:
			break
		
		quest.setDone( srcEntity )
		srcEntity.commitQuest( id )
	
	srcEntity.statusMessage(csstatus.GM_COMMAND_SUCCESS)

def gmCloseSpace( srcEntity, dstEntity, args ):
	"""
	关闭当前所在副本地图
	"""
	curSpace = srcEntity.getCurrentSpace()
	if curSpace.getScript().isSpaceCopy():
		curSpace.closeSpace()
		
def gmClearMagicMaze( srcEntity, dstEntity, args ):
	"""
	清理幻阵迷宫进度
	"""
	KBEngine.globalData["MagicMazeSpaceManager"].gmClear()
	srcEntity.statusMessage(csstatus.GM_COMMAND_SUCCESS)

def gmReloadSkillConfigs( srcEntity, dstEntity, args ):
	"""
	技能相关配置热更新
	"""
	from ConfigObject.Skill.EffectLoader import g_effects
	from ConfigObject.Skill.SkillLoader import g_skills
	from ConfigObject.Skill.BuffLoader import g_buffs
	from ConfigObject.Skill.SkillPostureLoader import g_skillPosture
	from ConfigObject.Skill.PassiveSkillBarLoader import g_passiveSkillBars
	if not g_effects.reloadConfig():
		srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_FAIL, "Skill/SkillConfigs/SkillEffectTable.json" )
		return
	if not g_skills.reloadConfig():
		srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_FAIL, "Skill/SkillConfigs/SkillTable.json" )
		return
	if not g_buffs.reloadConfig():
		srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_FAIL, "Skill/SkillConfigs/BuffTable.json" )
		return
	if not g_skillPosture.reloadConfig():
		srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_FAIL, "Skill/SkillConfigs/SkillPostureConfig.json" )
		return
	if not g_passiveSkillBars.reloadConfig():
		srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_FAIL, "Skill/SkillConfigs/PassiveSkillBarData.json" )
		return
	srcEntity.statusMessage( csstatus.GM_CONFIG_RELOAD_SUCCESS )

def gmClearDFData( srcEntity, dstEntity, args ):
	"""
	技能相关配置热更新
	"""
	KBEngine.globalData["SpaceLunHuiMiJinMgr"].GM_clearDFData()
	
	
def gmSetPayGameTime(srcEntity, dstEntity, args):
	"""
	设置付费时长
	"""
	
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setPayGameTime num" ) )
		return
		
	srcEntity.base.GMSetPayGameTime(int(argList[0]))
	
def gmSetDefaultGameTime(srcEntity, dstEntity, args):
	"""
	设置付费时长
	"""
	
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setDefaultGameTime num" ) )
		return
		
	srcEntity.base.GMSetDefaultGameTime(int(argList[0]))

def gmUpgradeDFBuild(srcEntity, dstEntity, args):
	"""
	升级洞府建筑
	"""
	
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/upgradeDFBuild type(type:1为灵泉，2为工坊，3为乾坤鼎，4为兽栏，5为灵田)" ) )
		return
		
	srcEntity.upgradeBuildSuccess(int(argList[0]))
	
def gmDoDefaultDFChallenge(srcEntity, dstEntity, args):
	"""
	d洞府所有挑战默认同意
	"""
	KBEngine.globalData["SpaceLunHuiMiJinMgr"].GM_doDefaultDFChallenge()
	
def gmOpenRandomShop(srcEntity, dstEntity, args):
	"""
	开启随机商店
	"""
	KBEngine.globalData["ShopManager"].GM_openRandomShop()

def gmDeclareBHZBPoint( srcEntity, dstEntity, args ):
	"""
	宣战帮会争霸据点
	"""
	argList = args.split()
	if len(argList) != 2:
		return
	#KBEngine.globalData["BHZBManager"].declareBHZBPoint( srcEntity.tongDBID, srcEntity.getCamp(), int(argList[0]),srcEntity.base,srcEntity.playerDBID, srcEntity.getName(),srcEntity.tongName )
	srcEntity.declareBHZBPoint( srcEntity.id, int(argList[0]), int( argList[1] ) )

def gmCancelBHZBPoint( srcEntity, dstEntity, args ):
	"""
	取消宣战帮会争霸据点
	"""
	argList = args.split()
	if not len(argList):
		return
	srcEntity.cancelDeclareBHZBPoint( srcEntity.id,int(argList[0]) )
	#KBEngine.globalData["BHZBManager"].cancelDeclareBHZBPoint( srcEntity.tongDBID, srcEntity.getCamp(), int(argList[0]), srcEntity.base, srcEntity.playerDBID )

def gmOccupyBHZBPoint( srcEntity, dstEntity, args ):
	"""
	占领帮会争霸某个据点
	"""
	argList = args.split()
	if not len(argList):
		return

	KBEngine.globalData["BHZBManager"].onBHZBPointWarSuccess( srcEntity.getCamp(), int(argList[0]) )

def gmDefenseBHZBPoint( srcEntity, dstEntity, args ):
	"""
	布防据点帮会某个据点
	"""
	argList = args.split()
	if len(argList) != 2:
		return
	srcEntity.defenseBHZBPoint( srcEntity.id, int( argList[0] ), int( argList[1] ))

def gmJoinDefenseBHZBPoint( srcEntity, dstEntity, args ):
	"""
	回防
	"""
	argList = args.split()
	if len(argList) != 2:
		return
	srcEntity.joinBHZBPointFight( srcEntity.id,int( argList[0] ), int( argList[1] ) )

def gmSetTongSafeTime( srcEntity, dstEntity, args ):
	"""
	设置帮会安全期剩余天数
	"""
	argList = args.split()
	if len(argList) != 1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setTongSafeTime time(time为安全期天数，需大于或等于0)" ) )
		return
	if not int(argList[0]) >= 0:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setTongSafeTime time(time为安全期天数，需大于或等于0)" ) )
		return
	if srcEntity.tongMB is None:
		return
	srcEntity.tongMB.gmSetSafeTime(int(argList[0]))
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS )

def gmSetTongProtectDay( srcEntity, dstEntity, args ):
	"""
	设置帮会保护期剩余天数
	"""
	argList = args.split()
	if len(argList) != 1:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setTongProtectDay day(day为保护期天数，需大于或等于0)" ) )
		return
	if not int(argList[0]) >= 0:
		srcEntity.statusMessage( csstatus.GM_FORMAT_TIPS , str( "/setTongProtectDay day(day为保护期天数，需大于或等于0)" ) )
		return
	if srcEntity.tongMB is None:
		return
	srcEntity.tongMB.gmSetProtectDay(int(argList[0]))
	srcEntity.statusMessage( csstatus.GM_COMMAND_SUCCESS )


def gmGotoLbc( srcEntity, dstEntity, args ):
	"""
	前往练兵场
	"""
	argsList = args.split()
	line, index = int(argsList[0]), int(argsList[1])
	srcEntity.reqGotoLbc(srcEntity, line, index)

def gmOccupyLbc( srcEntity, dstEntity, args ):
	"""
	占领练兵场（中高级）
	"""
	argsList = args.split()
	line, index = int(argsList[0]), int(argsList[1])
	KBEngine.globalData['LbcMgr'].occupy(srcEntity, line, index)

def gmOccupyLbcLow( srcEntity, dstEntity, args ):
	"""
	占领初级练兵场
	"""
	argsList = args.split()
	line, index = int(argsList[0]), int(argsList[1])
	#放弃原先的练兵场
	srcEntity.abandonLbc()
	
	#占领新的练兵场
	KBEngine.globalData['LbcMgr'].attackerWin(line, index, srcEntity, srcEntity.playerDBID, srcEntity.playerName, srcEntity.profession)
	

def gmDeclareLbc( srcEntity, dstEntity, args ):
	"""
	宣战练兵场
	"""
	argsList = args.split()
	line, index = int(argsList[0]), int(argsList[1])
	KBEngine.globalData['LbcMgr'].declare(srcEntity, line, index, srcEntity.playerDBID, srcEntity.playerName, srcEntity.profession)

def gmCancelDeclareLbc(srcEntity, dstEntity, args):
	"""
	撤销练兵场宣战
	"""
	srcEntity.cancelDeclare()


def gmNotifyLbcFightStart(srcEntity, dstEntity, args):
	"""
	通知玩家练兵场争夺战即将开始
	"""
	KBEngine.globalData['LbcMgr'].startFight()

def gmEnterLbcSpace(srcEntity, dstEntity, args):
	"""
	进入练兵场争夺战地图
	"""
	KBEngine.globalData['LbcMgr'].enterSpace()

def gmSureBHZBMember( srcEntity, dstEntity, args ):
	"""
	确认帮会成员
	"""
	getattr(KBEngine.globalData["BHZBManager"],"GMCommand")("onBHZBSureTong")
	getattr(KBEngine.globalData["BHZBManager"],"GMCommand")("onBHZBSureTongMem")

def gmClearBarracksData( srcEntity, dstEntity, args ):
	"""
	清除天兵营中部队数据
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.gmClearBarracksData()
		return

	srcEntity.gmClearBarracksData( argList[0] )
	
def gmCreateTongDropBox( srcEntity, dstEntity, args ):
	"""
	创建帮会宝箱
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	if srcEntity.tongMB is None:
		srcEntity.statusMessage( csstatus.TONG_SPACE_COPY_NOT_IN_TONG )
		return
		
	KBEngine.cellAppData["TONGDROPBOXPOS"] = srcEntity.position
	srcEntity.tongMB.gmCreateTongDropBox()
	
def gmCreateTeamDropBox( srcEntity, dstEntity, args ):
	"""
	创建队伍宝箱
	"""
	if srcEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
		srcEntity.statusMessage( csstatus.GM_SET_ENTITY_ERROR )
		return
		
	if not srcEntity.isInTeam():
		return
		
	reward = {101040145:1, 101040144:1}
	items = {}
	for itemID, amount in reward.items():
		ItemInst = ItemFactory.ItemFactoryInst.createDynamicItem( itemID, amount )
		if ItemInst is None: continue
		items[ItemInst.uid] = ItemInst
	
	dbids = []
	teammates = srcEntity.getInRangeTeammate(150)
	for teammate in teammates:
		dbids.append(teammate.playerDBID)
	if srcEntity.playerDBID not in dbids:
		dbids.append(srcEntity.playerDBID)
	teamCaptainDBID = 0
	for teammate in srcEntity.teamMembers:
		if teammate["mailbox"] and teammate["mailbox"].id == srcEntity.captainID:
			teamCaptainDBID = teammate["dbID"]
			break
	
	args = {
		"freeAllocationItems"	: {},
		"notAllocationItems"	: items,
		"teamID"				: srcEntity.teamMailbox.id,
		"allocation"			: srcEntity.allocation,
		"ownerDBIDs"			: dbids,
		"modelScale"			: Const.GREEN_DROPBOX_START_SCALE,
		"modelNumber"			: "SK_ZW0245_2_NPC",	
		"teamCaptainDBID"		: teamCaptainDBID,
	}
	position = tuple(Math.Vector3(srcEntity.position))
	dropbox = srcEntity.createEntityNear("TeamDropBox", position, srcEntity.direction, args)
	if dropbox is None:
		KBEDebug.ERROR_MSG("Create Team DropBox Fail")
		return

def gmSignUpGCZ( srcEntity, dstEntity, args ):
	"""
	报名帮会争霸
	"""
	KBEngine.globalData["GCZManager"].signUpGCZ( 1,srcEntity.base,srcEntity.playerDBID,50,"18:30" )

def gmBattleActivityInterrupt(srcEntity, dstEntity, args):
	"""
	团队竞技取消报名
	"""
	srcEntity.base.battleActivityInterrupt()

def gmSetTJMTToPlace(srcEntity, dstEntity, args):
	"""
	使用天机秘图到指定的地图
	"""
	argList = args.split()
	if len(argList) != 1:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS, str("/setTJMIToPlace JiYuanConfigID(JiYuanConfigID为机缘配置文件的ID"))
		return
	Data = g_jiYuanCfgLoader.getCfgByID(argList[0])
	if Data == None:
		return
	srcEntity.setTemp("JiYuanXinXi", str(argList[0]))
	srcEntity.statusMessage(csstatus.GM_COMMAND_SUCCESS)

def gmSetDFRepairTime(srcEntity, dstEntity, args):
	"""
	设置洞府建筑恢复时间
	"""
	argList = args.split()
	if not len(argList):
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS , str( "/setDFRepairTime  time" ))
		return
	time = int(argList[0])
	if time < 5:
		time = 5	#给5秒反应时间
	srcEntity.gmSetDFRepairTime( time )

def gmAddBHZBTongIntegralRecordStartTimes( srcEntity, dstEntity, args ):
	"""
	增加帮会争霸战报记录
	"""
	getattr(KBEngine.globalData["BHZBManager"],"GMCommand")("gmAddBHZBTongIntegralRecordStartTimes")

def gmClearBHZBTongIntegralRecord( srcEntity, dstEntity, args ):
	"""
	清除帮会争霸战报记录
	"""
	getattr(KBEngine.globalData["BHZBManager"],"GMCommand")("gmClearBHZBTongIntegralRecord")

def gmChangeActivityRecordDegree( srcEntity, dstEntity, args ):
	"""
	改变活动副本的参与次数
	"""
	argList = args.split()
	if len(argList) > 1:
		KBEngine.cellAppData[int(argList[0])] = int(argList[1])
	else:
		srcEntity.statusMessage(csstatus.GM_FORMAT_TIPS, str("/changeActivityRecordDegree 活动类型 活动次数"))

def ADD_COMMAND( cmd, grade, func ):
	"""
	@param cmd:string
	@param cmd:GM命令
	@param grade:int
	@param grade:当前GM命令的权限执行等级
	@param func:string
	@param func:GM命令对应的执行函数
	"""
	assert cmd not in g_gmCommandDict
	g_gmCommandDict[cmd] = ( grade, func )

# 增加命令字典
# **********************************begin of ADD_COMMAND**********************************
ADD_COMMAND( "goto",					20 , gmCommandGotoSpace )
ADD_COMMAND( "gotoRingTask",			20 , gmCommandGotoSpaceRingTask )
ADD_COMMAND( "gotoPoint",				20 , gmCommandGotoPoint )
ADD_COMMAND( "GOTO",					20 , gmCommandGotoSpaceUseServerPos )
ADD_COMMAND( "enterPlane",				20 , gmCommandEnterPlane )
ADD_COMMAND( "gotoPlane",				20 , gmCommandGotoPlane )
ADD_COMMAND( "gotoBunch",				20 , gmCommandGotoBunchSpace )
ADD_COMMAND( "setNextBunchSpace",		20 , gmCommandSetNextSpace )
ADD_COMMAND( "clearBunchRecord",		20 , gmCommandClearBunchRecord )
ADD_COMMAND( "clone",					20 , gmCommandClone )
ADD_COMMAND( "clone1",					20 , gmCommandClone1 )
ADD_COMMAND( "clone2",					20 , gmCommandClone2 )
ADD_COMMAND( "createBaseMonster",		20 , gmCommandCreateBaseMonster )
ADD_COMMAND( "set_attr",				20 , gmCommandSetAttr )
ADD_COMMAND( "query_attr",				20 , gmCommandQueryAttr )
ADD_COMMAND( "setAttr",					20 , gmCommandSetAttr )					#新增一批更规范的命令命名，以供策划同人适应
ADD_COMMAND( "queryAttr",				20 , gmCommandQueryAttr )				#新增一批更规范的命令命名，以供策划同人适应
ADD_COMMAND( "revive",					20 , gmCommandReviveOnOrigin )
ADD_COMMAND( "addItem",					20 , gmCommandAddItem )
ADD_COMMAND("addReward", 				20,  gmCommandAddReward)
ADD_COMMAND("addRewardSelf", 			20,  gmCommandAddRewardSelf)
ADD_COMMAND( "dropBox",					20 , gmCommandDropBox )
ADD_COMMAND( "spell",					20 , gmCommandSpell )
ADD_COMMAND( "spellSelf",				20 , gmCommandSpellSelf )
ADD_COMMAND( "spellItself",				20 , gmCommandSpellItself )
ADD_COMMAND( "spellItSelf",				20 , gmCommandSpellItself )				#新增一批更规范的命令命名，以供策划同人适应
ADD_COMMAND( "addEffect",				20 , gmCommandAddEffect )
ADD_COMMAND( "addEffectSelf",			20 , gmCommandAddEffectSelf )
ADD_COMMAND( "addEffectItSelf",			20 , gmCommandAddEffectItSelf )
ADD_COMMAND( "set_money",				20 , gmCommandSetMoney )
ADD_COMMAND( "set_level",				20 , gmCommandSetLevel )
ADD_COMMAND( "set_xiuwei",				20 , gmCommandSetXiuwei )
ADD_COMMAND( "setMoney",				20 , gmCommandSetMoney )				#新增一批更规范的命令命名，以供策划同人适应
ADD_COMMAND( "setBindMoney",			20 , gmCommandSetBindMoney )
ADD_COMMAND( "setPotential",			20 , gmCommandSetPotential )				#新增一批更规范的命令命名，以供策划同人适应
ADD_COMMAND( "setLevel",				20 , gmCommandSetLevel )				#新增一批更规范的命令命名，以供策划同人适应
ADD_COMMAND( "setXiuwei",				20 , gmCommandSetXiuwei )				#新增一批更规范的命令命名，以供策划同人适应
ADD_COMMAND( "setExploit",				20 , gmCommandSetExploit )
ADD_COMMAND( "setMaxMilitaryRank",		20 , gmCommandSetMaxMilitaryRank )
ADD_COMMAND( "remove_completed_quest",	20 , gmCommandRemoveCompletedQuest )
ADD_COMMAND( "accept_quest",			20 , gmCommandAcceptQuest )
ADD_COMMAND( "complete_quest",			20 , gmCommandCompleteQuest )
ADD_COMMAND( "complete_autoQuest",		20 , gmCommandCompleteAutoQuest )
ADD_COMMAND( "completeTask",			20 , gmCommandCompleteTask )
ADD_COMMAND( "completeStageTask",		20 , gmCommandCompleteStageTask )
ADD_COMMAND( "acceptLoopQuest",			20 , gmCommandAcceptLoopQuest )
ADD_COMMAND( "setAQuestFlag",			20 , gmCommandSetAQuestFlag )
ADD_COMMAND( "setDebugFlag",			20 , gmCommandSetDebugFlag )
ADD_COMMAND( "sendAI",					20 , gmCommandSendAI )
ADD_COMMAND( "triggerEvent",			20 , gmCommandTriggerEvent )
ADD_COMMAND( "smash",					20 , gmCommandSmash )
ADD_COMMAND( "del",						20 , gmCommandSmash )
ADD_COMMAND( "setSpeed",				20 , gmCommandSetSpeed )
ADD_COMMAND( "addFlag",					20 , gmCommandAddFlag )
ADD_COMMAND( "delFlag",					20 , gmCommandDelFlag )
ADD_COMMAND( "setModel",				20 , gmCommandSetModel )
ADD_COMMAND( "setScale",				20 , gmCommandSetScale )
ADD_COMMAND( "setPos",					20 , gmCommandSetPos )
ADD_COMMAND( "setDir",					20 , gmCommandSetDir )
ADD_COMMAND( "watch",					20 , gmCommandWatch )
ADD_COMMAND( "showInvisible",			20 , gmCommandShowInvisible )
ADD_COMMAND( "hideInvisible",			20 , gmCommandHideInvisible )
ADD_COMMAND( "reloadAI",				20 , gmReloadAI )
ADD_COMMAND( "reloadQuest",				20 , gmReloadQuest )
ADD_COMMAND( "reloadTalk",				20 , gmReloadTalk )
ADD_COMMAND( "reloadEntity",			20 , gmReloadEntity )
ADD_COMMAND( "reloadScript",			20 , gmReloadScript )
ADD_COMMAND( "reloadConfig",			20 , gmReloadConfig )
ADD_COMMAND( "playSound",				20 , gmCommandPlaySound )
ADD_COMMAND( "queryFlag",				20 , gmCommandQueryFlag )
ADD_COMMAND( "addBuff",					20 , gmCommandAddBuff )
ADD_COMMAND( "addBuffSelf",				20 , gmCommandAddBuffSelf )
ADD_COMMAND( "addBuffItSelf",			20 , gmCommandAddBuffItSelf )
ADD_COMMAND( "clearBuff",				20 , gmCommandClearBuff )
ADD_COMMAND( "queryBuff",				20 , gmCommandQueryBuff )
ADD_COMMAND( "full",					20 , gmCommandFull )
ADD_COMMAND( "clearBag",				20 , gmCommandClearBag )
ADD_COMMAND( "addSkill",				20 , gmCommandAddSkill )
ADD_COMMAND( "addSkillForQuest",		20 , gmCommandAddSkillForQuest )
ADD_COMMAND( "removeSkill",				20 , gmCommandRemoveSkill )
ADD_COMMAND( "playAction",				20 , gmCommandPlayAction )
ADD_COMMAND( "playRandomAction",		20 , gmCommandPlayRandomAction )
ADD_COMMAND( "stopAction",				20 , gmCommandStopAction )
ADD_COMMAND( "stopFrontAction",			20 , gmCommandStopFrontAction )
ADD_COMMAND( "queryRelation",			20 , gmCommandQueryRelation )
ADD_COMMAND( "playParticle",			20 , gmCommandPlayParticle )
ADD_COMMAND( "setHP",	 				20 , gmSetHP )
ADD_COMMAND( "addTitle",	 			20 , gmAddTitle )
ADD_COMMAND( "removeTitle",	 			20 , gmRemoveTitle )
ADD_COMMAND( "playOneByOneAction",	 	20 , gmCommandPlayOneByOneAction )
ADD_COMMAND( "setAdult",			 	20 , gmCommandSetAdult )
ADD_COMMAND( "tongCreate",			 	20 , gmCommandTongCreate )
ADD_COMMAND( "tongQuit",			 	20 , gmCommandTongQuit )
ADD_COMMAND( "tongDismiss",			 	20 , gmCommandTongDisMiss )
ADD_COMMAND( "activity_control", 	 	20 , gmCommandActivity_control)
ADD_COMMAND( "clearCD",					20 , gmCommandEliminateCD )
ADD_COMMAND( "clearPetSleep",			20 , gmCommandClearPetSleep )
ADD_COMMAND( "setMagicMazeChild",		20 , gmCommandSetMagicMazeChild )
ADD_COMMAND( "setTongAttr",				20 , gmCommandSetTongAttr )
ADD_COMMAND( "reloadFaZhenCf",			20 , gmCommandRelaodFaZhenCf )
ADD_COMMAND( "showRole",				20 , gmCommandShowRole )
ADD_COMMAND( "setRoleSpaceRelationRule",20 , gmCommandSetRoleSpaceRelationRule )
ADD_COMMAND( "setXianShi",				20 , gmCommandSetXianShi )
ADD_COMMAND( "setLingShi",				20 , gmCommandSetLingShi )
ADD_COMMAND( "setXuanShi",				20 , gmCommandSetXuanShi )
ADD_COMMAND( "setSyncPosToOtherClient",	20 , gmCommandSetSyncPosToOtherClient )
ADD_COMMAND( "createTeam",				20 , gmCommandCreateTeam )
ADD_COMMAND( "testMonsterFight",		20 , gmCommandTestMonsterFight )
ADD_COMMAND( "checkMemLeak",			20 , gmCommandCheckMemLeak )
ADD_COMMAND( "createMonsterInCircle",	20 , gmCommandCreateMonsterInCircle )
ADD_COMMAND( "openTeleportPoint",		20 , gmCommandOpenTeleportPoint )
ADD_COMMAND( "disbandAllTong",			20 , gmCommandDisbandAllTong )
ADD_COMMAND( "setJumpData",				20 , gmCommandSetJumpData )
ADD_COMMAND( "turnToPos",				20 , gmCommandTurnToPos )
ADD_COMMAND( "startAITick",				20 , gmCommandStartAITick )
ADD_COMMAND( "spell2",					20 , gmCommandSpell2 )
ADD_COMMAND( "fullAll",					20 , gmCommandFullAll )
ADD_COMMAND( "YXLMSignUp",				20 , gmCommandYXLMSignUp )
ADD_COMMAND( "queryLayer",				20 , gmCommandQueryLayer )
ADD_COMMAND( "setCampSwitch",			20 , gmCommandSetCampSwitch )
ADD_COMMAND( "LingMaiSignUp",			20 , gmCommandSetLingMaiSignUp )
ADD_COMMAND( "JSSLCSignUp",				20 , gmCommandSetJSSLCSignUp )
ADD_COMMAND( "enterJSSLC",				20 , gmCommandSetJSSLCEnter )
ADD_COMMAND( "setWXHJ",					20 , gmCommandSetWXHJ )
ADD_COMMAND( "queryWXHJ",				20 , gmCommandQueryWXHJ )
ADD_COMMAND( "setVIP",					20 , gmCommandSetVIP )
ADD_COMMAND( "querySceneObjectName",	20 , gmCommandQuerySceneObjectName )
ADD_COMMAND( "setSpaceDebugFlag",		20 , gmCommandSetSpaceDebugFlag )
ADD_COMMAND( "query_space",				20 , gmCommandQuerySpace )
ADD_COMMAND( "clearAllActivityRecord",	20 , gmCommandClearAllActivityRecord)
ADD_COMMAND( "SetMiniMapScale",			20 , gmCommandSetMiniMapScale)
ADD_COMMAND( "clearRejoinTongTime",		20 , gmCommandClearRejoinTongForbidTime)
ADD_COMMAND( "setOfflineTime",			20 , gmCommandSetOfflineTime )
ADD_COMMAND( "setOnlineTime",			20 , gmCommandSetOnlineTime )
ADD_COMMAND( "addFoe",					20 , gmCommandAddFoe )
ADD_COMMAND( "queryNavLayer",			20 , gmCommandQuyerNavLayer )
ADD_COMMAND( "follow",					20 , gmCommandFollow )
ADD_COMMAND( "cleanEntity",				20 , gmCommandCleanEntity )
ADD_COMMAND( "showEntityCount",			20 , gmCommandqueryEntityCount )
ADD_COMMAND( "cclone",        			20 , gmCommandCClone )
ADD_COMMAND( "catch",					20 , gmCommandCatchEntity )
ADD_COMMAND( "equipArms",				20 , gmCommandEquipArms )
ADD_COMMAND( "createArms",				20 , gmCommandCreateArms )
ADD_COMMAND( "removeArms",				20 , gmCommandRemoveArms )
ADD_COMMAND( "move_CST_9506",			20 , gmCommandMove_CST_9506Cmd )
ADD_COMMAND( "leadArms",				20 , gmCommandLeadArms )
ADD_COMMAND( "createSoldiers",			20 , gmCommandCreateSoldiers )
ADD_COMMAND( "finishCompose",			20 , gmCommandFinishCompose )
ADD_COMMAND( "clearPetCDTime",			20 , gmCommandClearPetCDTime )
ADD_COMMAND( "findRole",				20 , gmCommandFindRole )
ADD_COMMAND( "TestEffect",				20 , gmCommandTestEffect )
ADD_COMMAND( "reloadConst",				20 , gmReloadHotConst )
ADD_COMMAND( "notifyTrainWar",			20 , gmNotifyDeclareWarPlayer )
ADD_COMMAND( "climb",					20 , gmClimb )
ADD_COMMAND( "signUPBHZB", 				20 , gmSignUpBHZB )
ADD_COMMAND( "enterBHZBHomeBarracks",   20 , gmEnterBHZBHomeBarracks )
ADD_COMMAND( "sendMail",  				20 , gmSendMail )
ADD_COMMAND( "addPetExp", 				20 , gmAddPetExp )
ADD_COMMAND( "setPetStep",  			20 , gmSetPetStep )
ADD_COMMAND( "occupyTrainGround",  		20 , gmOccupyTrainGround )
ADD_COMMAND( "clearOccupyTrainGround",  20 , gmClearOccupyTrainGround )
ADD_COMMAND( "setYCJMDBossLevel",  		20 , gmSetYCJMDBossLevel )
ADD_COMMAND( "addTongMember",  			20 , gmAddTongMember )
ADD_COMMAND( "sendMailByID",  			20 , gmSendMailByID )
ADD_COMMAND( "clearTTT",  				20 , gmClearTTT )
ADD_COMMAND( "statusMsg", 				20 , gmStatusMsg )
ADD_COMMAND( "setDongFuGroup", 			20 , gmSetDongFuGroup )
ADD_COMMAND( "clearBuildTime", 			20 , gmClearBuildTime )
ADD_COMMAND( "openWin", 				20 , gmOpenWin )
ADD_COMMAND( "addequip", 				20 , gmAddequip )
ADD_COMMAND( "addEquip", 				20 , gmAddequip )
ADD_COMMAND( "addPassiveSkill", 		20 , gmAddPassiveSkill )
ADD_COMMAND( "removePassiveSkill", 		20 , gmRemovePassiveSkill )
ADD_COMMAND( "gotoMagicMainSpace", 		20 , gmGotoMagicMainSpace )
ADD_COMMAND( "enterBHZBStandMap", 		20 , gmEnterBHZBStandMap )
ADD_COMMAND( "activity", 				20 , gmControlActivity )
ADD_COMMAND( "completeLoopQuestBefore",	20 , gmCompleteLoopQuestBefore )
ADD_COMMAND( "closeSpace",				20 , gmCloseSpace )
ADD_COMMAND( "gotoMagicMazeChild",		20 , gmCommandGotoMagicMazeChild )
ADD_COMMAND( "clearMagicMaze",			20 , gmClearMagicMaze )
ADD_COMMAND( "reloadSkillConfigs",		20 , gmReloadSkillConfigs )
ADD_COMMAND( "reloadSkill",				20 , gmReloadSkillConfigs )
ADD_COMMAND( "clearDFData",				20 , gmClearDFData )
ADD_COMMAND( "setPayGameTime",			20 , gmSetPayGameTime )
ADD_COMMAND( "setDefaultGameTime",		20 , gmSetDefaultGameTime )
ADD_COMMAND( "upgradeDFBuild",			20 , gmUpgradeDFBuild )
ADD_COMMAND( "doDefaultDFChallenge",	20 , gmDoDefaultDFChallenge )
ADD_COMMAND( "openRandomShop",			20 , gmOpenRandomShop )
ADD_COMMAND( "declareBHZBPoint",  	 	20 , gmDeclareBHZBPoint )
ADD_COMMAND( "cancelBHZBPoint",  	 	20 , gmCancelBHZBPoint )
ADD_COMMAND( "occupyBHZBPoint", 		20 , gmOccupyBHZBPoint)
ADD_COMMAND( "defenseBHZBPoint",  		20 , gmDefenseBHZBPoint )
ADD_COMMAND( "joinDefenseBHZBPoint",  	20 , gmJoinDefenseBHZBPoint )
ADD_COMMAND( "setTongSafeTime",  	 	20 , gmSetTongSafeTime )
ADD_COMMAND( "setTongProtectDay",  	 	20 , gmSetTongProtectDay )
ADD_COMMAND( "gotoLbc",  	 			20 , gmGotoLbc )
ADD_COMMAND( "occupyLbc",  	 			20 , gmOccupyLbc )
ADD_COMMAND( "occupyLbcLow",  	 		20 , gmOccupyLbcLow )
ADD_COMMAND( "declareLbc",  	 		20 , gmDeclareLbc )
ADD_COMMAND( "cancelDeclareLbc",  	 	20 , gmCancelDeclareLbc )
ADD_COMMAND( "notifyLbcFightStart",  	20 , gmNotifyLbcFightStart )
ADD_COMMAND( "enterLbcSpace",  			20 , gmEnterLbcSpace )
ADD_COMMAND( "sureBHZBMember",        	20 , gmSureBHZBMember )
ADD_COMMAND( "clearBarracksData",       20 , gmClearBarracksData )
ADD_COMMAND( "createTongDropBox",       20 , gmCreateTongDropBox )
ADD_COMMAND( "createTeamDropBox",       20 , gmCreateTeamDropBox )
ADD_COMMAND( "signUpGCZ",       		20 , gmSignUpGCZ )
ADD_COMMAND( "battleActivityInterrupt",       		20 , gmBattleActivityInterrupt )
ADD_COMMAND( "setTJMTToPlace",          20 ,  gmSetTJMTToPlace)
ADD_COMMAND( "setDFRepairTime",       	20 , gmSetDFRepairTime )
ADD_COMMAND( "addBHZBTongIntegralRecordStartTimes",20, gmAddBHZBTongIntegralRecordStartTimes )
ADD_COMMAND( "clearBHZBTongIntegralRecord",20, gmClearBHZBTongIntegralRecord )
ADD_COMMAND( "changeActivityRecordDegree", 20, gmChangeActivityRecordDegree )

# **********************************end of ADD_COMMAND************************************
def executeGMCommand( srcEntity, dstEntityID, command, args ):
	"""
	执行一条GM命令
	@param	srcEntity:		Entity
	@param	srcEntity:		GM命令使用者
	@param	dstEntityID:	OBJECT_ID
	@param	dstEntityID:	目标entityID
	@param	command:		STRING
	@param	command:		GM命令
	@param	args:			STRING
	@param	args:			命令参数表,根据不同命令有不同的格式,各命令自行解释
	"""
	dstEntity = KBEngine.entities.get( dstEntityID, None )
	if dstEntityID == srcEntity.id or dstEntity == None:
		dstEntity = srcEntity
	if not command in g_gmCommandDict:
		srcEntity.statusMessage( csstatus.GM_CANNOT_FIND_COMMAND,"")													#GM命令没有定义
		return

	grade, func = g_gmCommandDict[command]
	if srcEntity.grade < grade:
		srcEntity.statusMessage( csstatus.GM_COMMAND_GRADE_NOT_ENOUGH,grade,srcEntity.grade)
		return
	func( srcEntity, dstEntity, args )																					#执行指令函数

activity_dict = {
		csdefine.ACTIVITY_SPAR_HUNTING_SIGNUP:("SparHunTingManager","onActiveSignUp","onActiveSignUpEnd"),
		csdefine.ACTIVITY_SPAR_HUNTING:( "SparHunTingManager","onActiveStart","onActiveEnd" ),
		csdefine.ACTIVITY_CAMP_LING_MAI:( "CampActivityLingMaiMgr","onActiveStart","onActiveEnd" ),
		csdefine.ACTIVITY_CAMP_FROZEN_FIGHT:( "CampActivityFrozenFightMgr","onActiveStart","onActiveEnd" ),
		csdefine.ACTIVITY_CAMP_YXLM:( "CampYXLMCopyMgr","onActiveStart","onActiveEnd"),
		csdefine.ACTIVITY_YE_ZHAN_FENG_QI:( "PersonStarcraftMgr","onYeZhanFengQiStart","onYeZhanFengQiEnd" ),
		csdefine.ACTIVITY_SHI_FANG_CHENG_SIGN_UP:( "PersonStarcraftMgr","onShiFangChengActiveSignUpStart","onShiFangChengActiveSignUpEnd" ),
		csdefine.ACTIVITY_SHI_FANG_CHENG_START:( "PersonStarcraftMgr","onShiFangChengActiveStart","onShiFangChengActiveEnd" ),
		csdefine.ACTIVITY_FIRST_TONG_STARCRAFT_SIGNUP:( "TongStarcraftManager7904","onFirstTongStarcraftSignUpStart","onFirstTongStarcraftSignUpEnd" ),
		csdefine.ACTIVITY_FIRST_TONG_STARCRAFT_START:( "TongStarcraftManager7904","onFirstTongStarcraftStart","onFirstTongStarcraftEnd" ),
		csdefine.ACTIVITY_CAMP_RANDOM_FIT:( "CampActivityRandomFitMgr","onActiveStart","onActiveEnd"),
		csdefine.ACTIVITY_BHZB_SIGN_UP:("BHZBManager","onBHZBSignUpStart","onBHZBSignUpEnd"),
		csdefine.ACTIVITY_BHZB_START:( "BHZBManager","onBHZBStart","onBHZBEnd" ),
		csdefine.ACTIVITY_TONG_PLUNDER_SIGN_UP:( "TongPlunderManager","onActiveSignUp","onActiveSignUpEnd" ),
		csdefine.ACTIVITY_TONG_PLUNDER_START:( "TongPlunderManager","onActiveStart","onActiveEnd" ),
		csdefine.ACTIVITY_TONG_PLUNDER_LOCK_SHOP:( "TongPlunderManager","onLockTongShopStart","onLockTongShopEnd" ),
		csdefine.ACTIVITY_TONG_PLUNDER_SHOP_SELL:( "TongPlunderManager","onTongPlunderShopSellStart","onTongPlunderShopSellEnd" ),
		csdefine.ACTIVITY_GCZ_SIGNUP:( "GCZManager","onGCZSignUpStart","onGCZSignUpEnd" ),
		csdefine.ACTIVITY_GCZ_MATCH:( "GCZManager","onGCZNotifyJoinMemberMatchStart","onGCZNotifyJoinMemberMatchEnd" ),
		csdefine.ACTIVITY_GCZ_ENTER:( "GCZManager","onGCZNotifyEnter","onGCZNotifyEnterClose" ),
		csdefine.ACTIVITY_GCZ_START:( "GCZManager","onGCZStart","onGCZEnd" ),
		csdefine.ACTIVITY_BATTLE:("BattleActivityMgr", "onActiveStart", "onActiveEnd"),
}