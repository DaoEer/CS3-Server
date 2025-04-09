// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleBuyNPCShopInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/EnumCsvDefine.h"
#include "KBEngine.h"
#include "JsonFieldData.h"
#include "Manager/CfgManager.h"
#include "Util/ConvertUtil.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/ConstData.h"
#include "Util/CS3Debug.h"
#include "Kismet/KismetStringLibrary.h"
#include "GameData/Item/ItemFactory.h"
#include "Manager/MessageManager.h"
#include "RoleTongInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleBuyNPCShopInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OpenTraviaShop, &URoleBuyNPCShopInterface::CLIENT_OpenTraviaShop, const int32&, const FVariant&, const FVariant&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_InitNPCShopItemList, &URoleBuyNPCShopInterface::InitNPCShopItemList, const int32&, const FString&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_InitNPCShopItemListByDiscount, &URoleBuyNPCShopInterface::InitNPCShopItemListByDiscount, const int32&, const FString&, const FVariant&, const float&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnInitBuyBackItemList, &URoleBuyNPCShopInterface::CLIENT_OnInitBuyBackItemList, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequestSellItem, &URoleBuyNPCShopInterface::CLIENT_OnRequestSellItem, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestBuyBackItem, &URoleBuyNPCShopInterface::OnRequestBuyBackItem, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_InitLHMJShopData, &URoleBuyNPCShopInterface::CLIENT_InitLHMJShopData, const int32&, const FString&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_reflashLHMJShopData, &URoleBuyNPCShopInterface::CLIENT_reflashLHMJShopData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_autoReflashLHMJShopData, &URoleBuyNPCShopInterface::CLIENT_autoReflashLHMJShopData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_LockTongShop, &URoleBuyNPCShopInterface::CLIENT_LockTongShop)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UnLockTongShop, &URoleBuyNPCShopInterface::CLIENT_UnLockTongShop)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnTongPlunderShopSellStart, &URoleBuyNPCShopInterface::OnTongPlunderShopSellStart, const FVariant&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_TongPlunderShopSellEnd, &URoleBuyNPCShopInterface::CLIENT_TongPlunderShopSellEnd)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnTongPlunderShopItemBuySuccess, &URoleBuyNPCShopInterface::OnTongPlunderShopItemBuySuccess, const FString&, const int&, const int&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onNotifyRandomItemSellEndTime, &URoleBuyNPCShopInterface::onNotifyRandomItemSellEndTime, const FString&, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleBuyNPCShopInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleBuyNPCShopInterface::URoleBuyNPCShopInterface()
{
}

URoleBuyNPCShopInterface::~URoleBuyNPCShopInterface()
{
}

void URoleBuyNPCShopInterface::InitNPCShopItemList(const int32& nid, const FString& sid, const FVariant& fixedDict )
{
	FNPCSHOP_ITEM_LIST itemList( fixedDict);
	npcID = nid;
	shopID = sid;
	ShopType = NPCSHOP_TYPE::COMMON_TYPE;
	if (NPCShopDatas.Contains(sid))
	{
		NPCShopDatas.Remove(sid);
	}

	InitShopDatas(sid);
	InitRandomShopDatas(sid, itemList.items1);
	
	for (auto item : itemList.items1)
	{
		TMap<FString, float> times;
		if (NPCShopDatas.Contains(sid) && NPCShopDatas[sid].Contains(item.id1))
		{
			NPCShopDatas[sid][item.id1].Amount = item.amount2;
			times.Add(item.id1, item.startTime3);
		}
		ShopServerTime.Add(sid, times);
	}
	CLIENT_InitNPCShopItemList();
}

void URoleBuyNPCShopInterface::InitNPCShopItemListByDiscount(const int32& nid, const FString& sid, const FVariant& fixedDict, const float& discount)
{
	FNPCSHOP_ITEM_LIST itemList(fixedDict);
	npcID = nid;
	shopID = sid;
	ShopType = NPCSHOP_TYPE::COMMON_TYPE;
	if (NPCShopDatas.Contains(sid))
	{
		NPCShopDatas.Remove(sid);
	}
	
	InitShopDatas(sid);
	InitRandomShopDatas(sid, itemList.items1);

	// 计算折扣
	for (auto it = NPCShopDatas[sid].CreateIterator(); it; ++it)
	{
		TArray<FString> SplitStr = UGolbalBPFunctionLibrary::SplitString(it.Value().Price, false, ",");
		it.Value().Price.Empty();
		for (auto& str : SplitStr )
		{
			TArray<FString> subStr = UGolbalBPFunctionLibrary::SplitString(str, false, ":");
			if (subStr.Num() >= 2)
			{
				it.Value().Price += subStr[0] + ":";
				FString endStr(TEXT(""));
				if (subStr[1].RemoveFromEnd(TEXT("}")))
				{
					endStr = "}";
				}
				else
				{
					endStr = ",";
				}
				int price = FSTRING_TO_INT(subStr[1])  * discount * 0.1;
				it.Value().Price += INT_TO_FSTRING(price);
				it.Value().Price += endStr;
			}	
		}
	}
	
	for (auto item : itemList.items1)
	{
		TMap<FString, float> times;
		if (NPCShopDatas.Contains(sid) && NPCShopDatas[sid].Contains(item.id1))
		{
			NPCShopDatas[sid][item.id1].Amount = item.amount2;
			times.Add(item.id1, item.startTime3);
		}
		ShopServerTime.Add(sid, times);
	}
	CLIENT_InitNPCShopItemList();
}

void URoleBuyNPCShopInterface::requestBuyNPCShopItem(const FString& slot, int itemID, int amount)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyNPCShopItem : GetEntity()!"));
		return;
	}

	//帮会商店没有npc
	if (!shopID.Equals("TongShop"))
	{
		KBEngine::Entity* npcEntity = UGolbalBPFunctionLibrary::FindEntity(npcID);
		if (npcEntity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyNPCShopItem : npcEntity!"));
			return;
		}
		auto NpcActor = npcEntity->Actor();
		auto SelfActor = GetEntity()->Actor();
		if (!IsValid(NpcActor) || !IsValid(SelfActor))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyNPCShopItem : NpcActor||SelfActor!"));
			return;
		}
		if (UGolbalBPFunctionLibrary::GetActorDistance(NpcActor, SelfActor) > 1000)
		{
			return;
		}
	}

	if (ShopType == NPCSHOP_TYPE::COMMON_TYPE)
	{
		KBEngine::FVariantArray Args;
		Args.Add(shopID);
		Args.Add(slot);
		Args.Add(itemID);
		Args.Add(amount);
		GetEntity()->CellCall(TEXT("requestBuyNPCShopItem"), Args);
	}
	else
	{
		RequestBuyLHMJShopItem(slot, itemID, amount);
	}
}

void URoleBuyNPCShopInterface::CLIENT_OnSuccessBuyShopItem_Implementation(const FString& sid, const FString& slot, int itemID, int amount)
{
	if (sid != shopID)
	{
		return;
	}
	if (NPCShopDatas.Contains(sid) && NPCShopDatas[sid].Contains(slot))
	{
		if (NPCShopDatas[sid][slot].Amount >= 0)
		{
			NPCShopDatas[sid][slot].Amount -= amount;
		}
		 
	}
}

void URoleBuyNPCShopInterface::requestSellItem(const FString& itemuid)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestSellItem : GetEntity()!"));
		return;
	}
	if (!shopID.Equals("TongShop"))
	{ 
		KBEngine::Entity* npcEntity = UGolbalBPFunctionLibrary::FindEntity(npcID);
		if (npcEntity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestSellItem : npcEntity!"));
			return;
		}
		auto NpcActor = npcEntity->Actor();
		auto SelfActor = GetEntity()->Actor();
		if (!IsValid(NpcActor) || !IsValid(SelfActor))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestSellItem : NpcActor||SelfActor!"));
			return;
		}
	
		if (UGolbalBPFunctionLibrary::GetActorDistance(NpcActor, SelfActor) > 1000)
		{
			return;
		}
	}
	KBEngine::FVariantArray Args;
	Args.Add(shopID);
	Args.Add(itemuid);
	GetEntity()->CellCall(TEXT("requestSellItem"), Args);
}

