// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleKitBagInterface.h"
#include "Entity/Alias.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "GameData/Item/ItemFactory.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/KitbagTypeEnum.h"
#include "Interface/BagInterface.h"
#include "GameData/Item/ItemUse.h"
#include "GameData/Item/EquipPart.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"
#include "Interface/StatusMessageInterface.h"
#include "CS3Base/UIManager.h"
#include "Manager/MessageManager.h"
#include "Interface/Role/RoleTalkInterface.h"
#include "KBEngine.h"
#include "CS3Base/CS3Entity.h"
#include "Manager/LocalDataSaveManager.h"
#include "GameData/MessageID.h"
#include "Manager/TutorialManager.h"
#include "Manager/SkillManager.h"
#include "GameData/ConstData.h"
#include "Manager/AudioManager.h"
#include "Manager/ParticleManager.h"


CONTROL_COMPILE_OPTIMIZE_START
	
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleKitBagInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(kitbagInit, &URoleKitBagInterface::kitbagInit, const FVariantArray& )
CS3_DECLARE_INTERFACE_REMOTE_METHOD(addItem, &URoleKitBagInterface::addItem, const FVariant&, const uint8& )
CS3_DECLARE_INTERFACE_REMOTE_METHOD(addStoreItem, &URoleKitBagInterface::addStoreItem, const FVariant& )
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_ShowItemListIcon, &URoleKitBagInterface::CLIENT_ShowItemListIcon, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updateTongStoreItem, &URoleKitBagInterface::updateTongStoreItem, const FVariant& )
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleKitBagInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleKitBagInterface::URoleKitBagInterface()
{
	bIsSort = false;
	initKitBag = false;
	storeCapacity = STORE_CAPACITY;
}

URoleKitBagInterface::~URoleKitBagInterface()
{
}

void URoleKitBagInterface::onLeaveWorld()
{
	FKB_ItemList.Empty();
	initKitBag = false;
	Supper::onLeaveWorld();
}

void URoleKitBagInterface::kitbagInit(const FVariantArray& itemList)
{
	for (auto it : itemList)
	{
		FITEM_FOR_CLIENT itemData(it);

		UItemBase* item = UItemFactory::GetItemByID(itemData.id);
		if (!IsValid(item))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::kitbagInit : item!"));
			return;
		}
		item->UID = itemData.uid;
		item->Amount = itemData.amount;
		item->BindType = itemData.bindType;
		item->ItemOrder = itemData.itemOrder;
		item->ItemEndTime = itemData.itemEndTime;
		item->InitDynamicDataForJson(itemData.dynamicData);
		
		FKB_ItemList.Add(item);

		if (IsValid(UUECS3GameInstance::Instance))
		{
			if (IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager))
				UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData->AddLocalItem(item);			// 添加本地存储

			if (IsValid(UUECS3GameInstance::Instance->SkillManager) && item->SkillID != 0)
			{
				UUECS3GameInstance::Instance->SkillManager->RefreshCDBySkillID(item->SkillID);
			}
		}

		UpdateGrid(item->UID, item->ItemOrder);
		UpdateQBItemAmount(item->ItemID);
	}
	initKitBag = true;
}

bool URoleKitBagInterface::isKBLocked(const FString& ItemUID)
{
	if (!ItemUID.IsEmpty())
	{
		UItemBase* item = FindItemByUID(ItemUID);
		if (IsValid(item))
		{
			if (item->IsWhite())
			{
				return false;
			}
		}
	}
	return kbLockStatus == (int32)KB_LOCK_STATUS::LOCK_KB_WITH_PW;
}

void URoleKitBagInterface::CLIENT_openInputKBPW_Implementation()
{

}

bool URoleKitBagInterface::IsSort()
{
	return bIsSort;
}

int32 URoleKitBagInterface::GetAmountByItemID(int32 ItemID, FIND_BINDTYPE_ENUM bindType)
{
	switch (bindType)
	{
	case FIND_BINDTYPE_ENUM::BIND:
		return GetAmountByItemList(GetItemsByBindType(ItemID, true));
	case FIND_BINDTYPE_ENUM::NONE_BIND:
		return GetAmountByItemList(GetItemsByBindType(ItemID, false));
	case FIND_BINDTYPE_ENUM::INGOREBIND:
		return GetAmountByItemList(GetItemsByBindType(ItemID, true)) + GetAmountByItemList(GetItemsByBindType(ItemID, false));
	default:
		return 0;
	}
}

int32 URoleKitBagInterface::GetAmountByKBType(EKITBAGTYPE bagType, int32 ItemID, FIND_BINDTYPE_ENUM bindType)
{
	switch (bindType)
	{
	case FIND_BINDTYPE_ENUM::BIND:
		return GetAmountByItemList(GetItemsByKBTypeAndID(bagType, ItemID, true));
	case FIND_BINDTYPE_ENUM::NONE_BIND:
		return GetAmountByItemList(GetItemsByKBTypeAndID(bagType, ItemID, false));
	case FIND_BINDTYPE_ENUM::INGOREBIND:
		return GetAmountByItemList(GetItemsByKBTypeAndID(bagType, ItemID, true)) + GetAmountByItemList(GetItemsByKBTypeAndID(bagType, ItemID, false));
	default:
		return 0;
	}
}

TArray<UItemBase*> URoleKitBagInterface::GetItemListByItemScript(const FString& ItemScript)
{
	TArray<UItemBase*> itemList;
	for (auto item : FKB_ItemList)
	{
		if (item->Script == ItemScript)
		{
			itemList.Add(item);
		}
	}
	return itemList;
}

bool URoleKitBagInterface::UseItem(const FString& UID)
{
	UItemBase* item = FindItemByUID(UID);
	if (item && item->IsCanUse())
	{
		UItemUse* useitem = Cast<UItemUse>(item);
		if (useitem)
		{
			AServerCharacter* player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
			int32 result = useitem->Use(player);
			if (result == UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG)
			{
				return true;
			}
			else
			{
				//根据result打印消息
				UGolbalBPFunctionLibrary::StatusMessage(result, TEXT(""));
				return false;
			}
		}
	}
	return false;
}


UItemBase* URoleKitBagInterface::FindItemByOrder(int32 order)
{
	TArray<UItemBase*> TempList;
	TempList.Append(FKB_ItemList);
	TempList.Append(StoreItemList);
	TempList.Append(TongStoreItemList);
	TempList.Append(ToolStoreItemList);
	TempList.Append(TripodStoreItemList);
	for (const auto item : TempList)
	{
		if (order == item->ItemOrder)
		{
			return item;
		}
	}
	
	return nullptr;
}

UItemBase* URoleKitBagInterface::FindItemByUID(const FString& uid)
{
	TArray<UItemBase*> TempList;
	TempList.Append(FKB_ItemList);
	TempList.Append(StoreItemList);
	TempList.Append(TongStoreItemList);
	TempList.Append(ToolStoreItemList);
	TempList.Append(TripodStoreItemList);
	for (const auto item : TempList)
	{
		if (uid == item->UID)
		{
			return item;
		}
	}
	
	return nullptr;
}

TArray<UItemBase*> URoleKitBagInterface::GetItemsByItemID(int32 itemid)
{
	TArray<UItemBase*> result;
	if (FKB_ItemList.Num() > 0)
	{
		for (auto item : FKB_ItemList)
		{
			if (item->ItemID == itemid)
			{
				result.Add(item);
			}
		}
	}
	return result;
}

bool URoleKitBagInterface::CheckIsOwnByItemID(int32 ItemID)
{
	if (FKB_ItemList.Num() > 0)
	{
		for (auto item : FKB_ItemList)
		{
			if (item->ItemID == ItemID)
			{
				return true;
			}
		}
	}
	return false;
}

TArray<UItemBase*> URoleKitBagInterface::GetItemsByBindType(int32 itemid, bool bIsBinded)
{
	TArray<UItemBase*> result;
	if (FKB_ItemList.Num() > 0)
	{
		for (auto item : FKB_ItemList)
		{
			if ((item->ItemID == itemid) && (item->IsBinded() == bIsBinded))
			{
				result.Add(item);
			}
		}
	}
	return result;
}

TArray<UItemBase*> URoleKitBagInterface::GetItemsByKBType(EKITBAGTYPE bagType)
{
	if (bagType == EKITBAGTYPE::STORE)
	{
		return StoreItemList;
	}
	else if (bagType == EKITBAGTYPE::TONG_STORE)
	{
		return TongStoreItemList;
	}
	else if (bagType == EKITBAGTYPE::BAG_TOOL)
	{
		return ToolStoreItemList;
	}
	else if (bagType == EKITBAGTYPE::BAG_TRIPOD)
	{
		return TripodStoreItemList;
	}
	TArray<UItemBase*> result;
	if (FKB_ItemList.Num() > 0)
	{
		for (auto item : FKB_ItemList)
		{
			if (UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(item->ItemOrder) == bagType)
			{
				result.Add(item);
			}
		}
	}
	return result;
}

