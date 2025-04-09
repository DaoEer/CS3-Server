// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleShopMallInterface.h"
#include "Util/CS3Debug.h"
#include "Entity/Alias.h"
#include "GameData/Item/ItemFactory.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "CS3Base/CS3Entity.h"
#include "Util/ConvertUtil.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleShopMallInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitCouponItem, &URoleShopMallInterface::InitCouponItem, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddCouponItem, &URoleShopMallInterface::AddCouponItem, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddReceiveGoodsDataRecord, &URoleShopMallInterface::AddReceiveGoodsDataRecord, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddGivingGoodsDataRecord, &URoleShopMallInterface::AddGivingGoodsDataRecord, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitGoodsDataRecord, &URoleShopMallInterface::InitGoodsDataRecord, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(DealReceiveGivingGoodsDataCB, &URoleShopMallInterface::DealReceiveGivingGoodsDataCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ChangeGivingGoodsDataCB, &URoleShopMallInterface::ChangeGivingGoodsDataCB, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleShopMallInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleShopMallInterface::URoleShopMallInterface()
{

}

URoleShopMallInterface::~URoleShopMallInterface()
{

}


void URoleShopMallInterface::OnEnterWorld()
{

}

void URoleShopMallInterface::OnLeaveWorld()
{

}

void URoleShopMallInterface::GetShopMallItemList_Implementation(const FString& data)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****getShopMallItemList| %s |*****"), *data);
	FString giftItemListData = "";
	FString xianShiItemListData = "";
	FString lingShiItemListData = "";
	FString xuanShiItemListData = "";
	TSharedRef<TJsonReader<TCHAR>> jsonReader = TJsonReaderFactory<TCHAR>::Create(data);
	TSharedPtr<FJsonObject> jsonParsed;
	bool BFlag = FJsonSerializer::Deserialize(jsonReader, jsonParsed);
	if (BFlag)
	{
		giftItemListData = jsonParsed->GetStringField(FString::FromInt(int(SHOPMALLTYPE::SHOP_TYPE_GIFT)));
		xianShiItemListData = jsonParsed->GetStringField(FString::FromInt(int(SHOPMALLTYPE::SHOP_TYPE_XIANSHI)));
		lingShiItemListData = jsonParsed->GetStringField(FString::FromInt(int(SHOPMALLTYPE::SHOP_TYPE_LINGSHI)));
		xuanShiItemListData = jsonParsed->GetStringField(FString::FromInt(int(SHOPMALLTYPE::SHOP_TYPE_XUANSHI)));
	}

	AliasShopMallItemList::CreateFromString(giftItemListData, GiftItemMap);
	AliasShopMallItemList::CreateFromString(xianShiItemListData, XianShiItemMap);
	AliasShopMallItemList::CreateFromString(lingShiItemListData, LingShiItemMap);
	AliasShopMallItemList::CreateFromString(xuanShiItemListData, XuanShiItemMap);

	GetShopMallItemListCB();
}

void URoleShopMallInterface::GetShopMallItemListCB()
{
	GiftItemList.Empty();
	XianShiItemList.Empty();
	XuanShiItemList.Empty();
	LingShiItemList.Empty();
	if (InitShopMallItem(SHOPMALLTYPE::SHOP_TYPE_GIFT))
	{
		if (InitShopMallItem(SHOPMALLTYPE::SHOP_TYPE_XIANSHI))
		{
			if (InitShopMallItem(SHOPMALLTYPE::SHOP_TYPE_XUANSHI))
			{
				InitShopMallItem(SHOPMALLTYPE::SHOP_TYPE_LINGSHI);
			}
		}
	}
	OnInitShopMallItem();
}

bool URoleShopMallInterface::InitShopMallItem(SHOPMALLTYPE shopMallType)
{
	if (GetItemMapLength(shopMallType) <= 0)
	{
		CS3_Warning(TEXT("This shop mall is not open"));
	}
	TMap<FString, TMap<FString, int32>>* ItemMap = GetShopMallItemMap(shopMallType);
	if (ItemMap == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::InitShopMallItem : ItemMap!"));
		return true;
	}
	for (auto item = ItemMap->CreateIterator(); item;++item)
	{
		FShopMallItem tempItem;
		TArray<int32> data = GetItemMapList(shopMallType, item.Key());
		if (data.Num() >= 2)
		{
			UItemBase* itemBase = UItemFactory::GetItemByID(data[0]);
			if (!IsValid(itemBase))
			{
				CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::InitShopMallItem : itemBase!"));
				return false;
			}
			itemBase->Amount = data[1];
			tempItem.Item = itemBase;
			tempItem.Id = item.Key();
			AddShopMallItem(shopMallType, tempItem);
		}
	}
	return true;
}