void URoleBuyNPCShopInterface::requestBuyBackItem(const FString& itemuid)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyBackItem : GetEntity()!"));
		return;
	}

	//帮会掠夺 没有npcid
	if (!shopID.Equals("TongShop"))
	{
		KBEngine::Entity* npcEntity = UGolbalBPFunctionLibrary::FindEntity(npcID);
		if (npcEntity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyBackItem : npcEntity!"));
			return;
		}
		auto NpcActor = npcEntity->Actor();
		auto SelfActor = GetEntity()->Actor();
		if (!IsValid(NpcActor) || !IsValid(SelfActor))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyBackItem : NpcActor||SelfActor!"));
			return;
		}
		if (UGolbalBPFunctionLibrary::GetActorDistance(NpcActor, SelfActor) > 1000)
		{
			return;
		}
	}
	KBEngine::FVariantArray Args;
	Args.Add(shopID);
	Args.Add(itemuid);
	GetEntity()->CellCall(TEXT("requestBuyBackItem"), Args);
}

void URoleBuyNPCShopInterface::CLIENT_OnRequestSellItem(const FVariant& Var)
{
	BUY_BACK_ITEM_DATA data = BUY_BACK_ITEM_DATA(Var);
	FBuyBackItemData  buyBackItemData;
	buyBackItemData.Id = data.id;
	buyBackItemData.Uid = data.uid;
	buyBackItemData.Amount = data.amount;
	buyBackItemData.BindType = data.bindType;
	buyBackItemData.CombatPower = data.combatPower;
	buyBackItemData.AttachPropertiesStr = data.attachPropertiesStr;
	buyBackItemData.AttackPropertiesStr = data.attackPropertiesStr;
	buyBackItemData.IntensifyDataStr = data.intensifyDataStr;
	buyBackItemData.Hardiness = data.hardiness;
	OnRequestSellItem(buyBackItemData);
}

void URoleBuyNPCShopInterface::OnRequestSellItem_Implementation(const FBuyBackItemData& buyBackItemData)
{
	UItemBase* Item = GetItemByString(buyBackItemData);
	//插入到最前面，最新的显示在第一个
	BuyBackDatas.Insert(Item, 0);
	if (BuyBackDatas.Num() > 10)
	{
		//删除数组最后一个数据（即最老的数据）
		BuyBackDatas.RemoveAt(BuyBackDatas.Num() - 1);
	}
	//因为是插入到前面，所以界面更新需要全部物品数据刷一遍
	OnUpdateBuyBackItemList();
}

void URoleBuyNPCShopInterface::OnRequestBuyBackItemBP_Implementation(const FBuyBackItemData& buyBackItemData)
{
	UItemBase* Item = GetItemByString(buyBackItemData);
	for (UItemBase* ItemBase : BuyBackDatas)
	{
		if (ItemBase->UID == Item->UID)
		{
			BuyBackDatas.Remove(ItemBase);
			OnUpdateBuyBackItemList();
			return;
		}
	}
}

void URoleBuyNPCShopInterface::OnRequestBuyBackItem(const FVariant& Var)
{
	SIMPLE_ITEM_DICT data = SIMPLE_ITEM_DICT(Var);
	FBuyBackItemData  buyBackItemData;
	buyBackItemData.Id = data.id;
	buyBackItemData.Uid = FString::Printf( TEXT("%llu"), data.uid);
	buyBackItemData.Amount = data.amount;
	buyBackItemData.BindType = data.bindType;
	OnRequestBuyBackItemBP(buyBackItemData);
}

#pragma region	/** 高级回购，目前已删除这个功能，代码暂不删 */
void URoleBuyNPCShopInterface::requestBuyBackHighItem(const FString& itemuid)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyBackHighItem : GetEntity()!"));
		return;
	}
	KBEngine::Entity* npcEntity = UGolbalBPFunctionLibrary::FindEntity(npcID);
	if (npcEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyBackHighItem : npcEntity!"));
		return;
	}
	auto NpcActor = npcEntity->Actor();
	auto SelfActor = GetEntity()->Actor();
	if (!IsValid(NpcActor) || !IsValid(SelfActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::requestBuyBackHighItem : NpcActor||SelfActor!"));
		return;
	}
	if (UGolbalBPFunctionLibrary::GetActorDistance(NpcActor, SelfActor) > 1000)
	{
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(shopID);
	Args.Add(itemuid);
	GetEntity()->CellCall(TEXT("requestBuyBackHighItem"), Args);
}

void URoleBuyNPCShopInterface::addHighBuyBackItem_Implementation(const FString& data)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("++++data++++ = %s"), *data);
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(data);
	auto value = returnvalue->GetObjectArray(this, TEXT("ROOT"));
	for (auto item : value)
	{
		auto itemUID = item->GetString(TEXT("uid"));
		FDateTime t = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(_tstof(*item->GetString(TEXT("time"))));
		highBuyBackTime.Add(itemUID, t);
		highBuyBackItem.Add(itemUID, data);
		addHighBuyBackItemCB(t, data);
	}
}

void URoleBuyNPCShopInterface::subHighBuyBackItem_Implementation(const FString& uid)
{
	//FDateTime time = *highBuyBackTime->Find(uid);
	//FString item = getHighBuyBackItem(uid);
	highBuyBackTime.Remove(uid);
	highBuyBackItem.Remove(uid);
	subHighBuyBackItemCB(uid);
}

TArray<FString> URoleBuyNPCShopInterface::getHighBuyBackUID()
{
	TArray<FString> uid;
	highBuyBackItem.GetKeys(uid);
	return uid;
}

FString URoleBuyNPCShopInterface::getHighBuyBackItem(const FString& uid)
{
	return *highBuyBackItem.Find(uid);
}

FDateTime URoleBuyNPCShopInterface::getHighBuyBackTime(const FString& uid)
{
	return *highBuyBackTime.Find(uid);
}
#pragma endregion

int32 URoleBuyNPCShopInterface::getItemMapLength()
{
	if (NPCShopDatas.Contains(shopID))
	{
		NPCShopDatas[shopID].Num();
	}
	return 0;
}

TArray<FString> URoleBuyNPCShopInterface::getItemMapKeys()
{
	TArray<FString> itemKeys;
	if (NPCShopDatas.Contains(shopID))
	{
		NPCShopDatas[shopID].GetKeys(itemKeys);
	}
	return itemKeys;
}

FNPCShopData URoleBuyNPCShopInterface::getShopItemBySlot(const FString& slot)
{
	if (NPCShopDatas.Contains(shopID) && NPCShopDatas[shopID].Contains(slot))
	{
		return NPCShopDatas[shopID][slot];
	}
	FNPCShopData Shop;
	return Shop;
}

float URoleBuyNPCShopInterface::getShopItemStarTime(const FString& slot)
{
	if (ShopServerTime.Contains(shopID) && ShopServerTime[shopID].Contains(slot))
	{
		return ShopServerTime[shopID][slot];
	}
	return 0.0;
}

TMap<FString, int32> URoleBuyNPCShopInterface::GetGoodsPrice(FNPCShopData ShopData)
{
	TMap<FString, int32> ReturnPriceMap;
	FString ShopPrice = ShopData.Price;
	FString TempStr = UKismetStringLibrary::GetSubstring(ShopPrice, 1, (ShopPrice.Len() - 2));
	TArray<FString> PriceArray = UGolbalBPFunctionLibrary::SplitString(TempStr, false, TEXT(","));
	for (FString PriceStr : PriceArray)
	{
		TArray<FString> TempPriceArray = UGolbalBPFunctionLibrary::SplitString(PriceStr, false, TEXT(":"));
		if (TempPriceArray.Num() >= 2)
		{
			//去掉前后的空格，工具导表的时候会自动在逗号后面增加空格
			FString PriceTypeStr = TempPriceArray[0].TrimStartAndEnd();
			int32 PriceValue = FSTRING_TO_INT(TempPriceArray[1].TrimStartAndEnd());
			//去掉前后的单引号
			FString PriceType = UKismetStringLibrary::GetSubstring(PriceTypeStr, 1, (PriceTypeStr.Len() - 2));
			//只有金币价格与出售比挂钩，其他货币与出售比无关
			if (PriceType == TEXT("money") | PriceType == TEXT("bindmoney"))
			{
				PriceValue = floor(PriceValue * NPCSHOP_SELL_RATIO);
				ReturnPriceMap.Add(PriceType, PriceValue);
			}
			else
			{
				ReturnPriceMap.Add(PriceType, PriceValue);
			}
		}
	}
	return ReturnPriceMap;
}