TArray<UItemBase*> URoleKitBagInterface::GetItemsByKBTypeAndID(EKITBAGTYPE bagType, int32 itemid, bool bIsBinded)
{
	TArray<UItemBase*> result;
	if (bagType == EKITBAGTYPE::STORE)
	{
		for (auto item : StoreItemList)
		{
			if ((item->ItemID == itemid) && (item->IsBinded() == bIsBinded))
			{
				result.Add(item);
			}
		}
		return result;
	}
	else if (bagType == EKITBAGTYPE::TONG_STORE)
	{
		for (auto item : TongStoreItemList)
		{
			if ((item->ItemID == itemid) && (item->IsBinded() == bIsBinded))
			{
				result.Add(item);
			}
		}
		return result;
	}

	for (auto item : FKB_ItemList)
	{
		EKITBAGTYPE itembt = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(item->ItemOrder);
		if ((item->ItemID == itemid) && (item->IsBinded() == bIsBinded) && itembt == bagType)
		{
			result.Add(item);
		}
	}
	return result;
}

int32 URoleKitBagInterface::GetAbsOrderIdByItemID(int32 ItemID)
{
	TArray<UItemBase*> items = GetItemsByItemID(ItemID);
	if (items.Num() > 0)
	{
		return items[0]->ItemOrder;
	}
	return 0;
}

int32 URoleKitBagInterface::GetFreeRingOrder()
{
	//优先选择空的戒指格子，如果两个格子都有物品，默认选择左手的戒指格子
	if (!IsValid(FindItemByOrder((uint8)MODEL_PART_TYPE::MODEL_PART_RHAND_RING)))
	{
		return (uint8)MODEL_PART_TYPE::MODEL_PART_RHAND_RING;
	}
	else
	{
		return (uint8)MODEL_PART_TYPE::MODEL_PART_LHAND_RING;
	}
}

bool URoleKitBagInterface::IsGridLocked(int32 absorder)
{	
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::IsGridLocked : GetEntity()!"));
		return false;
	}
	EKITBAGTYPE kitbag = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(absorder);
	int32 start = 0;
	int32 end = 0;
	int32 unlockgridnum = 0;
	int32 capacity = 0;
	int32 queststart = 0;
	int32 crystalstart = 0;
	switch (kitbag)
	{
	case EKITBAGTYPE::EQUIP:
		break;
	case EKITBAGTYPE::COMMON:
		//背包起始位置
		start = COMMON_BAG_START;
		//默认开启的普通背包格子数
		capacity = COMMON_BAG_CAPACITY;
		// 解锁的格子数
		unlockgridnum = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("unLockGridNum"));
		break;
	case EKITBAGTYPE::QUEST:
		break;
	case EKITBAGTYPE::CRYSTAL:
		break;
	case EKITBAGTYPE::STORE:
		queststart = COMMON_BAG_START + COMMON_BAG_CAPACITY + COMMON_BAG_LOCK_CAPACITY;
		crystalstart = queststart + QUEST_BAG_CAPACITY;
		//仓库起始位置
		start = crystalstart + CRYSTAL_BAG_CAPACITY;
		//默认开启的仓库格子数
		capacity = STORE_CAPACITY;
		// 解锁的格子数
		unlockgridnum = unLockStoreGridNum;
		break;
	case EKITBAGTYPE::BAG_TOOL:
		start = BAG_WORK_SHOP_LOCKERS_START;
		capacity = STORE_LOCKERS_CAPACITY;
		unlockgridnum = unLockToolGridNum;
	case EKITBAGTYPE::BAG_TRIPOD:
		start = BAG_ALCHEMIST_LOCKERS_START;
		capacity = STORE_LOCKERS_CAPACITY;
		unlockgridnum = unLockTripodGridNum;
	default:
		break;
	}

	//已经开启的最后一个格子
	end = start + capacity + unlockgridnum - 1;
	if ((absorder >= start) && (absorder <= end))
	{
		return true;
	}
	return false;
}


int32 URoleKitBagInterface::CalcEachUnLockGridCost(int32 absorder)
{
	EKITBAGTYPE kbType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(absorder);
	int32 start = 0;
	switch (kbType)
	{
	case EKITBAGTYPE::EQUIP:
		break;
	case EKITBAGTYPE::COMMON:
		start = COMMON_BAG_START + commonCapacity;
		break;
	case EKITBAGTYPE::QUEST:
	case EKITBAGTYPE::CRYSTAL:
		break;
	case EKITBAGTYPE::STORE:
		start = COMMON_BAG_START + COMMON_BAG_CAPACITY + COMMON_BAG_LOCK_CAPACITY + QUEST_BAG_CAPACITY + CRYSTAL_BAG_CAPACITY + STORE_CAPACITY;
		break;
	default:
		break;
	}
	int32 lockIndex = absorder - start + 1;
	return lockIndex * (lockIndex + 1);
}

int32 URoleKitBagInterface::CalcSumUnLockGridCost(int32 absorder, int32& unlockNum)
{
	EKITBAGTYPE kbType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(absorder);
	int32 startindex = 0;
	switch (kbType)
	{
	case EKITBAGTYPE::EQUIP:
		return 0;
	case EKITBAGTYPE::COMMON:
		startindex = COMMON_BAG_START + commonCapacity + unLockGridNum;
		break;
	case EKITBAGTYPE::QUEST:
	case EKITBAGTYPE::CRYSTAL:
		return 0;
	case EKITBAGTYPE::STORE:
		startindex = COMMON_BAG_START + COMMON_BAG_CAPACITY + COMMON_BAG_LOCK_CAPACITY + QUEST_BAG_CAPACITY + CRYSTAL_BAG_CAPACITY + STORE_CAPACITY + unLockStoreGridNum;
		break;
	default:
		return 0;
	}
	int32 endindex = absorder;
	int32 sumcost = 0;
	unlockNum = endindex - startindex + 1;
	for (int32 i = startindex; i <= endindex; i++)
	{
		sumcost += CalcEachUnLockGridCost(i);
	}
	return sumcost;
}

void URoleKitBagInterface::OnPlayerLevelChange(const int32& level)
{
	TMap< MODEL_PART_TYPE, UEquip* > PartEquips;
	for (auto item : FKB_ItemList)
	{
		OnItemCanUseStateChange(item->UID);

		//以下为引导提示功能：把同位置可用装备战斗力最强的加入（提示）字典
		if(item->ItemOrder > COMMON_BAG_START && item->IsEquip() && item->IsCanUse())
		{			
			UEquip* equip = Cast<UEquip>(item);
			MODEL_PART_TYPE PartType = equip->GetModelPartType();
			if(PartEquips.Contains(PartType))
			{
				if (PartEquips[PartType]->CombatPower < equip->CombatPower) { PartEquips[PartType] = equip; }
			}
			else
			{
				PartEquips.Add(PartType, equip);
			}
		}
	}
	//按照字典力的装备显示提示
	for (TPair< MODEL_PART_TYPE, UEquip* >partEquip:PartEquips)
	{	UGolbalBPFunctionLibrary::TutorialManager()->OnAddItem(partEquip.Value->UID);	}
}

void URoleKitBagInterface::OnEquipHardinessPercentChanged_Implementation(float HardinessPercentconst, const FString& UId, int32 ItemOrder)
{
	OnItemCanUseStateChange(UId);
}

void URoleKitBagInterface::CLIENT_OnUnLockStoreGridNumChange_Implementation(const int32& unLockNum)
{
	unLockStoreGridNum = unLockNum;
}

void URoleKitBagInterface::CLIENT_OnStoreMoneyChange_Implementation(const FString& money)
{
	StoreMoney = FSTRING_TO_INT64(money);
}

void URoleKitBagInterface::addItem(const FVariant& FVariantItem, const uint8& reason )
{
	
	FITEM_FOR_CLIENT itemData(FVariantItem);

	UItemBase* item = UItemFactory::GetItemByID(itemData.id);
	if (!IsValid(item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::CLIENT_addItem_Implementation : item!"));
		return;
	}
	item->UID = itemData.uid;
	item->Amount = itemData.amount;
	item->BindType = itemData.bindType;
	item->ItemOrder = itemData.itemOrder;
	item->ItemEndTime = itemData.itemEndTime;
	item->InitDynamicDataForJson(itemData.dynamicData);
	FKB_ItemList.Add(item);

	OnAddItem(item, reason );
	if (item->SkillID != 0)
	{
		UUECS3GameInstance::Instance->SkillManager->RefreshCDBySkillID(item->SkillID);
	}
}



void URoleKitBagInterface::OnAddItem(UItemBase* ItemInst, const uint8& reason)
{
	if (UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(ItemInst->ItemOrder) == EKITBAGTYPE::COMMON)
	{
		if (IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData))
		{
			UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData->AddLocalItem(ItemInst);			// 添加本地存储
			if (reason == uint8( ADD_ITEM_REASON::ITEM_ADD_BY_SPLIT))
			{
				UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData->SaveNewTip(ItemInst->UID, false);//如果是分割添加的物品，不需要显示tip样式
			}
		}
	}
	
	
	UpdateGrid(ItemInst->UID, ItemInst->ItemOrder);
	UpdateQBItemAmount(ItemInst->ItemID);

	ShowAddItemAction(ItemInst, reason);
}

void URoleKitBagInterface::ShowAddItemAction(UItemBase* ItemInst, const uint8& reason)
{
	//触发获取物品指引提示
	UGolbalBPFunctionLibrary::TutorialManager()->OnAddItem(ItemInst->UID);

	//金色及以上品质，除GM命令、摆摊、礼包、拆分以外的来源都要显示入包表现
	if (ItemInst->Quality >= 3
		&& !(reason == uint8(ADD_ITEM_REASON::ITEM_ADD_BY_GM_COMMAND)
			|| reason == uint8(ADD_ITEM_REASON::ITEM_ADD_BY_STALLTRADE)
			|| reason == uint8(ADD_ITEM_REASON::ITEM_ADD_BY_USE_GIFT_ITEM)
			|| reason == uint8(ADD_ITEM_REASON::ITEM_ADD_BY_SPLIT)
			))
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UBaseWindow* EnterBagAnim = UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("EnterBagAnim"));
			if (EnterBagAnim && EnterBagAnim->IsVisible())
			{
				//如果当前正在播放入包表现，则直接舍弃
				return;
			}
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("EnterBagAnim"));
		}
	}
}