void URoleShopMallInterface::AddShopMallItem(SHOPMALLTYPE shopMallType, FShopMallItem mallItem)
{
	switch (shopMallType)
	{
	case SHOPMALLTYPE::SHOP_TYPE_GIFT:
		GiftItemList.Add(mallItem);
		break;
	case SHOPMALLTYPE::SHOP_TYPE_XIANSHI:
		XianShiItemList.Add(mallItem);
		break;
	case SHOPMALLTYPE::SHOP_TYPE_XUANSHI:
		XuanShiItemList.Add(mallItem);
		break;
	case SHOPMALLTYPE::SHOP_TYPE_LINGSHI:
		LingShiItemList.Add(mallItem);
	default:
		break;
	}
}

int32 URoleShopMallInterface::GetItemMapLength(SHOPMALLTYPE shopMallTypeID)
{
	TMap<FString, TMap<FString, int32>>* ItemMap = GetShopMallItemMap(shopMallTypeID);
	if (ItemMap == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::GetItemMapLength : ItemMap!"));
		return 0;
	}
	return ItemMap->Num();
}

TArray<int32> URoleShopMallInterface::GetItemMapList(SHOPMALLTYPE shopMallTypeID,const FString& slot)
{
	TArray<int32> list;
	TMap<FString, TMap<FString, int32>>* ItemMap = GetShopMallItemMap(shopMallTypeID);
	if (ItemMap == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::GetItemMapList : ItemMap!"));
		return list;
	}
	TMap<FString, int32> *dict = ItemMap->Find(slot);
	if (dict != nullptr)
	{
		list.Add(*dict->Find("itemID"));
		list.Add(*dict->Find("amount"));
	}
	return list;
}

TMap<FString, TMap<FString, int32>>* URoleShopMallInterface::GetShopMallItemMap(SHOPMALLTYPE shopMallTypeID)
{
	switch (shopMallTypeID)
	{
	case SHOPMALLTYPE::SHOP_TYPE_GIFT :
		return &GiftItemMap;
		break;
	case SHOPMALLTYPE::SHOP_TYPE_XIANSHI :
		return &XianShiItemMap;
		break;
	case SHOPMALLTYPE::SHOP_TYPE_LINGSHI :
		return &LingShiItemMap;
		break;
	case SHOPMALLTYPE::SHOP_TYPE_XUANSHI :
		return &XuanShiItemMap;
		break;
	default:
		return nullptr;
	}
}

void URoleShopMallInterface::RequestBuyShopMallItem(const FString& couponUID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****requestBuyShopMallItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error: URoleShopMallInterface::RequestBuyShopMallItem : player()!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error: URoleShopMallInterface::RequestBuyShopMallItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	BuyShopMallItems buyItems;
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray d;
	for (auto item:BuyShopMallItemData)
	{
		buyItems.buyShopMallItemList.Add(item);
	}
	buyItems.ToFVariantMap(d);
	args.Add(d);
	args.Add(couponUID);
	args.Add((uint64)0);
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::RequestBuyShopMallItem : GetEntity()!"));
		return;
	}
	this->GetEntity()->BaseCall(TEXT("requestBuyShopMallItem"), args);
	BuyShopMallItemData.Empty();
}

void URoleShopMallInterface::RequestGiveShopMallItemToRole(int32 targetDBID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****requestGiveShopMallItemToRole*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::RequestGiveShopMallItemToRole : GetEntity()!"));
		return;
	}
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error: URoleShopMallInterface::RequestGiveShopMallItemToRole : player()!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error: URoleShopMallInterface::RequestGiveShopMallItemToRole :pEntity_Player->IsPlayerRole()!"));
		return;
	}
	BuyShopMallItems giveItems;
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray d;
	for (auto item : BuyShopMallItemData)
	{
		giveItems.buyShopMallItemList.Add(item);
	}
	giveItems.ToFVariantMap(d);
	args.Add(d);
	args.Add((uint64)targetDBID);
	this->GetEntity()->BaseCall(TEXT("GivingShopMallItemToPlayer"), args);
	BuyShopMallItemData.Empty();
}