TMap<FString, FString> URoleBuyNPCShopInterface::GetGoodsCondition(FString Condition, TArray<FString>& ConditionKeys)
{
	TArray<FString> TempConditionKeys;
	TMap<FString, FString> ReturnConditionMap;
	FString TempStr = UKismetStringLibrary::GetSubstring(Condition, 1, (Condition.Len() - 2));
	TArray<FString> ConditionArray = UGolbalBPFunctionLibrary::SplitString(TempStr, false, TEXT(","));
	for (FString ConditionStr : ConditionArray)
	{
		TArray<FString> TempConditionArray = UGolbalBPFunctionLibrary::SplitString(ConditionStr, false, TEXT(":"));
		if (TempConditionArray.Num() >= 2)
		{
			//去掉前后的空格，工具导表的时候会自动在逗号后面增加空格
			FString ConditionTypeStr = TempConditionArray[0].TrimStartAndEnd();
			FString ConditionValue = TempConditionArray[1].TrimStartAndEnd();
			//去掉前后的单引号
			FString ConditionType = UKismetStringLibrary::GetSubstring(ConditionTypeStr, 1, (ConditionTypeStr.Len() - 2));
			ReturnConditionMap.Add(ConditionType, ConditionValue);
			TempConditionKeys.Add(ConditionType);
		}
	}
	//按策划要求按照 帮会商店等级>玲珑玉令等级>军衔等级>境界等级>等级 排序
	if (TempConditionKeys.Contains(TEXT("tongShopLevel")))
	{
		ConditionKeys.Add(TEXT("tongShopLevel"));
	}
	else if (TempConditionKeys.Contains(TEXT("jadeItemLevel")))
	{
		ConditionKeys.Add(TEXT("jadeItemLevel"));
	}
	else if (TempConditionKeys.Contains(TEXT("militaryRankLevel")))
	{
		ConditionKeys.Add(TEXT("militaryRankLevel"));
	}
	else if (TempConditionKeys.Contains(TEXT("jingJieLevel")))
	{
		ConditionKeys.Add(TEXT("jingJieLevel"));
	}
	else if (TempConditionKeys.Contains(TEXT("playerLevel")))
	{
		ConditionKeys.Add(TEXT("playerLevel"));
	}
	return ReturnConditionMap;
}

FSHOP_TYPE_DATA URoleBuyNPCShopInterface::GetShopTypeConfig(const FString& ShopID, bool& Find)
{
	FSHOP_TYPE_DATA shopTypeData;
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager))
	{
		Find = false;
		return shopTypeData;
	}
	const UConfigTable* shopTypeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SHOP_TYPE_DATA);
	if (shopTypeTable)
	{
		const FSHOP_TYPE_DATA* ShopTypeData = const_cast<FSHOP_TYPE_DATA*>(shopTypeTable->GetRow<FSHOP_TYPE_DATA>(ShopID));
		if (ShopTypeData)
		{
			Find = true;
			return *ShopTypeData;
		}
	}
	Find = false;
	return shopTypeData;
}

void URoleBuyNPCShopInterface::GetShopPageIndexAndTabNames(TArray<int32>& PageIndexs, TArray<FString>& tabNames)
{
	TMap<int32, FString> TabsMap;//<PageIndex，Paging>
	if (NPCShopDatas.Contains(shopID))
	{
		for (TPair<FString, FNPCShopData>& Data : NPCShopDatas[shopID])
		{
			if (!TabsMap.Contains(Data.Value.PageIndex))
			{
				PageIndexs.Add(Data.Value.PageIndex);
				TabsMap.Add(Data.Value.PageIndex, Data.Value.Paging);
			}
		}
		if (PageIndexs.Num() <= 0)
		{
			return;
		}
		PageIndexs.Sort([](const int32 KeyA, const int32 KeyB)
		{
			return KeyA < KeyB;
		});
		for (int32 PageIndex : PageIndexs)
		{
			if (TabsMap.Contains(PageIndex))
			{
				tabNames.Add(TabsMap[PageIndex]);
			}
		}
	}
}

TArray<FNPCShopData> URoleBuyNPCShopInterface::GetShopGoodsDataByPageIndex(int32 PageIndex)
{
	TArray<FNPCShopData> ReturnData;
	if (NPCShopDatas.Contains(shopID))
	{
		for (TPair<FString, FNPCShopData>& Data : NPCShopDatas[shopID])
		{
			if (Data.Value.PageIndex == PageIndex)
			{
				ReturnData.Add(Data.Value);
			}
		}
	}
	ReturnData.Sort([](const FNPCShopData& A, const FNPCShopData& B)
	{
		//商品ID排序
		if (FSTRING_TO_FLOAT(A.Id) > FSTRING_TO_FLOAT(B.Id))
		{
			return false;
		}
		return true;
	});
	TWeakObjectPtr<URoleBuyNPCShopInterface> DelayThisPtr(this);
	ReturnData.Sort([DelayThisPtr](const FNPCShopData& A, const FNPCShopData& B)
	{
		//是否置灰
		if (DelayThisPtr.IsValid())
		{
			URoleBuyNPCShopInterface* ThisPtr = DelayThisPtr.Get();
			if (!ThisPtr->CheckIsUnEnable(A.Condition) && ThisPtr->CheckIsUnEnable(B.Condition))
			{
				return false;
			}
		}
		return true;
	});
	return ReturnData;
}

FNPCShopData URoleBuyNPCShopInterface::GetShopGoodsDataByGoodsID(FString GoodsID)
{
	if (NPCShopDatas.Contains(shopID) && NPCShopDatas[shopID].Contains(GoodsID))
	{
		return NPCShopDatas[shopID][GoodsID];
	}
	FNPCShopData NPCShopItemData;
	return NPCShopItemData;
}

UItemBase* URoleBuyNPCShopInterface::GetBuyBackDataByUID(FString UID)
{
	for (UItemBase* Data : BuyBackDatas)
	{
		if (Data->UID == UID)
		{
			return Data;
		}
	}
	return nullptr;
}

int32 URoleBuyNPCShopInterface::GetCanBuyMaxCount(int32 Amount, int32 ItemID)
{
	FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(ItemID);
	FString AtackAmont = ItemData.StackAmount;
	TArray<FString> NPCIDArray = UGolbalBPFunctionLibrary::SplitString(ItemData.StackAmount, false, TEXT("|"));
	if (NPCIDArray.Num() > 1)
	{
		if (NPCIDArray[0] == TEXT("0") || Amount == -1)
		{
			return FSTRING_TO_INT(NPCIDArray[1]);
		}
		else
		{
			return FMath::Min(FSTRING_TO_INT(NPCIDArray[1]), Amount);
		}
	}
	return 0;
}

bool URoleBuyNPCShopInterface::CheckIsUnEnable(FString Condition)
{
	TArray<FString> ConditionKeys;
	TMap<FString, FString> ConditionMap = GetGoodsCondition(Condition, ConditionKeys);
	//是否置灰只与帮会商店等级限制有关
	FString Key = TEXT("tongShopLevel");
	if (ConditionKeys.Contains(Key))
	{
		return CheckTradeConditionTongShopLevel(FSTRING_TO_INT(ConditionMap[Key]));
	}
	return true;
}