void URoleKitBagInterface::CLIENT_removeItem_Implementation(int32 itemorder)
{
	UItemBase* temp = FindItemByOrder(itemorder);
	if (temp)
	{
		if (FKB_ItemList.Contains(temp))
		{
			OnKitBagItemRemoved(temp->ItemID);
			FString uid = temp->UID;
			FKB_ItemList.Remove(temp);
			UpdateGrid(uid, itemorder);
			UpdateQBItemAmount(temp->ItemID);

			UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData->RemoveLocalItem(temp->UID);
			//移除背包物品时，检查有没有需要关闭的新手指引
			if (UGolbalBPFunctionLibrary::TutorialManager())
			{
				UGolbalBPFunctionLibrary::TutorialManager()->OnRemoveItem(uid);
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("try to remove item by order[%d]"), itemorder);
	}
}

void URoleKitBagInterface::CLIENT_swapItemAC_Implementation(int32 srcorder, int32 dstorder)
{
	UItemBase* srcitem = FindItemByOrder(srcorder);
	UItemBase* dstitem = FindItemByOrder(dstorder);
	if (IsValid(srcitem))
	{
		srcitem->ItemOrder = dstorder;
		//把源物品信息更新到dstorder位置上
		UpdateGrid(srcitem->UID, dstorder);
		UpdateQBItemAmount(srcitem->ItemID);
	}
	else
	{
		UpdateGrid(TEXT(""), dstorder);
	}
	
	if (IsValid(dstitem))
	{
		dstitem->ItemOrder = srcorder;
		//把目标物品的信息更新到srcorder位置上
		UpdateGrid(dstitem->UID, srcorder);
		UpdateQBItemAmount(dstitem->ItemID);
	}
	else
	{
		//去掉原来的物品
		UpdateGrid(TEXT(""), srcorder);
	}
	
}

void URoleKitBagInterface::CLIENT_requestSortKitBagCB_Implementation(int32 kbType, const TArray<int32>& oldorders, const TArray<int32>& neworders)
{
	TArray<UItemBase*> tempList;
	for (int i = 0; i < oldorders.Num(); i++)
	{
		int32 oldorder = oldorders[i];
		UItemBase* item = FindItemByOrder(oldorder);
		tempList.Add(item);
	}
	int i = 0;
	for (i = 0; i < oldorders.Num(); i++)
	{
		auto item = tempList[i];
		if (IsValid(item))
		{
			int32 neworder = neworders[i];
			FString uid = item->UID;
			item->ItemOrder = neworder;
			//去掉原来格子里的物品
			UpdateGrid(TEXT(""), oldorders[i]);
		}
		else
		{
			CS3_Warning(TEXT("can't find item by oldorder[%d]"), oldorders[i]);
		}
	}
	for (i = 0; i < neworders.Num(); i++)
	{
		auto item = tempList[i];
		if (IsValid(item))
		{
			//移动物品到新格子
			UpdateGrid(item->UID, neworders[i]);
		}
		else
		{
			CS3_Warning(TEXT("can't find item by neworder[%d]"), neworders[i]);
		}
	}
	CLIENT_endSort();
}

void URoleKitBagInterface::RequestRemoveItem(FString UID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RequestRemoveItem : GetEntity()!"));
		return;
	}
	UItemBase* ItemBase = FindItemByUID(UID);
	if (ItemBase)
	{
		if (ItemBase->IsCanDestory())
		{
			KBEngine::FVariantArray args;
			args.Add(UID);
			GetEntity()->CellCall(TEXT("CELL_requestRemoveItemByUID"), args);
		}
		else
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(606, TEXT(""));
		}
	}
}

void URoleKitBagInterface::RequestRemoveStoreItem(FString UID, int32 AbsOrder)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RequestRemoveStoreItem : GetEntity()!"));
		return;
	}
	UItemBase* ItemBase = FindItemByUID(UID);
	if (ItemBase && ItemBase->IsCanDestory())
	{
		KBEngine::FVariantArray args;
		args.Add(UID);
		EKITBAGTYPE TempBagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(AbsOrder);
		if (TempBagType == EKITBAGTYPE::STORE)
		{
			GetEntity()->BaseCall(TEXT("requestRemoveStoreItem"), args);
		}
		else if (TempBagType == EKITBAGTYPE::TONG_STORE)
		{
			GetEntity()->CellCall(TEXT("CELL_requestRemoveTongStoreItem"), args);
		}
		else
		{
			CS3_Warning(TEXT("--URoleKitBagInterface::RequestRemoveStoreItem is not store type or tong store type"));
		}
	}
}

void URoleKitBagInterface::CLIENT_OnSetGridEnabledByOrderID_Implementation(const int32& itemOrder, const int32& isEnable)
{

}

void URoleKitBagInterface::RequestSwapItem(int32 FromAbsOrder, int32 ToAbsOrder)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RequestSwapItem : GetEntity()!"));
		return;
	}
	if (FromAbsOrder == ToAbsOrder)return;
	//绑定类型不一样则变为绑定
	bool IsChangeBindType = false;
	UItemBase* ToItemBase = FindItemByOrder(ToAbsOrder);
	UItemBase* FromItemBase = FindItemByOrder(FromAbsOrder);
	if (ToItemBase && FromItemBase)
	{
		
		if (  ToItemBase->ItemID == FromItemBase->ItemID 
			&& ToItemBase->BindType != FromItemBase->BindType 
			&& ToItemBase->IsCanStack(1)&& FromItemBase->IsCanStack(1))
		{
			IsChangeBindType = true;
		}
	}
	if (!_CheckSwapOrder(FromAbsOrder, ToAbsOrder, FromItemBase, ToItemBase))return;

	if (IsChangeBindType)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(609, "", FBtnClick::CreateLambda([this, FromAbsOrder, ToAbsOrder](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				_RequestSwapItem(FromAbsOrder, ToAbsOrder);
			}
		}));
	}
	else
	{
		_RequestSwapItem(FromAbsOrder, ToAbsOrder);
		
	}
}

void URoleKitBagInterface::splitItem(const FString& UID, const int32& Amount)
{
	for (const auto item : FKB_ItemList)
	{
		if (UID.Equals(item->UID))
		{
			if (item->Amount <= Amount)
			{
				CS3_Warning(TEXT("Split Item Err! amount is not emough(has amount:%d,split amount:%d)"), item->Amount, Amount);
				return;
			}
			EKITBAGTYPE bagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(item->ItemOrder);
			if (bagType == EKITBAGTYPE::QUEST || bagType == EKITBAGTYPE::CRYSTAL)
			{
				UGolbalBPFunctionLibrary::StatusMessage(1521, TEXT(""));
				return;
			}
			else
			{
				KBEngine::FVariantArray args;
				args.Add(UID);
				args.Add(INT_TO_FSTRING(Amount));
				if (nullptr != GetEntity())
				{
					GetEntity()->CellCall(TEXT("CELL_splitItem"), args);
				}
				return;
			}
			
		}
	}
	for (auto Item : StoreItemList)
	{
		if (Item->UID.Equals(UID))
		{
			KBEngine::FVariantArray args;
			args.Add(Item->ItemOrder);
			args.Add(Amount);
			if (nullptr != GetEntity())
			{
				GetEntity()->BaseCall(TEXT("splitStoreItem"), args);
			}
			return;
		}
	}
}

void URoleKitBagInterface::GetItemInfoByString(const FString& jsonstr, int32& itemid, int32& itemorder, int32& amount, int32& bindtype, FString& uid, FString& itemEndTime)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("jsonstr = %s"), *jsonstr);
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(jsonstr);
	auto temparray = returnvalue->GetObjectArray(this, TEXT("ROOT"));
	//列表只有一个元素
	for (auto item : temparray)
	{
		itemid = FSTRING_TO_INT(item->GetString(TEXT("id")));
		itemorder = FSTRING_TO_INT(item->GetString(TEXT("itemOrder")));
		amount = FSTRING_TO_INT(item->GetString(TEXT("amount")));
		bindtype = FSTRING_TO_INT(item->GetString(TEXT("bindType")));
		uid = item->GetString(TEXT("uid"));
		itemEndTime = item->GetString(TEXT("itemEndTime"));
	}
}