void URoleShopMallInterface::RequestDealReceiveGoodsData(TArray<FString> goodsDataUIDs, int32 dealWay)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****RequestDealReceiveGoodsData*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error: URoleShopMallInterface::RequestDealReceiveGoodsData : player()!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error: URoleShopMallInterface::RequestDealReceiveGoodsData : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray arg;
	arg.Add(UGolbalBPFunctionLibrary::ListToFVariant(goodsDataUIDs));
	arg.Add(dealWay);
	if (GetEntity())
	{
		GetEntity()->BaseCall(TEXT("dealReceiveGivingGoodsData"), arg);
	}
}

void URoleShopMallInterface::AddGivingGoodsDataRecord(const FVariant& goodsData)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****addGivingGoodsDataRecord | %s |*****"), *goodsData);
	FGiftGoodsData goodsItem = GetGiftDataFromVariantData(goodsData);
	GivingGoodsData.Add(goodsItem);
	AddGivingGoodsDataRecordCB(goodsItem);
}

void URoleShopMallInterface::AddReceiveGoodsDataRecord(const FVariant& goodsData)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****addReceiveGoodsDataRecord | %s |*****"), *goodsData);
	FGiftGoodsData goodsItem = GetGiftDataFromVariantData(goodsData);
	ReceiveGoodsData.Add(goodsItem);
	AddReceiveGoodsDataRecordCB(goodsItem);
}

void URoleShopMallInterface::InitGoodsDataRecord(const FVariant& variant)
{
	TArray<TSharedPtr<FJsonValue>> givingGoodsData;
	TArray<TSharedPtr<FJsonValue>> receiveGoodsData;
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_givingGoods = variantMap[TEXT("givingGoodsData")].GetValue<KBEngine::FVariantArray>();
	KBEngine::FVariantArray variantArray_reveiveGoodsData = variantMap[TEXT("reveiveGoodsData")].GetValue<KBEngine::FVariantArray>();
	InitGivingGoodsDataRecord(variantArray_givingGoods);
	InitReceiveGoodsDataRecord(variantArray_reveiveGoodsData);
}

void URoleShopMallInterface::InitGivingGoodsDataRecord(const  KBEngine::FVariantArray& goodsData)
{
	GivingGoodsData.Empty();
	
	for (auto data:goodsData )
	{
		GivingGoodsData.Add(GetGiftDataFromVariantData(data));
	}
	InitGivingGoodsDataRecordCB();
}

void URoleShopMallInterface::InitReceiveGoodsDataRecord(const KBEngine::FVariantArray& goodsData)
{
	ReceiveGoodsData.Empty();
	for (auto data:goodsData)
	{
		ReceiveGoodsData.Add(GetGiftDataFromVariantData(data));
	}
	InitReceiveGoodsDataRecordCB();
}

FGiftGoodsData URoleShopMallInterface::GetGiftDataFromVariantData(const FVariant& data)
{
	FGiftGoodsData goodsData;
	FGIFT_GOODS_DATA tempData = FGIFT_GOODS_DATA(data);
	goodsData.GoodsDataUID = tempData.uid;
	goodsData.ItemID = tempData.itemID;
	goodsData.Amount = tempData.amount;
	goodsData.ItemName = tempData.itemName;
	goodsData.PlayerName = tempData.playerName;
	switch (tempData.state )
	{
	case 0:
		goodsData.State = GIFTSTATE::GIFT_STATE_WAIT;
		break;
	case 1:
		goodsData.State = GIFTSTATE::GIFT_STATE_OVERRDUE;
		break;
	case 2:
		goodsData.State = GIFTSTATE::GIFT_STATE_RECEIVE;
		break;
	case 3:
		goodsData.State = GIFTSTATE::GIFT_STATE_WITHDRAW;
		break;
	case 4:
		goodsData.State = GIFTSTATE::GIFT_STATE_REFUSE;
		break;
	default:
		break;
	}
	goodsData.Time = FSTRING_TO_INT64(tempData.time);
	
	return goodsData;
}