bool URoleBuyNPCShopInterface::CheckTradeConditionTongShopLevel(int32 ReqTongShopLevel)
{
	URoleTongInterface * TongInterface = Cast<URoleTongInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTongInterface"), 0));
	if (IsValid(TongInterface))
	{
		UTongObject* Tong = TongInterface->Tong;
		if (IsValid(Tong))
		{
			TMap<TONG_BUILD_TYPE, int32> TongBuildLevel = Tong->TongBuildLevel;
			int32 TongShopLevel = TongBuildLevel[TONG_BUILD_TYPE::TONG_BUILDING_TYPE_SD];
			if (TongShopLevel >= ReqTongShopLevel)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
	}
	return false;
}

void URoleBuyNPCShopInterface::RequestTongShop()
{
	KBEngine::FVariantArray args;
	args.Add(0);
	args.Add(TONG_SHOPID);
	CellCall(TEXT("requestTongShopItemList"), args);
}

#pragma region	/** 英雄王座商店 */
void URoleBuyNPCShopInterface::CLIENT_OpenTraviaShop(const int32& NPCID, const FVariant& GUARD_SOUL_DATAS_1, const FVariant& PAGODA_SOUL_DATA_1, const FVariant& DRUP_SOUL_DATAS_1)
{
	KBEngine::FVariantArray GUARD_SOUL_DATAS_1_ = GUARD_SOUL_DATAS_1.GetValue<KBEngine::FVariantArray>();
	TArray<FGUARD_SOUL_DATA> GUARD_SOUL_DATAS_1_A = TArray<FGUARD_SOUL_DATA>();
	for (FVariant& elementVariant0 : GUARD_SOUL_DATAS_1_)
	{
		FGUARD_SOUL_DATA element1 = FGUARD_SOUL_DATA(elementVariant0);
		GUARD_SOUL_DATAS_1_A.Add(element1);
	}

	KBEngine::FVariantArray PAGODA_SOUL_DATAS_1_ = PAGODA_SOUL_DATA_1.GetValue<KBEngine::FVariantArray>();
	TArray<FPAGODA_SOUL_DATA> PAGODA_SOUL_DATAS_1_A = TArray<FPAGODA_SOUL_DATA>();
	for (FVariant& elementVariant0 : PAGODA_SOUL_DATAS_1_)
	{
		FPAGODA_SOUL_DATA element1 = FPAGODA_SOUL_DATA(elementVariant0);
		PAGODA_SOUL_DATAS_1_A.Add(element1);
	}

	KBEngine::FVariantArray DRUP_SOUL_DATAS_1_ = DRUP_SOUL_DATAS_1.GetValue<KBEngine::FVariantArray>();
	TArray<FDRUP_SOUL_DATA> DRUP_SOUL_DATAS_1_A = TArray<FDRUP_SOUL_DATA>();
	for (FVariant& elementVariant0 : DRUP_SOUL_DATAS_1_)
	{
		FDRUP_SOUL_DATA element1 = FDRUP_SOUL_DATA(elementVariant0);
		DRUP_SOUL_DATAS_1_A.Add(element1);
	}

	AnalysisCombatSoul();
	AnalysisGuardSoul(GUARD_SOUL_DATAS_1_A);
	AnalysisPagodaSoul(PAGODA_SOUL_DATAS_1_A);
	npcID = NPCID;
	TArray<FDRUG_SOUL_SHOP_TYPE_DATA> drugShop;
	for (FDRUP_SOUL_DATA data : DRUP_SOUL_DATAS_1_A)
	{
		FDRUG_SOUL_SHOP_TYPE_DATA drug;
		drug.id = data.id1;
		drug.buyPrice = data.buyPrice3;
		drug.sellPrice = data.sellPrice2;

		drugShop.Add(drug);
	}
	OpenTraviaShop(NPCID, drugShop);
}

void URoleBuyNPCShopInterface::RequestBuyCombatSoulItem(const FString& itemID)
{
	KBEngine::FVariantArray param;
	param.Add(itemID);
	CellCall(TEXT("CELL_requestBuyCombatSoulItem"), param);
}

void URoleBuyNPCShopInterface::CLIENT_OnRequestBuyCombatSoulItem_Implementation(const FString& preItemID, const FString& itemID)
{
	int32 preID = FSTRING_TO_INT(preItemID);
	if (CombatSoulShop.Contains(preID))
	{
		if (itemID.Equals("0"))
		{
			CombatSoulShop[preID].NextItemID = 0;
		}
		else
		{
			CombatSoulShop.Remove(preID);
			UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
			const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COMBAT_SOUL_SHOP_DATA);
			if (ConfigTable)
			{
				TArray<FCOMBAT_SOUL_SHOP_TYPE_DATA*> CombatShops;
				ConfigTable->GetAllRows(CombatShops);
				for (auto CS : CombatShops)
				{
					if (FSTRING_TO_INT(itemID) == CS->ItemID)
					{
						FCOMBAT_SOUL_SHOP_TYPE_DATA data;
						data.BuyPrice = CS->BuyPrice;
						data.ItemID = CS->ItemID;
						data.NextItemID = CS->NextItemID == 0 ? CS->ItemID : CS->NextItemID;
						data.PreItemID = CS->PreItemID;
						data.SellPrice = CS->SellPrice;
						data.Type = CS->Type;
						data.Tip = CS->Tip;
						CombatSoulShop.Add(CS->ItemID, data);
					}
				}
			}
		}
		
		CombatSoulShop.KeySort(TLess<int32>());
	}
}

FString URoleBuyNPCShopInterface::GetNextCombatItemTip(const FString& itemID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COMBAT_SOUL_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FCOMBAT_SOUL_SHOP_TYPE_DATA*> CombatShops;
		ConfigTable->GetAllRows(CombatShops);
		int32 NextItemID(0);
		for (auto item : CombatShops)
		{
			if (INT_TO_FSTRING(item->ItemID) == itemID)
			{
				NextItemID = item->NextItemID;
			}
		}
		if (NextItemID != 0)
		{
			for (auto item : CombatShops)
			{
				if (item->ItemID == NextItemID)
				{
					return item->Tip;
				}
			}
		}
	}
	return FString("");
}

FCOMBAT_SOUL_SHOP_TYPE_DATA URoleBuyNPCShopInterface::GetPreCombatItem(const FString& itemID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COMBAT_SOUL_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FCOMBAT_SOUL_SHOP_TYPE_DATA*> CombatShops;
		ConfigTable->GetAllRows(CombatShops);
		int32 preItemID(0);
		for (auto item : CombatShops)
		{
			if (INT_TO_FSTRING(item->ItemID) == itemID)
			{
				preItemID = item->PreItemID;
				if (preItemID == 0)
				{
					return *item;
				}
				break;
			}
		}
		if (preItemID != 0)
		{
			for (auto item : CombatShops)
			{
				if (item->ItemID == preItemID)
				{
					return *item;
				}
			}
		}
	}
	return FCOMBAT_SOUL_SHOP_TYPE_DATA();
}

FCOMBAT_SOUL_SHOP_TYPE_DATA URoleBuyNPCShopInterface::GetNextCombatItem(const FString& itemID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COMBAT_SOUL_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FCOMBAT_SOUL_SHOP_TYPE_DATA*> CombatShops;
		ConfigTable->GetAllRows(CombatShops);
		int32 nextItemID(0);
		for (auto item : CombatShops)
		{
			if (INT_TO_FSTRING(item->ItemID) == itemID)
			{
				nextItemID = item->NextItemID;
				if (nextItemID == 0)
				{
					return *item;
				}
				break;
			}
		}
		if (nextItemID != 0)
		{
			for (auto item : CombatShops)
			{
				if (item->ItemID == nextItemID)
				{
					return *item;
				}
			}
		}
	}
	return FCOMBAT_SOUL_SHOP_TYPE_DATA();
}

void URoleBuyNPCShopInterface::RequestSellCombatSoulItem(const FString& itemID)
{
	KBEngine::FVariantArray param;
	param.Add(itemID);
	CellCall(TEXT("CELL_requestSellCombatSoulItem"), param);
}

void URoleBuyNPCShopInterface::CLIENT_OnRequestSellCombatSoulItem_Implementation(const FString& itemID)
{
	int32 id = FSTRING_TO_INT(itemID);
	if (CombatSoulShop.Contains(id))
	{
		CombatSoulShop.Remove(id);
	}
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COMBAT_SOUL_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FCOMBAT_SOUL_SHOP_TYPE_DATA*> CombatShops;
		ConfigTable->GetAllRows(CombatShops);
		int32 _id = GetInitialCombatItemID(itemID);

		for (auto item : CombatShops)
		{
			if (item->ItemID == _id)
			{
				CombatSoulShop.Add(id, *item);
			}
		}
		CombatSoulShop.KeySort(TLess<int32>());
	}
}

int32 URoleBuyNPCShopInterface::GetInitialCombatItemID(const FString& itemID)
{
	return FSTRING_TO_INT(itemID) / 10 * 10 + 1;
}

void URoleBuyNPCShopInterface::RequestBuyGuardSoul(const FString& scriptID, const int32& type)
{
	if (GuardBTimeMapping.Contains(scriptID) && GuardBTimeMapping[scriptID] >= 3)return;
	KBEngine::FVariantArray param;
	param.Add(scriptID);
	param.Add(type);
	CellCall(TEXT("CELL_requestBuyGuardSoul"), param);
}

void URoleBuyNPCShopInterface::CLIENT_OnRequestBuyGuardSoul_Implementation(const int32& callTimer, const FString& scriptID)
{
	if (GuardBTimeMapping.Contains(scriptID))
	{
		GuardBTimeMapping[scriptID] = callTimer;
	}
}

void URoleBuyNPCShopInterface::RequestUpdatePagodaSoul(const FString& srcScriptID, const FString& dstScriptID, const int32& wayType)
{
	KBEngine::FVariantArray param;
	param.Add(srcScriptID);
	param.Add(dstScriptID);
	param.Add(wayType);
	CellCall(TEXT("CELL_requestUpdatePagodaSoul"), param);
}