void URoleKitBagInterface::UpdateGrid(const FString& uid, const int32& absorder)
{
	EKITBAGTYPE bagtype = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(absorder);
	UBaseWindow* rolepropertywindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("RoleProperty"));
	UBaseWindow* kitbagwindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("KitBag"));
	UBaseWindow* storewindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("Store"));
	UBaseWindow* tongStorageWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("TongStorage"));
	UBaseWindow* spaceCopyBagWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SpaceCopyBag"));
	UBaseWindow* spaceCopyYXLMBagWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("YXLMExtraBar"));
	UBaseWindow* planeJSZZActivityWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("GoldTreeSeedActivityMain"));
	UBaseWindow* spaceNewJSZZWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("GoldTreeSeed"));
	UBaseWindow* toolStoreWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("WorkShopStorage"));
	UBaseWindow* tripodStoreWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("TripodStorage"));
	UBaseWindow* aimWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("Aim"));
	bool bIsImplemted = false;
	switch (bagtype)
	{
	case EKITBAGTYPE::EQUIP:
	case EKITBAGTYPE::BAG_TEMP_EQUIP:
		if (!IsValid(rolepropertywindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : rolepropertywindow!"));
			return;
		}
		bIsImplemted = rolepropertywindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(rolepropertywindow, uid, absorder);
		}
		else
		{
			CS3_Warning(TEXT("RolePropertyWindow not implement BagInterface"));
		}
		break;
	case EKITBAGTYPE::COMMON:
	case EKITBAGTYPE::QUEST:
	case EKITBAGTYPE::CRYSTAL:
		if (!IsValid(kitbagwindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : kitbagwindow!"));
			return;
		}
		bIsImplemted = kitbagwindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(kitbagwindow, uid, absorder);

		}
		else
		{
			CS3_Warning(TEXT("KitBagWindow not implement BagInterface"));
		}
		if (IsValid(planeJSZZActivityWindow))
		{
			bool bIsJSZZWndImplemted = planeJSZZActivityWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
			if (bIsJSZZWndImplemted)
			{
				IBagInterface::Execute_UpdateGrid(planeJSZZActivityWindow, uid, absorder);
			}
			else
			{
				CS3_Warning(TEXT("PlaneJSZZActivityWindow not implement BagInterface"));
			}
		}
		break;
	case EKITBAGTYPE::STORE:
		if (!IsValid(storewindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : storewindow !"));
			return;
		}
		bIsImplemted = storewindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(storewindow, uid, absorder);
		}
		else
		{
			CS3_Warning(TEXT("StoreWindow not implement BagInterface"));
		}
		break;
	case EKITBAGTYPE::TONG_STORE:
		if (!IsValid(tongStorageWindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : tongStorageWindow!"));
			return;
		}
		bIsImplemted = tongStorageWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(tongStorageWindow, uid, absorder);
		}
		else
		{
			CS3_Warning(TEXT("TongStorageWindow not implement BagInterface"));
		}
		break;
	case EKITBAGTYPE::SPACE_COPY_BAG:
		if (!IsValid(spaceCopyBagWindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : spaceCopyBagWindow!"));
			return;
		}
		bIsImplemted = spaceCopyBagWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(spaceCopyBagWindow, uid, absorder);
		}
		else
		{
			CS3_Warning(TEXT("spaceCopyBagWindow not implement BagInterface"));
		}
		if (IsValid(spaceNewJSZZWindow))
		{
			bool bIsJSZZWndImplemted = spaceNewJSZZWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
			if (bIsJSZZWndImplemted)
			{
				IBagInterface::Execute_UpdateGrid(spaceNewJSZZWindow, uid, absorder);
			}
			else
			{
				CS3_Warning(TEXT("spaceNewJSZZWindow not implement BagInterface"));
			}
		}
		if (IsValid(aimWidget))
		{
			bool bIsAimWidgetImplemted = aimWidget->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
			if (bIsAimWidgetImplemted)
			{
				IBagInterface::Execute_UpdateGrid(aimWidget, uid, absorder);
			}
			else
			{
				CS3_Warning(TEXT("aimWidget not implement BagInterface"));
			}
		}
		break;
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM1:
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM2:
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM3:
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM4:
		if (!IsValid(spaceCopyYXLMBagWindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : spaceCopyYXLMBagWindow!"));
			return;
		}
		bIsImplemted = spaceCopyYXLMBagWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(spaceCopyYXLMBagWindow, uid, absorder);
		}
		else
		{
			CS3_Warning(TEXT("spaceCopyYXLMBagWindow not implement BagInterface"));
		}
		break;
	case EKITBAGTYPE::BAG_TOOL:
		if (!IsValid(toolStoreWindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : toolStoreWindow!"));
			return;
		}
		bIsImplemted = toolStoreWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(toolStoreWindow, uid, absorder);
		}
		else
		{
			CS3_Warning(TEXT("toolStoreWindow not implement BagInterface"));
		}
		break;
	case EKITBAGTYPE::BAG_TRIPOD:
		if (!IsValid(tripodStoreWindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGrid : tripodStoreWindow!"));
			return;
		}
		bIsImplemted = tripodStoreWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGrid(tripodStoreWindow, uid, absorder);
		}
		else
		{
			CS3_Warning(TEXT("tripodStoreWindow not implement BagInterface"));
		}
		break;
	default:
		break;
	}
}

UItemBase* URoleKitBagInterface::GetItemByDynamicProperty(FString& type, FString& propertyname, FString& propertyvalue)
{
	TArray<FString> out;
	DynamicProperty.ParseIntoArray(out, TEXT("|#|"), true);
	if (out.Num() == 4)
	{
		type = out[0];
		FString uid = out[1];
		propertyname = out[2];
		propertyvalue = out[3];
		return FindItemByUID(uid);
	}
	else if (out.Num() == 3)
	{
		type = out[0];
		FString uid = out[1];
		propertyname = out[2];
		propertyvalue = TEXT("");				// 有可能是空的
		return FindItemByUID(uid);
	}
	return nullptr;
}

void URoleKitBagInterface::OnRep_DynamicProperty()
{
	UItemBase* item;
	FString type;
	int32 typeint;
	FString propertyname;
	FString propertyvalue;
	item = GetItemByDynamicProperty(type, propertyname, propertyvalue);
	if (!IsValid(item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::OnRep_DynamicProperty : item!"));
		return;
	}
	if (type == TEXT("INT"))
	{
		typeint = 0;
	}
	else if (type == TEXT("FLOAT"))
	{
		typeint = 1;
	}
	else if (type == TEXT("STRING"))
	{
		typeint = 2;
	}
	else if (type == TEXT("BOOL"))
	{
		typeint = 3;
	}
	else
	{
		typeint = 4;
	}
	switch (typeint)
	{
	case 0:
		item->SetIntPropertyByKey(propertyname, FSTRING_TO_INT(propertyvalue));
		break;
	case 1:
		item->SetFloatPropertyByKey(propertyname, FSTRING_TO_FLOAT(propertyvalue));
		break;
	case 2:
		item->SetFStringPropertyByKey(propertyname, propertyvalue);
		break;
	case 3:
	{
		bool value = propertyvalue == "True" ? true : false;
		item->SetBoolPropertyByKey(propertyname, value);
		break;
	}
	default:
		item->SetFStringPropertyByKey(propertyname, propertyvalue);
		break;
	}
}

void URoleKitBagInterface::OnSetCooldown(int32 SkillID, float RemainningTime, float PersistTime)
{
	TArray<UItemBase*> result;
	result = GetItemListBySkillID(SkillID);
	if (result.Num() <= 0)
	{
		return;
	}
	for (auto item : result)
	{
		//设置物品CD总持续时间
		item->SetCDPersistTime(PersistTime);
		//物品CD
		OnUpdateItemUsingCD(item->ItemID, RemainningTime, PersistTime);
		//背包物品CD
		if (item->ItemOrder >= COMMON_BAG_START)
		{
			UpdateGridUsingCD(item->UID, item->ItemOrder, RemainningTime, PersistTime);
			UItemUse* ItemUse = Cast<UItemUse>(item);
			if (IsValid(ItemUse) && RemainningTime > 0.0f)
			{
				ItemUse->StartCdTime(RemainningTime);
			}
		}
	}
}

TArray<UItemBase*> URoleKitBagInterface::GetItemListBySkillID(int32 SkillID)
{
	TArray<UItemBase*> result;
	for (auto item : FKB_ItemList)
	{
		if (SkillID == item->SkillID)
		{
			result.Add(item);
		}
	}
	return result;
}

void URoleKitBagInterface::UpdateGridUsingCD(const FString& uid, const int32& absorder, const float& RemainningTime, const float& PersistTime)
{
	EKITBAGTYPE bagtype = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(absorder);
	UBaseWindow* kitbagwindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("KitBag"));
	UBaseWindow* spaceCopyBagWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SpaceCopyBag"));
	UBaseWindow* spaceCopyYXLMBagWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("YXLMExtraBar"));
	UBaseWindow* spaceNewJSZZWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("GoldTreeSeed"));
	bool bIsImplemted = false;
	switch (bagtype)
	{
	case EKITBAGTYPE::EQUIP:
		break;
	case EKITBAGTYPE::BAG_TEMP_EQUIP:
		break;
	case EKITBAGTYPE::COMMON:
	case EKITBAGTYPE::QUEST:
	case EKITBAGTYPE::CRYSTAL:
		if (!IsValid(kitbagwindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGridUsingCD : kitbagwindow!"));
			return;
		}
		bIsImplemted = kitbagwindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGridUsingCD(kitbagwindow, uid, absorder, RemainningTime, PersistTime);
		}
		else
		{
			CS3_Warning(TEXT("KitBagWindow not implement BagInterface"));
		}
		break;
	case EKITBAGTYPE::SPACE_COPY_BAG:
		if (!IsValid(spaceCopyBagWindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGridUsingCD : spaceCopyBagWindow!"));
			return;
		}
		bIsImplemted = spaceCopyBagWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGridUsingCD(spaceCopyBagWindow, uid, absorder, RemainningTime, PersistTime);
		}
		else
		{
			CS3_Warning(TEXT("spaceCopyBagWindow not implement BagInterface"));
		}
		if (IsValid(spaceNewJSZZWindow))

		{
			bool bIsJSZZWndImplemted = spaceNewJSZZWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
			if (bIsJSZZWndImplemted)
			{
				IBagInterface::Execute_UpdateGridUsingCD(spaceNewJSZZWindow, uid, absorder, RemainningTime, PersistTime);
			}
			else
			{
				CS3_Warning(TEXT("SpaceNewJSZZWindow not implement BagInterface"));
			}
		}
		break;
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM1:
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM2:
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM3:
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM4:
		if (!IsValid(spaceCopyYXLMBagWindow))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UpdateGridUsingCD : spaceCopyYXLMBagWindow!"));
			return;
		}
		bIsImplemted = spaceCopyYXLMBagWindow->GetClass()->ImplementsInterface(UBagInterface::StaticClass());
		if (bIsImplemted)
		{
			IBagInterface::Execute_UpdateGridUsingCD(spaceCopyYXLMBagWindow, uid, absorder, RemainningTime, PersistTime);
		}
		else
		{
			CS3_Warning(TEXT("spaceCopyYXLMBagWindow not implement BagInterface"));
		}
		break;

	default:
		break;
	}
}