FGiftGoodsData URoleShopMallInterface::GetGiftDataFromJsonData(const FString& data)
{
	FGiftGoodsData goodsData;
	TSharedRef<TJsonReader<TCHAR>> jsonReader = TJsonReaderFactory<TCHAR>::Create(data);
	TSharedPtr<FJsonObject> jsonParsed;
	bool BFlag = FJsonSerializer::Deserialize(jsonReader, jsonParsed);
	if (BFlag)
	{
		goodsData.GoodsDataUID = jsonParsed->GetStringField("uid");
		goodsData.ItemID = jsonParsed->GetIntegerField("itemID");
		goodsData.Amount = jsonParsed->GetIntegerField("amount");
		goodsData.ItemName = jsonParsed->GetStringField("itemName");
		goodsData.PlayerName = jsonParsed->GetStringField("playerName");
		switch (jsonParsed->GetIntegerField("state"))
		{
		case 0:
			goodsData.State = GIFTSTATE::GIFT_STATE_WAIT;
			break;
		case 1:
			goodsData.State = GIFTSTATE::GIFT_STATE_OVERRDUE;
			break;
		case 2:
			goodsData.State = GIFTSTATE::GIFT_STATE_RECEIVE;
			break;
		case 3:
			goodsData.State = GIFTSTATE::GIFT_STATE_WITHDRAW;
			break;
		case 4:
			goodsData.State = GIFTSTATE::GIFT_STATE_REFUSE;
			break;
		default:
			break;
		}
		goodsData.Time = FSTRING_TO_INT64(jsonParsed->GetStringField("time"));
	}
	return goodsData;
}

void URoleShopMallInterface::DealReceiveGivingGoodsDataCB(const FVariant& data)
{
	RECALL_GIFT_DATAS tempData = RECALL_GIFT_DATAS( data );
	for (auto dData : tempData.dealGivingGoodsData)
	{
		FString uid =  dData.uid;
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****DealReceiveGivingGoodsDataCB | %s |*****"), *uid)
		FGiftGoodsData giftGoodsData = GetGiftGoodsData(uid, ReceiveGoodsData);
		if (giftGoodsData.GoodsDataUID.Len() == 0)
		{
			return;
		}
		giftGoodsData.State = GIFTSTATE(dData.state );
		giftGoodsData.Time = FSTRING_TO_INT64( dData.changeTime );
		OnDealReceiveGivingGoodsData(uid);
		
	}
	
}

void URoleShopMallInterface::ChangeGivingGoodsDataCB(const FVariant& goodsData)
{
	RECALL_GIFT_DATA tempData = RECALL_GIFT_DATA();

	FString uid = tempData.uid;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****changeGivingGoodsDataCB | %s |*****"), *uid);
	FGiftGoodsData giftGoodsData = GetGiftGoodsData(uid, GivingGoodsData);
	if (giftGoodsData.GoodsDataUID.Len() == 0)
	{
		return;
	}
	giftGoodsData.State = GIFTSTATE(tempData.state);
	giftGoodsData.Time = FSTRING_TO_INT64(tempData.changeTime);
	OnChangeGivingGoodsData(uid);
	
}

void URoleShopMallInterface::ClearGivingGoodsDataRecordCB_Implementation(const TArray<FString>& goodsDataUIDs)
{
	TArray<FGiftGoodsData*> giftGoodsDataArray;
	for (auto uid : goodsDataUIDs)
	{
		FGiftGoodsData giftGoodsData = GetGiftGoodsData(uid, GivingGoodsData);
		if (giftGoodsData.GoodsDataUID.Len() == 0)
		{
			continue;
		}
		giftGoodsDataArray.Add(&giftGoodsData);
		OnClearGivingGoodsDataRecord(uid);
	}
	for (auto goodsData : giftGoodsDataArray)
	{
		GivingGoodsData.Remove(*goodsData);
	}
}