void URoleBuyNPCShopInterface::CLIENT_OnRequestUpdatePagodaSoul_Implementation(const FString& srcScriptID, const FString& dstScriptID, const int32& wayType)
{
	if (WayPagodaSoulShop.Contains(wayType) && WayPagodaSoulShop[wayType].Contains(srcScriptID))
	{
		WayPagodaSoulShop[wayType].Remove(srcScriptID);
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PAGODA_SOUL_SHOP_DATA);
		if (ConfigTable)
		{
			TArray<FPAGODA_SOUL_SHOP_TYPE_DATA*> AllRows;
			ConfigTable->GetAllRows(AllRows);
			for (auto Row : AllRows)
			{
				if (Row->scriptID == dstScriptID && Row->level == 1 && Row->type == wayType)
				{
					FPAGODA_SOUL_SHOP_TYPE_DATA temp;
					temp.scriptID = Row->scriptID;
					temp.camp = Row->camp;
					temp.type = Row->type;
					temp.lavaPagoda = Row->lavaPagoda;
					temp.lavaPrice = Row->lavaPrice;
					temp.lavaTip = Row->lavaTip;
					temp.icePagoda = Row->icePagoda;
					temp.icePrice = Row->icePrice;
					temp.iceTip = Row->iceTip;
					temp.trapPagoda = Row->trapPagoda;
					temp.trapPrice = Row->trapPrice;
					temp.trapTip = Row->trapTip;
					temp.spiritPagoda = Row->spiritPagoda;
					temp.spiritPrice = Row->spiritPrice;
					temp.spiritTip = Row->spiritTip;
					temp.bSruvival = true;
					WayPagodaSoulShop[wayType].Add(dstScriptID, temp);
					break;
				}
				else if (Row->type == wayType && (Row->lavaPagoda == dstScriptID || Row->spiritPagoda == dstScriptID ||
					Row->icePagoda == dstScriptID || Row->trapPagoda == dstScriptID))
				{
					AnalysisNextPagodaSoul(AllRows, Row->scriptID, dstScriptID, Row->level + 1, wayType);
				}

			}
		}
	}
}
#pragma endregion

void URoleBuyNPCShopInterface::CLIENT_OnInitBuyBackItemList(const FVariant& Var)
{
	BUY_BACK_ITEM_DATAS datas = BUY_BACK_ITEM_DATAS(Var);
	TArray<FBuyBackItemData> buyBackItemDatas;
	for (auto data : datas.buyBackItemDataList)
	{
		FBuyBackItemData  buyBackItemData;
		buyBackItemData.Id = data.id;
		buyBackItemData.Uid = data.uid;
		buyBackItemData.Amount = data.amount;
		buyBackItemData.BindType = data.bindType;
		buyBackItemData.CombatPower = data.combatPower;
		buyBackItemData.AttachPropertiesStr = data.attachPropertiesStr;
		buyBackItemData.AttackPropertiesStr = data.attackPropertiesStr;
		buyBackItemData.IntensifyDataStr = data.intensifyDataStr;
		buyBackItemData.Hardiness = data.hardiness;

		buyBackItemDatas.Add(buyBackItemData);
	}

	OnInitBuyBackItemList(buyBackItemDatas);

}

void URoleBuyNPCShopInterface::OnInitBuyBackItemList_Implementation(const TArray<FBuyBackItemData>& buyBackItemDatas)
{
	StructBackItem(buyBackItemDatas);
}

void URoleBuyNPCShopInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnInitBuyBackItemList");
	ArrBlueFunc.Add("CLIENT_OnRequestSellItem");
	ArrBlueFunc.Add("CLIENT_OnRequestBuyBackItem");
	ArrBlueFunc.Add("addHighBuyBackItem");
	ArrBlueFunc.Add("subHighBuyBackItem");
	ArrBlueFunc.Add("CLIENT_OnSuccessBuyShopItem");	

	ArrBlueFunc.Add("CLIENT_OnRequestBuyCombatSoulItem");
	ArrBlueFunc.Add("CLIENT_OnRequestSellCombatSoulItem");
	ArrBlueFunc.Add("CLIENT_OnRequestBuyGuardSoul");
	ArrBlueFunc.Add("CLIENT_OnRequestUpdatePagodaSoul");
	ArrBlueFunc.Add("CLIENT_openLMNeuralShop");
	ArrBlueFunc.Add("CLIENT_OnBuyNeuralGuard");
	
	ArrBlueFunc.Add("CLIENT_reflashLHMJShopTime");
	ArrBlueFunc.Add("CLIENT_OnSuccessBuyLHMJShopItem");

	Supper::InitBlueCB();
}

void URoleBuyNPCShopInterface::onLeaveWorld()
{
	NPCShopDatas.Empty();
	TongShopExtDatas.Empty();
	ShopServerTime.Empty();
	CombatSoulShop.Empty();
	GuardSoulShop.Empty();
	GuardLevelMapping.Empty();
	GuardBTimeMapping.Empty();
	WayPagodaSoulShop.Empty();
	Supper::onLeaveWorld();
}

void URoleBuyNPCShopInterface::InitShopDatas(const FString& ShopID)
{
	if (!NPCShopDatas.Contains(ShopID))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC_SHOP_DATA);
		if (ConfigTable)
		{
			TArray<FNPCShopData*> NPCShops;
			TMap<FString, FNPCShopData>  ShopMapping;
			ConfigTable->GetAllRows(NPCShops);
			for (auto shop : NPCShops)
			{
				if (shop->shopID == ShopID)
				{
					FNPCShopData data;
					data.shopID = shop->shopID;
					data.Id = shop->Id;
					data.ItemID = shop->ItemID;
					data.Amount = shop->BuyLimit;
					data.Price = shop->Price;
					data.RefreshType = shop->RefreshType;
					data.Condition = shop->Condition;
					data.BuyLimit = shop->BuyLimit;
					data.IsShared = shop->IsShared;
					data.Paging = shop->Paging;
					data.PageIndex = shop->PageIndex;
					ShopMapping.Add(shop->Id, data);
				}
			}
			NPCShopDatas.Add(ShopID, ShopMapping);
		}
	}
	if (ShopID == TONG_SHOPID)
	{
		InitTongPlunderShopData();
	}
}

void URoleBuyNPCShopInterface::InitRandomShopDatas(const FString & ShopID, const TArray<FNPCSHOP_ITEM>& RandItem)
{
	if (RandItem.Num() == 0)
	{
		return;
	}
	//随机限量商品配置
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable2 = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC_RANDOM_LIMIT_SHOP_DATA);
	if (ConfigTable2)
	{
		TArray<FNPCRandomLimitShopData*> NPCShops;
		ConfigTable2->GetAllRows(NPCShops);
		for (auto& shop : NPCShops)
		{
			if (shop->shopID != ShopID)
				continue;
			
			if (!NPCShopDatas.Contains(ShopID))
			{
				TMap<FString, FNPCShopData>  ShopMapping;
				NPCShopDatas.Add(ShopID, ShopMapping);
			}

			for (auto& item : RandItem)
			{
				if (item.id1 == shop->Id)
				{
					FNPCShopData data;
					data.shopID = shop->shopID;
					data.Id = shop->Id;
					data.ItemID = shop->ItemID;
					data.Amount = shop->BuyLimit;
					data.Price = shop->Price;
					data.RefreshType = shop->RefreshType;
					data.Condition = shop->Condition;
					data.BuyLimit = shop->BuyLimit;
					data.IsShared = shop->IsShared;
					data.Paging = shop->Paging;
					data.PageIndex = shop->PageIndex;
					NPCShopDatas[shopID].Add(shop->Id, data);
				}
			}	
		}
	}
}

void URoleBuyNPCShopInterface::StructBackItem(TArray<FBuyBackItemData> Datas)
{
	BuyBackDatas.Empty();
	for (auto Data : Datas)
	{
		UItemBase* ItemBase = UItemFactory::GetItemByID(Data.Id);
		if (IsValid(ItemBase))
		{
			ItemBase->InitData(Data.Uid, Data.Amount, Data.BindType, -1);
			ItemBase->SetDynamicProperty(Data.CombatPower, Data.AttackPropertiesStr, Data.AttachPropertiesStr, Data.IntensifyDataStr, Data.Hardiness);
			BuyBackDatas.Add(ItemBase);
		}
	}
}