void URoleKitBagInterface::CLIENT_requestOpenStoreWindow_Implementation(const int32& npcID, const int32& unlockNum, const FString& money)
{
	canUnLockStoreCapacity = STORE_LOCK_CAPACITY;
	unLockStoreGridNum = unlockNum;
	StoreMoney = FSTRING_TO_INT64(money);
	StoreItemList.Empty();
	UCS3EntityInterface* BaseInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTalkInterface"), EntityID);
	if (IsValid(BaseInterface))
	{
		URoleTalkInterface * talkInt = Cast<URoleTalkInterface>(BaseInterface);
		if (IsValid(talkInt))
		{
			talkInt->openStoreWindown(npcID);
		}
	}
	
}

bool URoleKitBagInterface::IsSameScriptType(const int32& srcItemID, const int32& dstItemID)
{
	if (srcItemID == dstItemID)
	{
		return true;
	}
	FCS3ItemData srcData = UItemFactory::GetStaticDataByItemID(srcItemID);
	FCS3ItemData dstData = UItemFactory::GetStaticDataByItemID(dstItemID);
	return srcData.Script.Equals(dstData.Script) && srcData.Param1.Equals(dstData.Param1);
}

bool URoleKitBagInterface::IsStoreMoneyEnough(int64 money)
{
	if (StoreMoney >= money)
	{
		return true;
	}
	return false;
}

int32 URoleKitBagInterface::GetAmountByItemList(TArray<UItemBase*> itemList)
{
	if (itemList.Num() == 0)
	{
		return 0;
	}
	int32 sum = 0;
	for (auto item : itemList)
	{
		sum += item->Amount;
	}
	return sum;
}


TArray<USkillData*> URoleKitBagInterface::GetItemSkillDataList()
{
	TArray<USkillData*> skillList;
	TArray<int32> skillIDList;
	for (auto item : FKB_ItemList)
	{
		if (item->SkillID != 0)
		{
			if (skillIDList.Contains(item->SkillID)) continue;
			USkillData* skilldata = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(item->SkillID);
			if (IsValid(skilldata))
			{
				skillList.Add(skilldata);
				skillIDList.Add(item->SkillID);
			}
		}
	}
	return skillList;
}

TArray<FString> URoleKitBagInterface::GetSamePartEquipUIds(const FString& EquipUId)
{
	TArray<FString> EquipUIds;
	UItemBase* ItemBase = FindItemByUID(EquipUId);
	if (!IsValid(ItemBase))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::GetSamePartEquipUIds : ItemBase!"));
		return EquipUIds;
	}
	UEquip* equip_ = Cast<UEquip>(ItemBase);
	if (IsValid(equip_))
	{
		GetSamePartEquipByItem(EquipUIds, equip_);
	}
	return EquipUIds;
}

void URoleKitBagInterface::GetSamePartEquipByItem(TArray<FString>& UIDArr, UEquip* Equip_)
{
	if (Equip_)
	{
		MODEL_PART_TYPE PartType = Equip_->GetModelPartType();
		FString EquipUId = Equip_->UID;
		if (PartType == MODEL_PART_TYPE::MODEL_PART_LHAND_RING || PartType == MODEL_PART_TYPE::MODEL_PART_RHAND_RING)
		{
			bool IsOwnerEquip = false;
			UItemBase* LHandRing = FindItemByOrder(int32(MODEL_PART_TYPE::MODEL_PART_LHAND_RING));
			UItemBase* RHandRing = FindItemByOrder(int32(MODEL_PART_TYPE::MODEL_PART_RHAND_RING));
			IsOwnerEquip = (IsValid(LHandRing) && LHandRing->UID == EquipUId) || (IsValid(RHandRing) && RHandRing->UID == EquipUId);
			if (!IsOwnerEquip)
			{
				if (IsValid(LHandRing)) UIDArr.Add(LHandRing->UID);
				if (IsValid(RHandRing)) UIDArr.Add(RHandRing->UID);
			}
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_BWEAPON || PartType == MODEL_PART_TYPE::MODEL_PART_LWEAPON || PartType == MODEL_PART_TYPE::MODEL_PART_RWEAPON)
		{
			bool IsOwnerEquip = false;
			UItemBase* BWeapon = FindItemByOrder(int32(MODEL_PART_TYPE::MODEL_PART_BWEAPON));
			UItemBase* LWeapon = FindItemByOrder(int32(MODEL_PART_TYPE::MODEL_PART_LWEAPON));
			UItemBase* RWeapon = FindItemByOrder(int32(MODEL_PART_TYPE::MODEL_PART_RWEAPON));
			IsOwnerEquip = (IsValid(BWeapon) && BWeapon->UID == EquipUId) || (IsValid(LWeapon) && LWeapon->UID == EquipUId) || (IsValid(RWeapon) && RWeapon->UID == EquipUId);
			if (!IsOwnerEquip)
			{
				if (IsValid(BWeapon)) UIDArr.Add(BWeapon->UID);
				if (IsValid(LWeapon)) UIDArr.Add(LWeapon->UID);
				if (IsValid(RWeapon)) UIDArr.Add(RWeapon->UID);
			}
		}
		else
		{
			UItemBase* PartEquip = FindItemByOrder(int32(PartType));
			if (IsValid(PartEquip))
			{
				if (PartEquip->UID != EquipUId) UIDArr.Add(PartEquip->UID);
			}
		}
	}
	
}

bool URoleKitBagInterface::IsSamePartType(MODEL_PART_TYPE SrcPartType, MODEL_PART_TYPE DstPartType)
{
	if (SrcPartType == DstPartType)
	{
		return true;
	}
	else if ((SrcPartType == MODEL_PART_TYPE::MODEL_PART_LHAND_RING || SrcPartType == MODEL_PART_TYPE::MODEL_PART_RHAND_RING) && (DstPartType == MODEL_PART_TYPE::MODEL_PART_LHAND_RING || DstPartType == MODEL_PART_TYPE::MODEL_PART_RHAND_RING))
	{
		return true;
	}
	else if ((SrcPartType == MODEL_PART_TYPE::MODEL_PART_LWEAPON || SrcPartType == MODEL_PART_TYPE::MODEL_PART_RWEAPON || SrcPartType == MODEL_PART_TYPE::MODEL_PART_BWEAPON) && (DstPartType == MODEL_PART_TYPE::MODEL_PART_LWEAPON || DstPartType == MODEL_PART_TYPE::MODEL_PART_RWEAPON || DstPartType == MODEL_PART_TYPE::MODEL_PART_BWEAPON))
	{
		return true;
	}
	else
	{
		return false;
	}
}

void URoleKitBagInterface::CLIENT_ShowNextLevelGift_Implementation(const int32& ReqLevel, const TArray<int32>& GiftItemIDs, const TArray<int32>& GiftItemAmounts)
{

}

void URoleKitBagInterface::CLIENT_ShowLevelGift_Implementation(const FString& ItemUID, const TArray<int32>& GiftItemIDs, const TArray<int32>& GiftItemAmounts)
{

}

void URoleKitBagInterface::UseLevelGiftItem(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::UseLevelGiftItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UID);

	entity->CellCall(TEXT("CELL_useLevelGiftItem"), args);
}