void URoleShopMallInterface::ClearReceiveGoodsDataRecordCB_Implementation(const TArray<FString>& goodsDataUIDs)
{
	TArray<FGiftGoodsData*> giftGoodsDataArray;
	for (auto uid : goodsDataUIDs)
	{
		FGiftGoodsData giftGoodsData = GetGiftGoodsData(uid, ReceiveGoodsData);
		if (giftGoodsData.GoodsDataUID.Len() == 0)
		{
			continue;
		}
		giftGoodsDataArray.Add(&giftGoodsData);
		OnClearReceiveGoodsDataRecord(uid);
	}
	for (auto goodsData : giftGoodsDataArray)

	{
		ReceiveGoodsData.Remove(*goodsData);
	}
	
}

FGiftGoodsData URoleShopMallInterface::GetGiftGoodsData(const FString& goodsDataUid, const TArray<FGiftGoodsData>& giftGoodsDataArray)
{	
	for (auto& goodsData : giftGoodsDataArray)
	{
		if (goodsData.GoodsDataUID == goodsDataUid)
		{
			return goodsData;
		}
	}
	FGiftGoodsData giftGoodsData;
	giftGoodsData.GoodsDataUID = "";
	return giftGoodsData;
}

FGiftGoodsData URoleShopMallInterface::GetReceiveGiftGoodsDataByUID(FString goodsDataUid)
{
	return GetGiftGoodsData(goodsDataUid, ReceiveGoodsData);
}

FGiftGoodsData URoleShopMallInterface::GetGivingGiftGoodsDataByUID(FString goodsDataUid)
{
	return GetGiftGoodsData(goodsDataUid, GivingGoodsData);
}

FShopMallItem URoleShopMallInterface::GetShopMallItemByID(FString id)
{
	FShopMallItem tempMallItem;
	tempMallItem.Id = "";
	tempMallItem = GetShopMallItemByIDAndMallType(SHOPMALLTYPE::SHOP_TYPE_GIFT, id);
	if (tempMallItem.Id != "")
	{
		return tempMallItem;
	}
	tempMallItem = GetShopMallItemByIDAndMallType(SHOPMALLTYPE::SHOP_TYPE_LINGSHI, id);
	if (tempMallItem.Id != "")
	{
		return tempMallItem;
	}
	tempMallItem = GetShopMallItemByIDAndMallType(SHOPMALLTYPE::SHOP_TYPE_XIANSHI, id);
	if (tempMallItem.Id != "")
	{
		return tempMallItem;
	}
	tempMallItem = GetShopMallItemByIDAndMallType(SHOPMALLTYPE::SHOP_TYPE_XUANSHI, id);
	return tempMallItem;
}

FShopMallItem URoleShopMallInterface::GetShopMallItemByIDAndMallType(SHOPMALLTYPE shopMallTypeID, FString id)
{
	FShopMallItem tempMallItem;
	tempMallItem.Id = "";
	switch (shopMallTypeID)
	{
	case SHOPMALLTYPE::SHOP_TYPE_GIFT:
		tempMallItem = GetShopMallItemByIDAndItemList(GiftItemList, id);
		break;
	case SHOPMALLTYPE::SHOP_TYPE_LINGSHI:
		tempMallItem = GetShopMallItemByIDAndItemList(LingShiItemList, id);
		break;
	case SHOPMALLTYPE::SHOP_TYPE_XIANSHI:
		tempMallItem = GetShopMallItemByIDAndItemList(XianShiItemList, id);
		break;
	case  SHOPMALLTYPE::SHOP_TYPE_XUANSHI:
		tempMallItem = GetShopMallItemByIDAndItemList(XuanShiItemList, id);
		break;
	default:
		break;
	}
	return tempMallItem;
}

FShopMallItem URoleShopMallInterface::GetShopMallItemByIDAndItemList(TArray<FShopMallItem> mallItemList, FString id)
{
	FShopMallItem tempMallItem;
	tempMallItem.Id = "";
	for (auto item : mallItemList)
	{
		if (item.Id == id)
		{
			tempMallItem = item;
		}
	}
	return tempMallItem;
}

void URoleShopMallInterface::InitCouponItem(const FVariant& data)
{
	FCOUPON_ITEM_LIST couponItemList = FCOUPON_ITEM_LIST(data);
	for (auto bbData : couponItemList.couponItems)
	{
		FCouponItemData couponItemData;
		couponItemData.CouponId = bbData.couponId;
		char uidChar[21];
		sprintf_s(uidChar, "%llu", bbData.uid);
		couponItemData.CouponUid = uidChar;

		CouponItemList.Add(couponItemData);
	}
	OnInitCouponItemCB();
}