UItemBase* URoleBuyNPCShopInterface::GetItemByString(FBuyBackItemData Data)
{
	UItemBase* ItemBase = UItemFactory::GetItemByID(Data.Id);
	if (IsValid(ItemBase))
	{
		ItemBase->InitData(Data.Uid, Data.Amount, Data.BindType, 0);
		ItemBase->SetDynamicProperty(Data.CombatPower, Data.AttackPropertiesStr, Data.AttachPropertiesStr, Data.IntensifyDataStr, Data.Hardiness);
	}
	return ItemBase;
}

#pragma region	/** 英雄王座商店 */
void URoleBuyNPCShopInterface::AnalysisCombatSoul()
{
	CombatSoulShop.Empty();
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COMBAT_SOUL_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FCOMBAT_SOUL_SHOP_TYPE_DATA*> CombatShops;
		ConfigTable->GetAllRows(CombatShops);
		TArray<int32> initItemIDs;		///所有一级 的战魂
		for (FCOMBAT_SOUL_SHOP_TYPE_DATA* combatItem : CombatShops)
		{
			if (combatItem->PreItemID == 0)
			{
				initItemIDs.Add(combatItem->ItemID);
			}
		}
		/// 玩家身上的物品替换
		URoleKitBagInterface* kitBagInter = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
		if (kitBagInter)
		{
			TArray<UItemBase*> ComItem = kitBagInter->GetItemsByKBType(EKITBAGTYPE::SPACE_COPY_BAG);

			for (UItemBase* item : ComItem) 
			{
				int32 id = GetInitialCombatItemID(INT_TO_FSTRING(item->ItemID));

				int32 index = initItemIDs.Find(id);
				if (index != INDEX_NONE)
				{
					initItemIDs.Remove(id);
					FCOMBAT_SOUL_SHOP_TYPE_DATA nextItem = GetNextCombatItem(INT_TO_FSTRING(item->ItemID));
					if (nextItem.ItemID)
					{
						initItemIDs.Add(nextItem.ItemID);
					}
					else
					{
						initItemIDs.Add(item->ItemID);
					}
					
				}
			}
			for (auto id : initItemIDs)
			{
				for (FCOMBAT_SOUL_SHOP_TYPE_DATA* combatItem : CombatShops)
				{
					if (combatItem->ItemID == id)
					{
						FCOMBAT_SOUL_SHOP_TYPE_DATA temp;
						temp.ItemID = combatItem->ItemID;
						temp.Type = combatItem->Type;
						temp.PreItemID = combatItem->PreItemID;
						temp.NextItemID = combatItem->NextItemID;
						temp.BuyPrice = combatItem->BuyPrice;
						temp.SellPrice = combatItem->SellPrice;
						temp.Tip = combatItem->Tip;
						CombatSoulShop.Add(id, temp);
					}
				}
			}
			CombatSoulShop.KeySort(TLess<int32>());
		}
		
	}
}

void URoleBuyNPCShopInterface::AnalysisGuardSoul(const TArray<FGUARD_SOUL_DATA>& GUARD_SOUL_DATAS_1)
{
	GuardSoulShop.Empty();
	GuardLevelMapping.Empty();
	GuardBTimeMapping.Empty();


	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_GUARD_SOUL_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FGUARD_SOUL_SHOP_TYPE_DATA*> guardList;
		ConfigTable->GetAllRows(guardList);
		for (auto guard : GUARD_SOUL_DATAS_1)
		{
			for(auto GD : guardList)
			{
				if (guard.scriptID1.Equals(GD->scriptID))
				{
					FGUARD_SOUL_SHOP_TYPE_DATA temp;
					temp.scriptID = GD->scriptID;
					temp.camp = GD->camp;
					temp.type = GD->type;
					temp.guardName = GD->guardName;
					temp.maxBuyTime = GD->maxBuyTime;
					temp.carPath = GD->carPath;
					temp.buyPrice = GD->buyPrice;
					temp.levelRelevant = GD->levelRelevant;
					temp.tip_1 = GD->tip_1;
					temp.tip_2 = GD->tip_2;
					GuardSoulShop.Add(guard.scriptID1, temp);
					GuardLevelMapping.Add(guard.scriptID1, guard.level2);
					GuardBTimeMapping.Add(guard.scriptID1, guard.buyTime3);
				}
				
			}	
		}
		GuardSoulShop.KeySort(TLess<FString>());
	}
}

void URoleBuyNPCShopInterface::AnalysisPagodaSoul(const TArray<FPAGODA_SOUL_DATA>& PAGODA_SOUL_DATA_1)
{
	WayPagodaSoulShop.Empty();

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PAGODA_SOUL_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FPAGODA_SOUL_SHOP_TYPE_DATA*> AllRows;
		ConfigTable->GetAllRows(AllRows);
		for (FPAGODA_SOUL_DATA soulData: PAGODA_SOUL_DATA_1)
		{
			for (auto Row:AllRows)
			{
				if (Row->type == soulData.wayType3)
				{
					for (FString scriptID: soulData.allPagoda1)
					{
						if (Row->scriptID == scriptID && Row->level == 1)
						{
							TMap<FString, FPAGODA_SOUL_SHOP_TYPE_DATA> PagodaSoulShop1;
							FPAGODA_SOUL_SHOP_TYPE_DATA temp;
							temp.scriptID = Row->scriptID;
							temp.camp = Row->camp;
							temp.type = Row->type;
							temp.lavaPagoda = Row->lavaPagoda;
							temp.lavaPrice = Row->lavaPrice;
							temp.lavaTip = Row->lavaTip;
							temp.icePagoda = Row->icePagoda;
							temp.icePrice = Row->icePrice;
							temp.iceTip = Row->iceTip;
							temp.trapPagoda = Row->trapPagoda;
							temp.trapPrice = Row->trapPrice;
							temp.trapTip = Row->trapTip;
							temp.spiritPagoda = Row->spiritPagoda;
							temp.spiritPrice = Row->spiritPrice;
							temp.spiritTip = Row->spiritTip;
							temp.bSruvival = IsSurvivalPagoda(scriptID, AllRows, soulData.deadPagoda2,soulData.wayType3);
							PagodaSoulShop1.Add(scriptID, temp);
							WayPagodaSoulShop.Add(Row->type, PagodaSoulShop1);
							break;
						}
						else if (Row->lavaPagoda == scriptID || Row->spiritPagoda == scriptID ||
							Row->icePagoda == scriptID || Row->trapPagoda == scriptID)
						{
							AnalysisNextPagodaSoul(AllRows, Row->scriptID, scriptID, Row->level + 1, soulData.wayType3);
							if (WayPagodaSoulShop.Contains(soulData.wayType3) && WayPagodaSoulShop[soulData.wayType3].Contains(scriptID))
							{
								WayPagodaSoulShop[soulData.wayType3][scriptID].bSruvival = IsSurvivalPagoda(scriptID, AllRows, soulData.deadPagoda2, soulData.wayType3);
							}
						}
					}
				}
			}
		}
	}
}


void URoleBuyNPCShopInterface::AnalysisNextPagodaSoul(const TArray<FPAGODA_SOUL_SHOP_TYPE_DATA*>& Rows, const FString SrcSriiptID, const FString& ScriptID, const int32& level, const int32& wayType)
{
	for (auto Row : Rows)
	{
		if (Row->scriptID == SrcSriiptID && Row->level == level && Row->type == wayType)
		{
			TMap<FString, FPAGODA_SOUL_SHOP_TYPE_DATA> PagodaSoulShop1;
			FPAGODA_SOUL_SHOP_TYPE_DATA temp;
			temp.scriptID = Row->scriptID;
			temp.camp = Row->camp;
			temp.type = Row->type;
			temp.lavaPagoda = Row->lavaPagoda;
			temp.lavaPrice = Row->lavaPrice;
			temp.lavaTip = Row->lavaTip;
			temp.icePagoda = Row->icePagoda;
			temp.icePrice = Row->icePrice;
			temp.iceTip = Row->iceTip;
			temp.trapPagoda = Row->trapPagoda;
			temp.trapPrice = Row->trapPrice;
			temp.trapTip = Row->trapTip;
			temp.spiritPagoda = Row->spiritPagoda;
			temp.spiritPrice = Row->spiritPrice;
			temp.spiritTip = Row->spiritTip;
			temp.bSruvival = true;
			PagodaSoulShop1.Add(ScriptID, temp);
			if (WayPagodaSoulShop.Contains(wayType))
			{
				WayPagodaSoulShop[wayType] = PagodaSoulShop1;
			}
			else
			{
				WayPagodaSoulShop.Add(wayType, PagodaSoulShop1);
			}
			return;
		}
	}

	FPAGODA_SOUL_SHOP_TYPE_DATA emptyData;
	TMap<FString, FPAGODA_SOUL_SHOP_TYPE_DATA> tempPagodaSoulShop1;
	tempPagodaSoulShop1.Add(ScriptID, emptyData);
	if (WayPagodaSoulShop.Contains(wayType))
	{
		WayPagodaSoulShop[wayType] = tempPagodaSoulShop1;
	}
	else
	{
		WayPagodaSoulShop.Add(wayType, tempPagodaSoulShop1);
	}
}