void URoleKitBagInterface::SortLevelGiftItem(TArray<int32> GiftItemIDs, TArray<int32> GiftItemAmounts, TArray<int32>& NewGiftItemIDs, TArray<int32>& NewGiftItemAmounts)
{
	TArray<UItemBase*> ItemBaseList;
	for (int32 i = 0; i < GiftItemIDs.Num(); i++)
	{
		UItemBase* ItemBase = UItemFactory::GetItemByID(GiftItemIDs[i]);
		if (!IsValid(ItemBase)) continue;
		ItemBase->Amount = GiftItemAmounts[i];
		ItemBaseList.Add(ItemBase);
	}
	
	ItemBaseList.Sort([](const UItemBase& ItemBaseA, const UItemBase& ItemBaseB)
	{
		UItemBase& A = const_cast<UItemBase&>(ItemBaseA);
		UItemBase& B = const_cast<UItemBase&>(ItemBaseB);
		//品质
		if (ItemBaseB.Quality > ItemBaseA.Quality)
		{
			return false;
		}
		else if (ItemBaseB.Quality == ItemBaseA.Quality)
		{
			//装备
			if (B.IsEquip() && !A.IsEquip())
			{
				return false;
			}
			if (B.IsEquip() && A.IsEquip())
			{
				//ItemID
				if (ItemBaseA.ItemID > ItemBaseB.ItemID)
				{
					return false;
				}
			}
			else if (!B.IsEquip() && !A.IsEquip())
			{
				//药品（气血药）
				if (B.CheckItemType(20002) && !A.CheckItemType(20002))
				{
					return false;
				}
				else if (B.CheckItemType(20002) && A.CheckItemType(20002))
				{
					//ItemID
					if (ItemBaseA.ItemID > ItemBaseB.ItemID)
					{
						return false;
					}
				}
				else if (!B.CheckItemType(20002) && !A.CheckItemType(20002))
				{
					//药品（内息药）
					if (B.CheckItemType(20003) && !A.CheckItemType(20003))
					{
						return false;
					}
					else if (B.CheckItemType(20003) && A.CheckItemType(20003))
					{
						//ItemID
						if (ItemBaseA.ItemID > ItemBaseB.ItemID)
						{
							return false;
						}
					}
					else if (!B.CheckItemType(20003) && !A.CheckItemType(20003))
					{
						//礼包
						if (A.CheckItemType(20012) && !B.CheckItemType(20012))
						{
							return false;
						}
						else if (A.CheckItemType(20012) && B.CheckItemType(20012))
						{
							//ItemID
							if (ItemBaseA.ItemID > ItemBaseB.ItemID)
							{
								return false;
							}
						}
					}
				}
			}
			//ItemID
			if (ItemBaseA.ItemID > ItemBaseB.ItemID)
			{
				return false;
			}
		}
		return true;
	});

	for (UItemBase* Item : ItemBaseList)
	{
		NewGiftItemIDs.Add(Item->ItemID);
		NewGiftItemAmounts.Add(Item->Amount);
	}
}