//void URoleShopMallInterface::OnInitCouponItem(const TArray<FString>& data)
//{
//	for (auto sdata : data)
//	{
//		CouponItemList.Add(GetCouponItemByData(sdata));
//	}
//	OnInitCouponItemCB();
//}

FCouponItemData URoleShopMallInterface::GetCouponItemByData(const FVariant& data)
{
	double x = 1;
	FString y;
	FCOUPON_ITEM tempData = FCOUPON_ITEM(data);
	FCouponItemData couponItemData;
	couponItemData.CouponId = tempData.couponId;
	char uidChar[21];
	sprintf_s(uidChar, "%llu", tempData.uid);
	couponItemData.CouponUid = uidChar;
	return couponItemData;
}

void URoleShopMallInterface::AddCouponItem(const FVariant& data)
{
	FCouponItemData couponItemData = GetCouponItemByData(data);
	CouponItemList.Add(couponItemData);
	AddCouponItemCB(couponItemData);
}

void URoleShopMallInterface::RemoveCouponItem_Implementation(const FString& couponUid)
{
	FCouponItemData couponItemData;
	for (auto couponItem : CouponItemList)
	{
		if (couponItem.CouponUid == couponUid)
		{
			couponItemData = couponItem;
			break;
		}
	}
	CouponItemList.Remove(couponItemData);
	RemoveCouponItemCB(couponUid);
}

void URoleShopMallInterface::RPC_requestShopMallItemList()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::RPC_requestShopMallItemList : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->BaseCall(TEXT("requestShopMallItemList"), args);
}

void URoleShopMallInterface::RPC_withDrawGiveGoodsData(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::RPC_withDrawGiveGoodsData : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->BaseCall(TEXT("withDrawGiveGoodsData"), args);
}

void URoleShopMallInterface::RPC_clearGivingGoodsDataRecord(const TArray<FString>& ARRAY_STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::RPC_clearGivingGoodsDataRecord : entity!"));
		return;
	}
	KBEngine::FVariantArray ARRAY_STRING_1_ = KBEngine::FVariantArray();
	for (auto& elementVariant0 : ARRAY_STRING_1)
	{
		FVariant element1 = FVariant(elementVariant0);
		ARRAY_STRING_1_.Add(element1);
	}

	KBEngine::FVariantArray args;
	args.Add(ARRAY_STRING_1_);

	entity->BaseCall(TEXT("clearGivingGoodsDataRecord"), args);
}

void URoleShopMallInterface::RPC_clearReceiveGoodsDataRecord(const TArray<FString>& ARRAY_STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::RPC_clearReceiveGoodsDataRecord : entity!"));
		return;
	}
	KBEngine::FVariantArray ARRAY_STRING_1_ = KBEngine::FVariantArray();
	for (auto& elementVariant0 : ARRAY_STRING_1)
	{
		FVariant element1 = FVariant(elementVariant0);
		ARRAY_STRING_1_.Add(element1);
	}

	KBEngine::FVariantArray args;
	args.Add(ARRAY_STRING_1_);

	entity->BaseCall(TEXT("clearReceiveGoodsDataRecord"), args);
}

void URoleShopMallInterface::RPC_takeBackGivingGoodsData(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShopMallInterface::RPC_takeBackGivingGoodsData : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->BaseCall(TEXT("takeBackGivingGoodsData"), args);
}

void URoleShopMallInterface::InitBlueCB()
{
	ArrBlueFunc.Add("GetShopMallItemList");
	ArrBlueFunc.Add("AddGivingGoodsDataRecord");
	ArrBlueFunc.Add("AddReceiveGoodsDataRecord");
	ArrBlueFunc.Add("InitGoodsDataRecord");
	ArrBlueFunc.Add("DealReceiveGivingGoodsDataCB");
	ArrBlueFunc.Add("ChangeGivingGoodsDataCB");
	ArrBlueFunc.Add("ClearGivingGoodsDataRecordCB");
	ArrBlueFunc.Add("ClearReceiveGoodsDataRecordCB");
	ArrBlueFunc.Add("InitCouponItem");
	ArrBlueFunc.Add("AddCouponItem");
	ArrBlueFunc.Add("RemoveCouponItem");
	Supper::InitBlueCB();
}