void URoleBuyNPCShopInterface::AnalysisNeuralGuard(const TArray<FString>& ScriptIDs)
{
	NeuralShop.Empty();

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NEURAL_GUARD_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FGUARD_SOUL_SHOP_TYPE_DATA*> guardList;
		ConfigTable->GetAllRows(guardList);
		for (auto scriptID : ScriptIDs)
		{
			for (auto GD : guardList)
			{
				if (scriptID.Equals(GD->scriptID))
				{
					FGUARD_SOUL_SHOP_TYPE_DATA temp;
					temp.scriptID = GD->scriptID;
					temp.camp = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("camp"));
					temp.type = GD->type;
					temp.guardName = GD->guardName;
					temp.maxBuyTime = GD->maxBuyTime;
					temp.carPath = GD->carPath;
					temp.buyPrice = GD->buyPrice;
					temp.levelRelevant = GD->levelRelevant;
					temp.tip_1 = GD->tip_1;
					temp.tip_2 = GD->tip_2;
					NeuralShop.Add(scriptID, temp);
				}
			}
		}
		NeuralShop.KeySort(TLess<FString>());
	}
}

int32 URoleBuyNPCShopInterface::GetPagodaTypeByScriptID(const FString& SrciptID, const int32& wayType)
{
	if (WayPagodaSoulShop.Contains(wayType))
	{
		for (auto It = WayPagodaSoulShop[wayType].CreateConstIterator(); It; ++It)
		{
			if (SrciptID.Equals(It.Value().lavaPagoda))
			{
				return 1;
			}
			else if (SrciptID.Equals(It.Value().icePagoda))
			{
				return 2;
			}
			else if (SrciptID.Equals(It.Value().trapPagoda))
			{
				return 3;
			}
		}
	}
	return 0;
}

bool URoleBuyNPCShopInterface::IsSurvivalPagoda(const FString& pagodaScriptID, const TArray<FPAGODA_SOUL_SHOP_TYPE_DATA*>& Raws, const TArray<FString>& DeadPagodas, const int32& wayType)
{
	int32 num(0);
	for (FString pagoda : DeadPagodas)
	{
		if (pagoda.Equals(pagodaScriptID))
		{
			num += 1;
			if (num >= 2)
			{
				return false;
			}
			continue;
		}
		for (auto raw : Raws)
		{
			if (pagodaScriptID.Equals(raw->scriptID) || pagodaScriptID.Equals(raw->icePagoda) || 
				pagodaScriptID.Equals(raw->lavaPagoda) || pagodaScriptID.Equals(raw->trapPagoda) || pagodaScriptID.Equals(raw->spiritPagoda))
			{
				if (pagoda.Equals(raw->scriptID) || pagoda.Equals(raw->icePagoda) ||
					pagoda.Equals(raw->lavaPagoda) || pagoda.Equals(raw->trapPagoda) || pagoda.Equals(raw->spiritPagoda))
				{
					num += 1;
					if (num >= 2)
					{
						return false;
					}
					break;
				}
			}
		}
	}

	return true;
}

void URoleBuyNPCShopInterface::RequestBuyDrugItem(const int32& ItemID)
{
	KBEngine::FVariantArray param;
	param.Add(ItemID);
	CellCall(TEXT("CELL_requestBuyDrugSoulItem"), param);
}

void URoleBuyNPCShopInterface::RequestSellDrugItem(const int32& ItemID)
{
	KBEngine::FVariantArray param;
	param.Add(ItemID);
	CellCall(TEXT("CELL_requestSellDrugSoulItem"), param);
}

void URoleBuyNPCShopInterface::RequestBuyNeuralGuard(const FString& ScriptID, const int32& Type)
{
	KBEngine::FVariantArray param;
	param.Add(ScriptID);
	param.Add(Type);
	CellCall(TEXT("CELL_requestBuyNeuralGuard"), param);
}

void URoleBuyNPCShopInterface::CLIENT_openLMNeuralShop_Implementation(const int32& NPCID, const TArray<FString>& ScriptIDs, const TArray<int32>& Times, const int32& Level)
{
	AnalysisNeuralGuard(ScriptIDs);
}

TMap<FString, FPAGODA_SOUL_SHOP_TYPE_DATA> URoleBuyNPCShopInterface::GetPagodaSoulShopByWayTyp(const int32& wayType)
{
	if (WayPagodaSoulShop.Contains(wayType))
	{
		return WayPagodaSoulShop[wayType];
	}
	TMap<FString, FPAGODA_SOUL_SHOP_TYPE_DATA> tempWayPagodaSoulShop;
	return tempWayPagodaSoulShop;
}

void URoleBuyNPCShopInterface::InitTongPlunderShopData()
{
	if (TongPlunderShopDatas.Num() > 0)
	{
		return;
	}
	if (TongPlunderShopItems.Num() > 0)
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_PLUNDER_SHOP_DATA);
		if (ConfigTable)
		{
			TArray<FNPCShopData*> NPCShops;
			ConfigTable->GetAllRows(NPCShops);
			if (TongPlunderShopItems.Num() > 0)
			{
				for (auto shop : NPCShops)
				{
					if (shop->shopID == TONG_PLUNDER_SHOPID)
					{
						if (TongPlunderShopItems.Contains(shop->Id) && TongPlunderShopItems[shop->Id].Contains(shop->ItemID))
						{

							FNPCShopData data;
							data.shopID = shop->shopID;
							data.Id = shop->Id;
							data.ItemID = shop->ItemID;
							data.Amount = TongPlunderShopItems[shop->Id][shop->ItemID]; //只有这一项不一样
							data.Price = shop->Price;
							data.RefreshType = shop->RefreshType;
							data.Condition = shop->Condition;
							data.BuyLimit = shop->BuyLimit;
							data.IsShared = shop->IsShared;
							data.Paging = shop->Paging;
							data.PageIndex = shop->PageIndex;
							TongPlunderShopDatas.Add(shop->Id, data);
							break;
						}
					}
				}
			}
		}
	}
}

TArray<FNPCShopData> URoleBuyNPCShopInterface::GetTongPlunderShopData()
{
	TArray<FNPCShopData> ReturnData;
	for (auto it = TongPlunderShopDatas.CreateIterator(); it; ++it)
	{
		ReturnData.Add(it.Value());
	}
	ReturnData.Sort([](const FNPCShopData& A, const FNPCShopData& B)
	{
		//商品ID排序
		if (FSTRING_TO_FLOAT(A.Id) > FSTRING_TO_FLOAT(B.Id))
		{
			return false;
		}
		return true;
	});
	return ReturnData;
}

void URoleBuyNPCShopInterface::OnUnLockTongShop_Implementation()
{
}

void URoleBuyNPCShopInterface::OnLockTongShop_Implementation()
{
}

void URoleBuyNPCShopInterface::OnTongPlunderShopSellStartBP_Implementation()
{
}

void URoleBuyNPCShopInterface::CLIENT_LockTongShop()
{
	TongShopLock = true;
	OnLockTongShop();
}

void URoleBuyNPCShopInterface::CLIENT_UnLockTongShop()
{
	TongShopLock = false;
	OnUnLockTongShop();
}

void URoleBuyNPCShopInterface::OnTongPlunderShopSellStart(const FVariant& ShopDatas, const FString& EndTime)
{
	TongPlunderShopEndTime = EndTime;
	TongPlunderShopItems.Empty();
	TongPlunderPage = true;

	KBEngine::FVariantArray ShopDatas_Ex = ShopDatas.GetValue<KBEngine::FVariantArray>();
	for (auto Data : ShopDatas_Ex)
	{

		TMap<int32, int32> TempData;
		auto VariantData = Data.GetValue<KBEngine::FVariantMap>();
		TempData.Add(VariantData[TEXT("itemID")].GetValue<int32>(), VariantData[TEXT("amount")].GetValue<int32>());
		TongPlunderShopItems.Add(VariantData[TEXT("id")].GetValue<FString>(), TempData);
	}

	OnTongPlunderShopSellStartBP();
}