void URoleKitBagInterface::addStoreItem( const FVariant& FVariantItem )
{
	FITEM_FOR_CLIENT itemData(FVariantItem);
	if (itemData.id == 0)
	{
		CS3_Warning(TEXT("add item by itemid[%d] failed!"), itemData.id);
		return;
	}
	UItemBase* item = UItemFactory::GetItemByID(itemData.id);
	if (!IsValid(item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::addStoreItem : item!"));
		return;
	}
	item->UID = itemData.uid;
	item->Amount = itemData.amount;
	item->BindType = itemData.bindType;
	item->ItemOrder = itemData.itemOrder;
	item->ItemEndTime = itemData.itemEndTime;
	item->InitDynamicDataForJson(itemData.dynamicData);
	EKITBAGTYPE bagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(itemData.itemOrder);
	if (bagType == EKITBAGTYPE::STORE)
	{
		StoreItemList.Add(item);
	}
	else if (bagType == EKITBAGTYPE::BAG_TOOL)
	{
		ToolStoreItemList.Add(item);
	}
	else if (bagType == EKITBAGTYPE::BAG_TRIPOD)
	{
		TripodStoreItemList.Add(item);
	}

	UpdateGrid(itemData.uid, itemData.itemOrder);
}

void URoleKitBagInterface::CLIENT_removeStoreItem_Implementation(const int32& itemorder)
{
	EKITBAGTYPE bagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(itemorder);
	if (bagType == EKITBAGTYPE::STORE)
	{
		for (auto item : StoreItemList)
		{
			if (item->ItemOrder == itemorder)
			{
				StoreItemList.Remove(item);
				break;
			}
		}
	}
	else if (bagType == EKITBAGTYPE::BAG_TOOL)
	{
		for (auto item : ToolStoreItemList)
		{
			if (item->ItemOrder == itemorder)
			{
				ToolStoreItemList.Remove(item);
				break;
			}
		}
	}
	else if (bagType == EKITBAGTYPE::BAG_TRIPOD)
	{
		for (auto item : TripodStoreItemList)
		{
			if (item->ItemOrder == itemorder)
			{
				TripodStoreItemList.Remove(item);
				break;
			}
		}
	}

	UpdateGrid(TEXT(""), itemorder);
}

void URoleKitBagInterface::CLIENT_swapStoreItemAC_Implementation(const int32& srcorder, const int32& dstorder)
{
	bool bNullSrcItem(true);
	bool bNullDstItem(true);

	for (auto item : StoreItemList)
	{
		if (item->ItemOrder == srcorder)
		{
			item->ItemOrder = dstorder;
			bNullSrcItem = false;
			UpdateGrid(item->UID, dstorder);
			continue;
		}
		if (item->ItemOrder == dstorder)
		{
			item->ItemOrder = srcorder;
			bNullDstItem = false;
			UpdateGrid(item->UID, srcorder);
			continue;
		}
	}
	if (bNullSrcItem)
	{
		UpdateGrid(TEXT(""), dstorder);
	}
	if (bNullDstItem)
	{
		UpdateGrid(TEXT(""), srcorder);
	}

}

void URoleKitBagInterface::CLIENT_swapItemFromBagToStore_Implementation(const int32& srcorder, const int32& dstorder)
{
	UItemBase* bagItem = FindItemByOrder(srcorder);
	UItemBase* storeItem(nullptr);
	for (auto item : StoreItemList)
	{
		if (item->ItemOrder == dstorder)
		{
			storeItem = item;
			break;
		}
	}
	if (storeItem)
	{
		storeItem->ItemOrder = srcorder;
		FKB_ItemList.Add(storeItem);
		StoreItemList.Remove(storeItem);
		UpdateGrid(storeItem->UID, srcorder);
		UpdateQBItemAmount(storeItem->ItemID);
	}
	else
	{
		UpdateGrid(TEXT(""), srcorder);
	}
	if (bagItem)
	{
		bagItem->ItemOrder = dstorder;
		FString uid = bagItem->UID;
		FKB_ItemList.Remove(bagItem);
		StoreItemList.Add(bagItem);
		UpdateGrid(bagItem->UID, dstorder);
		UpdateQBItemAmount(bagItem->ItemID);
		//移除背包物品时，检查有没有需要关闭的新手指引
		if (UGolbalBPFunctionLibrary::TutorialManager())
		{
			UGolbalBPFunctionLibrary::TutorialManager()->OnRemoveItem(uid);
		}
	}
	else
	{
		UpdateGrid(TEXT(""), dstorder);
	}

}


UItemBase* URoleKitBagInterface::FindStoreItemByUID(const FString& uid)
{
	for (auto item : StoreItemList)
	{
		if (item->UID == uid)
		{
			return item;
		}
	}
	return nullptr;
}

void URoleKitBagInterface::updateTongStoreItem(const FVariant& FVariantItem)
{
	FITEM_FOR_CLIENT itemData(FVariantItem);
	if (itemData.id == 0)
	{
		CS3_Warning(TEXT("add item by itemid[%d] failed!"), itemData.id);
		return;
	}
	UItemBase* item = UItemFactory::GetItemByID(itemData.id);
	if (!IsValid(item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::updateTongStoreItem : item!"));
		return;
	}
	item->UID = itemData.uid;
	item->Amount = itemData.amount;
	item->BindType = itemData.bindType;
	item->ItemOrder = itemData.itemOrder;
	item->ItemEndTime = itemData.itemEndTime;
	item->InitDynamicDataForJson(itemData.dynamicData);
	TongStoreItemList.Add(item);

	UpdateGrid(itemData.uid, itemData.itemOrder);
}

void URoleKitBagInterface::CLIENT_removeTongStoreItem_Implementation(const int32& itemorder)
{
	for (auto item : TongStoreItemList)
	{
		if (item->ItemOrder == itemorder)
		{
			TongStoreItemList.Remove(item);
			break;
		}
	}

	UpdateGrid(TEXT(""), itemorder);
}

void URoleKitBagInterface::CLIENT_swapTongStoreItemAC_Implementation(const int32& srcorder, const int32& dstorder)
{
	bool bNullSrcItem(true);
	bool bNullDstItem(true);

	for (auto item : TongStoreItemList)
	{
		if (item->ItemOrder == srcorder)
		{
			item->ItemOrder = dstorder;
			bNullSrcItem = false;
			UpdateGrid(item->UID, dstorder);
			continue;
		}
		if (item->ItemOrder == dstorder)
		{
			item->ItemOrder = srcorder;
			bNullDstItem = false;
			UpdateGrid(item->UID, srcorder);
			continue;
		}
	}
	if (bNullSrcItem)
	{
		UpdateGrid(TEXT(""), dstorder);
	}
	if (bNullDstItem)
	{
		UpdateGrid(TEXT(""), srcorder);
	}
}

void URoleKitBagInterface::CLIENT_swapItemFromBagToTongStore_Implementation(const int32& srcorder, const int32& dstorder)
{
	UItemBase* bagItem = FindItemByOrder(srcorder);
	UItemBase* storeItem(nullptr);
	for (auto item : TongStoreItemList)
	{
		if (item->ItemOrder == dstorder)
		{
			storeItem = item;
			break;
		}
	}
	if (storeItem)
	{
		storeItem->ItemOrder = srcorder;
		FKB_ItemList.Add(storeItem);
		TongStoreItemList.Remove(storeItem);
		UpdateGrid(storeItem->UID, srcorder);
	}
	else
	{
		UpdateGrid(TEXT(""), srcorder);
	}
	if (bagItem)
	{
		bagItem->ItemOrder = dstorder;
		FString uid = bagItem->UID;
		FKB_ItemList.Remove(bagItem);
		TongStoreItemList.Add(bagItem);
		UpdateGrid(bagItem->UID, dstorder);
		//移除背包物品时，检查有没有需要关闭的新手指引
		if (UGolbalBPFunctionLibrary::TutorialManager())
		{
			UGolbalBPFunctionLibrary::TutorialManager()->OnRemoveItem(uid);
		}
	}
	else
	{
		UpdateGrid(TEXT(""), dstorder);
	}
}

UItemBase* URoleKitBagInterface::FindTongStoreItemByUID(const FString& uid)
{
	for (auto item : TongStoreItemList)
	{
		if (item->UID == uid)
		{
			return item;
		}
	}
	return nullptr;
}
void URoleKitBagInterface::UseSpaceCopyItemByQuickKey(const int32 & index)
{
	int32 order = UGolbalBPFunctionLibrary::GetAbsItemOrder(index, EKITBAGTYPE::SPACE_COPY_BAG);
	UItemBase* item = FindItemByOrder(order);
	if (IsValid(item))
	{
		UItemUse* ItemUse = Cast<UItemUse>(item);
		if (IsValid(ItemUse))
		{
			AServerCharacter* player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
			ItemUse->Use(player);
		}
	}
}
void URoleKitBagInterface::CLIENT_GreyItem_Implementation(const int32& ItemID)
{

}

void URoleKitBagInterface::CLIENT_ClearGreyItem_Implementation(const int32& ItemID)
{

}

void URoleKitBagInterface::CLIENT_ShowItemListIcon(const FVariant& dictStrInt)
{
	FDICT_STR_INT TempList = FDICT_STR_INT(dictStrInt);
	const TMap<FString, int32> data(TempList.dictDataList);
	OnShowItemListIcon(data);
}

UItemBase * URoleKitBagInterface::getItemByHyperLinkString(const FString & dataString)
{
		FString jsonStr = dataString.Replace(TEXT("/"), TEXT("\""));
		UJsonFieldData* temp = UJsonFieldData::Create(this);
		auto returnvalue = temp->FromString(jsonStr);
		auto itemdata = returnvalue->GetObject(TEXT("ROOT"));
		int32 itemid = FSTRING_TO_INT(itemdata->GetString(TEXT("id")));
		UItemBase* ItemBase = UItemFactory::GetItemByID(itemid);
		if (IsValid(ItemBase) && ItemBase->IsEquip())
		{
			UEquip* Equip = Cast<UEquip>(ItemBase);
			Equip->UID = itemdata->GetString(TEXT("uid"));
			Equip->Amount = FSTRING_TO_INT(itemdata->GetString(TEXT("amount")));
			Equip->BindType = FSTRING_TO_INT(itemdata->GetString(TEXT("bindType")));
			Equip->Hardiness = FSTRING_TO_INT(itemdata->GetString(TEXT("hardiness")));
			Equip->CombatPower = FSTRING_TO_INT(itemdata->GetString(TEXT("combatPower")));
			Equip->AttackPropertiesStr = itemdata->GetString(TEXT("attackProperties")).Replace(TEXT("_"), TEXT("|"));
			Equip->AttachPropertiesStr = itemdata->GetString(TEXT("attachProperties")).Replace(TEXT("_"), TEXT("|"));
			Equip->IntensifyDataStr = itemdata->GetString(TEXT("intensifyData")).Replace(TEXT("_"), TEXT("|"));
			return Equip;
		}
		else
		{
			ItemBase->UID = itemdata->GetString(TEXT("uid"));
			ItemBase->Amount = FSTRING_TO_INT(itemdata->GetString(TEXT("amount")));
			ItemBase->BindType = FSTRING_TO_INT(itemdata->GetString(TEXT("bindType")));
			return ItemBase;
		}
	return nullptr;
}


void URoleKitBagInterface::GetMeltingEquipUID(TArray<FString>& EquipUIDArr)
{
	TArray<UItemBase*> Items = GetItemsByKBType(EKITBAGTYPE::COMMON);
	for (auto item : Items)
	{
		if (CheckMelting(item))
		{
			EquipUIDArr.Add(item->UID);
		}
	}
}

bool URoleKitBagInterface::CheckMelting(UItemBase* ItemBase)
{
	if (ItemBase->IsEquip())
	{
		UEquipPart* equipPart = Cast<UEquipPart>(ItemBase);
		if (equipPart)
		{
			//半成品，淬炼次数小于10次
			if (equipPart->quenchingNum < 10)
			{
				return true;
			}
		}
		//品质蓝色及以下，需求等级大于等于30
		else if (ItemBase->Quality <= int(QUALITY::QUALITY_BLUE) && ItemBase->ReqLevel >= 30)
		{
			return true;
		}
	}
	return false;
}

void URoleKitBagInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_removeItem");
	ArrBlueFunc.Add("CLIENT_swapItemAC");
	ArrBlueFunc.Add("CLIENT_requestSortKitBagCB");
	ArrBlueFunc.Add("CLIENT_openInputKBPW");
	ArrBlueFunc.Add("CLIENT_hideKBLockWin");
	ArrBlueFunc.Add("CLIENT_AddToItemUseAmountArray");
	ArrBlueFunc.Add("CLIENT_UpdateItemUseAmount");
	ArrBlueFunc.Add("CLIENT_endSort");
	ArrBlueFunc.Add("CLIENT_requestOpenStoreWindow");
	ArrBlueFunc.Add("CLIENT_OnUnLockStoreGridNumChange");
	ArrBlueFunc.Add("CLIENT_OnStoreMoneyChange");
	ArrBlueFunc.Add("CLIENT_ShowNextLevelGift");
	ArrBlueFunc.Add("CLIENT_ShowLevelGift");
	ArrBlueFunc.Add("CLIENT_removeStoreItem");
	ArrBlueFunc.Add("CLIENT_swapStoreItemAC");
	ArrBlueFunc.Add("CLIENT_swapItemFromBagToStore");
	ArrBlueFunc.Add("CLIENT_removeTongStoreItem");
	ArrBlueFunc.Add("CLIENT_swapTongStoreItemAC");
	ArrBlueFunc.Add("CLIENT_swapItemFromBagToTongStore");
	ArrBlueFunc.Add("CLIENT_GreyItem");
	ArrBlueFunc.Add("CLIENT_ClearGreyItem");
	ArrBlueFunc.Add("CLIENT_OnSetGridEnabledByOrderID");
	ArrBlueFunc.Add("OnBeforeRemoveItemBP");
	Supper::InitBlueCB();
}

bool URoleKitBagInterface::_CheckSwapOrder(const int32& FromAbsOrder, const int32& ToAbsOrder, UItemBase* FromItem, UItemBase* ToItem)
{
	EKITBAGTYPE fromBagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(FromAbsOrder);
	EKITBAGTYPE toBagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(ToAbsOrder);
	if (toBagType == EKITBAGTYPE::COMMON)
	{
		if (IsValid(FromItem))
		{
			if (FromItem->isQuest() || FromItem->isSpar())
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(1606, "");
				return false;
			}
		}
	}
	else if (toBagType == EKITBAGTYPE::CRYSTAL)
	{
		if (IsValid(FromItem) && !FromItem->isSpar())
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1605, "");
			return false;
		}
	}
	else if (toBagType == EKITBAGTYPE::QUEST)
	{
		if (IsValid(FromItem) && !FromItem->isQuest())
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1607, "");
			return false;
		}
	}
	else if (toBagType == EKITBAGTYPE::STORE)
	{
		if (fromBagType == EKITBAGTYPE::TONG_STORE)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1608, "");
			return false;
		}
		if (fromBagType == EKITBAGTYPE::QUEST)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1604, "");
			return false;
		}
	}
	else if (toBagType == EKITBAGTYPE::TONG_STORE)
	{
		if (fromBagType == EKITBAGTYPE::STORE)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1608, "");
			return false;
		}
		if (fromBagType == EKITBAGTYPE::QUEST)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1604, "");
			return false;
		}
	}
	
	return true;
}

void URoleKitBagInterface::_RequestSwapItem(const int32& FromAbsOrder, const int32& ToAbsOrder)
{
	KBEngine::FVariantArray args;
	args.Add(INT_TO_FSTRING(FromAbsOrder));
	args.Add(INT_TO_FSTRING(ToAbsOrder));
	EKITBAGTYPE fromBagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(FromAbsOrder);
	EKITBAGTYPE toBagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(ToAbsOrder);
	if (nullptr != GetEntity())
	{
		if (toBagType == EKITBAGTYPE::STORE || fromBagType == EKITBAGTYPE::STORE)
		{
			GetEntity()->CellCall(TEXT("CELL_swapStoreItem"), args);
		}
		else if (toBagType == EKITBAGTYPE::TONG_STORE || fromBagType == EKITBAGTYPE::TONG_STORE)
		{
			GetEntity()->CellCall(TEXT("CELL_swapTongStoreItem"), args);
		}
		else
		{
			GetEntity()->CellCall(TEXT("CELL_swapItem"), args);
		}
	}
}

bool URoleKitBagInterface::IsBagFull(EKITBAGTYPE BagType)
{
	TArray<UItemBase*> ItemList = GetItemsByKBType(BagType);
	switch (BagType)
	{
	case EKITBAGTYPE::COMMON:
	{
		if (ItemList.Num() >= commonCapacity + unLockGridNum)
			return true;
		break;
	}
	case EKITBAGTYPE::CRYSTAL:
	{
		if (ItemList.Num() >= crystalCapacity) 
			return true;
		break;
	}
	case EKITBAGTYPE::QUEST:
	{
		if (ItemList.Num() >= questCapacity) 
			return true;
		break;
	}
	case EKITBAGTYPE::STORE:
	{
		if (ItemList.Num() >= STORE_CAPACITY + unLockStoreGridNum)
			return true;
		break;
	}
	}
	return false;
}


void URoleKitBagInterface::OnUseItemByPos(FString UID, FVector Pos)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::OnUseItemByPos : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UID);
	args.Add(Pos);
	GetEntity()->CellCall(TEXT("CELL_useItemByPos"), args);
}

void URoleKitBagInterface::OnUseItemByPosAndDir(FString UID, FVector Pos, FVector Dir)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::OnUseItemByPos : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UID);
	args.Add(Pos);
	args.Add(Dir);
	GetEntity()->CellCall(TEXT("CELL_useItemByPosAndDir"), args);
}

void URoleKitBagInterface::requestSortKitBag(int32 kbType)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::requestSortKitBag : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)kbType);
	GetEntity()->CellCall(TEXT("CELL_requestSortKitBag"), args);
}

void URoleKitBagInterface::startSort(int32 kbType)
{
	bIsSort = true;
	requestSortKitBag(kbType);
}

void URoleKitBagInterface::CLIENT_endSort()
{
	bIsSort = false;
	OnKitBagEndSort.Broadcast();
	NotifyEndSort();
}
void URoleKitBagInterface::CLIENT_AddToItemUseAmountArray(const int32 itemId, const int32 number, const FString createTime)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("--AddToItemUseAmountArray---itemId = %d--number = %d--"), itemId, number);
	FItemUseAmountInfo tempData;
	tempData.ItemID = itemId;
	tempData.ItemUseAmount = number;
	tempData.ItemCreateTime = createTime;
	ItemUseAmountArray.Add(tempData);
}

int32 URoleKitBagInterface::GetItemUseAmountByItemID(const int32 itemID)
{
	int32 useAmount = -1;
	for (auto item : ItemUseAmountArray)
	{
		if (item.ItemID == itemID)
		{
			useAmount = item.ItemUseAmount;
		}
	}
	return useAmount;
}

FString URoleKitBagInterface::GetItemUseCreateTimeByItemID(const int32 itemID)
{
	FString createTime = "";
	for (auto item : ItemUseAmountArray)
	{
		if (item.ItemID == itemID)
		{
			createTime = item.ItemCreateTime;
		}
	}
	return createTime;
}

void URoleKitBagInterface::CLIENT_UpdateItemUseAmount(const int32 itemId, const int32 number, const FString newRefreshTime)
{
	for (FItemUseAmountInfo& item : ItemUseAmountArray)
	{
		if (item.ItemID == itemId)
		{
			item.ItemCreateTime = newRefreshTime;
			item.ItemUseAmount = number;
		}
	}
}

void URoleKitBagInterface::RPC_unLockStoreGrid()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_unLockStoreGrid : entity!"));
		return;
	}
	//当前解锁的格子
	int32 GridIndex = STORE_CAPACITY + unLockStoreGridNum;
	int32 ItemOrder = UGolbalBPFunctionLibrary::GetAbsItemOrder(GridIndex, EKITBAGTYPE::STORE);

	KBEngine::FVariantArray args;
	args.Add(INT_TO_FSTRING(ItemOrder));

	entity->BaseCall(TEXT("unLockStoreGrid"), args);
}

void URoleKitBagInterface::RPC_requestRemoveStoreItem(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requestRemoveStoreItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->BaseCall(TEXT("requestRemoveStoreItem"), args);
}

void URoleKitBagInterface::RPC_splitStoreItem(const int32& INT32_1, const int32& INT32_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_splitStoreItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	args.Add(INT32_2);

	entity->BaseCall(TEXT("splitStoreItem"), args);
}

void URoleKitBagInterface::RPC_swapItem(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_swapItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("CELL_swapItem"), args);
}

void URoleKitBagInterface::RPC_unWieldEquip(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_unWieldEquip : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_unWieldEquip"), args);
}

void URoleKitBagInterface::RPC_requestRemoveItemByUID(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requestRemoveItemByUID : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("requestRemoveItemByUID"), args);
}

void URoleKitBagInterface::RPC_useItem(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_useItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("CELL_useItem"), args);
}

void URoleKitBagInterface::RPC_uesItemByShortcutBar(const int32& ItemID, const int32& TargetID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_uesItemByShortcutBar : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(ItemID);
	args.Add(TargetID);

	entity->CellCall(TEXT("CELL_uesItemByShortcutBar"), args);
}

void URoleKitBagInterface::RPC_unLockGrid()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_unLockGrid : entity!"));
		return;
	}
	//当前解锁的格子
	int32 GridIndex = COMMON_BAG_CAPACITY + unLockGridNum;
	int32 ItemOrder = UGolbalBPFunctionLibrary::GetAbsItemOrder(GridIndex, EKITBAGTYPE::COMMON);

	KBEngine::FVariantArray args;
	args.Add(INT_TO_FSTRING(ItemOrder));

	entity->CellCall(TEXT("CELL_unLockGrid"), args);
}

void URoleKitBagInterface::RPC_requestSortKitBag(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requestSortKitBag : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);

	entity->CellCall(TEXT("CELL_requestSortKitBag"), args);
}

void URoleKitBagInterface::RPC_requsetSetPW(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requsetSetPW : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("CELL_requsetSetPW"), args);
}

void URoleKitBagInterface::RPC_unLockKB(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_unLockKB : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_unLockKB"), args);
}

void URoleKitBagInterface::RPC_cancelKBPW(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_resetKBPW : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_cancelPW"), args);
}

void URoleKitBagInterface::RPC_resetKBPW()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_resetKBPW : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_resetKBPW"), args);
}

void URoleKitBagInterface::RPC_cancelResetKBPW()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_cancelResetKBPW : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_cancelResetKBPW"), args);
}

void URoleKitBagInterface::RPC_LockKB()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_LockKB : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_LockKB"), args);
}

void URoleKitBagInterface::RPC_requestSaveMoney(const int64& MoneyValue)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requestSaveMoney : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT64_TO_FSTRING(MoneyValue));

	entity->CellCall(TEXT("CELL_requestSaveMoney"), args);
}

void URoleKitBagInterface::RPC_requestTakeMoney(const int64& MoneyValue)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requestTakeMoney : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT64_TO_FSTRING(MoneyValue));

	entity->CellCall(TEXT("CELL_requestTakeMoney"), args);
}

void URoleKitBagInterface::RPC_requestSaveItem(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requestSaveItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_requestSaveItem"), args);
}

void URoleKitBagInterface::RPC_requestTakeItem(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_requestTakeItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_requestTakeItem"), args);
}

void URoleKitBagInterface::RPC_swapStoreItem(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleKitBagInterface::RPC_swapStoreItem : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("CELL_swapStoreItem"), args);
}

FKITBAG_GRID_COST URoleKitBagInterface::GetKitBagGridCost(int32& GridIndex)
{
	FKITBAG_GRID_COST KitgagGridCost;
	
	int32 LockIndex = unLockGridNum + 1;
	GridIndex = COMMON_BAG_CAPACITY + LockIndex;

	auto CostTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_KITBAG_GRID_COST);
	const FKITBAG_GRID_COST* CostData = CostTable->GetRow<FKITBAG_GRID_COST>(FSTRING_TO_FNAME(INT_TO_FSTRING(LockIndex)));
	if (CostData != nullptr)
	{
		KitgagGridCost.ItemCost = CostData->ItemCost;
		KitgagGridCost.ItemID = CostData->ItemID;
		KitgagGridCost.MoneyCost = CostData->MoneyCost;
	}
	else
	{
		CS3_Warning(TEXT("-->GetKitBagGridCost error: Can not find Row :%d!"), LockIndex);
		KitgagGridCost.ItemCost = 0;
		KitgagGridCost.ItemID = 0;
		KitgagGridCost.MoneyCost = 0;
	}

	return KitgagGridCost;
}

FKITBAG_GRID_COST URoleKitBagInterface::GetStoreGridCost(int32& GridIndex)
{
	FKITBAG_GRID_COST StoreGridCost;

	int32 LockIndex = unLockStoreGridNum + 1;
	GridIndex = STORE_CAPACITY + LockIndex;

	auto CostTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STORE_GRID_COST);
	const FKITBAG_GRID_COST* CostData = CostTable->GetRow<FKITBAG_GRID_COST>(FSTRING_TO_FNAME(INT_TO_FSTRING(LockIndex)));
	if (CostData != nullptr)
	{
		StoreGridCost.ItemCost = CostData->ItemCost;
		StoreGridCost.ItemID = CostData->ItemID;
		StoreGridCost.MoneyCost = CostData->MoneyCost;
	}
	else
	{
		CS3_Warning(TEXT("-->GetStoreGridCost error: Can not find Row :%d!"), LockIndex);
		StoreGridCost.ItemCost = 0;
		StoreGridCost.ItemID = 0;
		StoreGridCost.MoneyCost = 0;
	}

	return StoreGridCost;
}

CONTROL_COMPILE_OPTIMIZE_END