void URoleBuyNPCShopInterface::OnTongPlunderShopSellEnd_Implementation()
{
	TongPlunderShopItems.Empty();
	TongPlunderShopEndTime = "";
	TongPlunderPage = false;
}

void URoleBuyNPCShopInterface::CLIENT_TongPlunderShopSellEnd()
{
	OnTongPlunderShopSellEnd();
}

FString URoleBuyNPCShopInterface::GetTongPlunderShopEndTime()
{
	return TongPlunderShopEndTime;
}

void URoleBuyNPCShopInterface::OnTongPlunderShopItemBuySuccess(const FString& Slot, const int& ItemID, const int& Amount)
{
	if (TongPlunderShopItems.Contains(Slot) && TongPlunderShopItems[Slot].Contains(ItemID))
	{
		TongPlunderShopItems[Slot][ItemID] -= Amount;
	}
	if (TongPlunderShopDatas.Contains(Slot))
	{
		TongPlunderShopDatas[Slot].Amount -= Amount;
	}
}

void URoleBuyNPCShopInterface::RequestBuyTongPlunderShopItem(const FString& slot, int itemID, int amount)
{
	KBEngine::FVariantArray Args;
	Args.Add(TONG_PLUNDER_SHOPID);
	Args.Add(slot);
	Args.Add(itemID);
	Args.Add(amount);
	GetEntity()->CellCall(TEXT("requestBuyNPCShopItem"), Args);
}


#pragma endregion

#pragma region	/** 轮回秘境商店 */

void URoleBuyNPCShopInterface::CLIENT_InitLHMJShopData(const int32 & _NPCID, const FString & _ShopID, const FVariant & fixedDict)
{
	npcID = _NPCID;
	shopID = _ShopID;
	ShopType = NPCSHOP_TYPE::LHMJ_FIELD_TYPE;
	_InitShopData(fixedDict);
	OnInitLHMJShop();
}

void URoleBuyNPCShopInterface::RequestReflashLHMJShop()
{
	KBEngine::FVariantArray param;
	CellCall(TEXT("CELL_reflashLHMJShop"), param);
}

void URoleBuyNPCShopInterface::CLIENT_reflashLHMJShopData(const FVariant & fixedDict)
{
	RefreshNum += 1;
	_InitShopData(fixedDict);
	OnUpdateShopItemList();
	OnUpdateRefreshNum();

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("RefreshSuccess"));
	}
}

void URoleBuyNPCShopInterface::CLIENT_reflashLHMJShopTime(const int32 & _reflashNum)
{
	RefreshNum = _reflashNum;
	OnUpdateRefreshNum();
}

int32 URoleBuyNPCShopInterface::GetCurReflashCost()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LHMJ_SKOP_REFLASH_COST_DATA);
	if (ConfigTable)
	{
		TArray<FLHMJShopReflashCostData*> guardList;
		ConfigTable->GetAllRows(guardList);
		for (auto It : guardList)
		{
			if (It->reflashNum == RefreshNum + 1)
			{
				return It->money;
			}
		}
	}
	return 0;
}

int32 URoleBuyNPCShopInterface::GetAutoReflashTime()
{
	FDateTime now_ = FDateTime::Now();
	return 3600 - (now_.GetMinute() * 60 + now_.GetSecond());
}

void URoleBuyNPCShopInterface::RequestAutoReflashLHMJShop()
{
	KBEngine::FVariantArray param;
	BaseCall(TEXT("BASE_autoReflashLHMJShop"), param);
}

void URoleBuyNPCShopInterface::CLIENT_autoReflashLHMJShopData(const FVariant & fixedDict)
{
	_InitShopData(fixedDict);
	OnUpdateShopItemList();
}

void URoleBuyNPCShopInterface::RequestBuyLHMJShopItem(const FString & slot, const int32 & itemID, const int32 & amount)
{
	KBEngine::FVariantArray param;
	param.Add(slot);
	param.Add(itemID);
	param.Add(amount);
	CellCall(TEXT("CELL_requestBuyLHMJShopItem"), param);
}

void URoleBuyNPCShopInterface::CLIENT_OnSuccessBuyLHMJShopItem_Implementation(const FString & slot, const int32 & amount)
{
	if (NPCShopDatas.Contains(shopID) && NPCShopDatas[shopID].Contains(slot))
	{
		if (NPCShopDatas[shopID][slot].Amount >= 0)
		{
			NPCShopDatas[shopID][slot].Amount -= amount;
		}
	}
}

void URoleBuyNPCShopInterface::_InitShopData(const FVariant & fixedDict)
{
	NPCShopDatas.Empty();
	FSHOPMALL_ITEM_LIST shopItems(fixedDict);

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FNPCShopData*> NPCShops;
		ConfigTable->GetAllRows(NPCShops);

		TMap<FString, FNPCShopData>  ShopMapping;
		for (auto item : shopItems.items)
		{
			FNPCShopData data;
			data.Id = item.id;
			data.ItemID = item.itemID;
			data.Amount = item.amount;

			for (auto shop : NPCShops)
			{
				if (shop->Id == data.Id && shop->ItemID == data.ItemID)
				{
					data.shopID = shop->shopID;
					data.Price = shop->Price;
					data.RefreshType = shop->RefreshType;
					data.Condition = shop->Condition;
					data.BuyLimit = shop->BuyLimit;
					data.IsShared = shop->IsShared;
					data.Paging = shop->Paging;
					data.PageIndex = shop->PageIndex;
				}
			}

			ShopMapping.Add(data.Id, data);
		}
		NPCShopDatas.Add(shopID, ShopMapping);
	}
}
#pragma endregion

void URoleBuyNPCShopInterface::RPC_requestRepairOneEquip(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::RPC_requestRepairOneEquip : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("requestRepairOneEquip"), args);
}

void URoleBuyNPCShopInterface::RPC_requestRepairAllEquip(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBuyNPCShopInterface::RPC_requestRepairAllEquip : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("requestRepairAllEquip"), args);
}

void URoleBuyNPCShopInterface::FilterItemsByLevel(const int32& level, const TArray<FNPCShopData> &itemarray, TArray<FNPCShopData>& result)
{
	for (auto Item : itemarray)
	{
		FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(Item.ItemID);
		if (level >= ItemData.Level)
		{
			result.Add(Item);
		}
	}
}

void URoleBuyNPCShopInterface::FilterItemsByProfession(const int32& profession, const TArray<FNPCShopData> &itemarray, TArray<FNPCShopData>& result)
{
	for (auto Item : itemarray)
	{
		FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(Item.ItemID);
		TArray<FString> ReqClasses = UGolbalBPFunctionLibrary::SplitString(ItemData.ReqClasses, false, TEXT("|"));
		if (ReqClasses.Contains(INT_TO_FSTRING(profession)))
		{
			result.Add(Item);
		}
	}
}

void URoleBuyNPCShopInterface::onNotifyRandomItemSellEndTime(const FString& sid, const int32& EndTime)
{
	if (randomItemSellEndTimes.Contains(sid))
		randomItemSellEndTimes.Remove(sid);
	randomItemSellEndTimes.Add(sid, EndTime);
}

int32 URoleBuyNPCShopInterface::getRandomItemShopSellEndTime(const FString& sid)
{
	if (randomItemSellEndTimes.Contains(sid))
		return randomItemSellEndTimes[sid];
	return 0;
}

void URoleBuyNPCShopInterface::removeRandomItemSell(const FString& sid)
{
	if (!NPCShopDatas.Contains(sid))
	{
		return;
	}

	//随机限量商品配置
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC_RANDOM_LIMIT_SHOP_DATA);
	if (ConfigTable)
	{
		TArray<FNPCRandomLimitShopData*> NPCShops;
		ConfigTable->GetAllRows(NPCShops);
		for (auto& shop : NPCShops)
		{
			if (shop->shopID != sid)
				continue;

			for (auto& item : NPCShopDatas[sid])
			{
				if (item.Value.Id == shop->Id)
				{
					NPCShopDatas[sid].Remove(item.Key);
					break;
				}
			}
		}
	}

	CLIENT_InitNPCShopItemList();
}

CONTROL_COMPILE_OPTIMIZE_END