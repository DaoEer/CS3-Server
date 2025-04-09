#include "RoleStoreInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/CS3Entity.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/MessageManager.h"
#include "Manager/CfgManager.h"
#include "CS3Base/UIManager.h"
#include "GameData/GameDefine.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameData/Item/ItemFactory.h"
#include "Util/ConvertUtil.h"
#include "Components/CapsuleComponent.h"
#include "Manager/EventManager.h"
#include "Manager/TimeManager.h"
#include "Level/ClothesHostsLevel.h"
#include "Actor/PinchFace/ModifyFaceCharacter.h"
#include "Kismet/KismetMathLibrary.h"
#include "Actor/GameCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START
		
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleStoreInterface, Supper)

CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnUpdateStoreGoods, &URoleStoreInterface::CLIENT_OnUpdateStoreGoods, const FString&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnGetRecommentGoods, &URoleStoreInterface::CLIENT_OnGetRecommentGoods, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnGetStoreNewGoods, &URoleStoreInterface::CLIENT_OnGetStoreNewGoods, const FString&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnUpdateBuyRecords, &URoleStoreInterface::CLIENT_OnUpdateBuyRecords, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnUpdatePresentRecords, &URoleStoreInterface::CLIENT_OnUpdatePresentRecords, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequestPresentGift, &URoleStoreInterface::CLIENT_OnRequestPresentGift, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnUpdateGiftBox, &URoleStoreInterface::CLIENT_OnUpdateGiftBox, const FVariant&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UpdateStoreCart, &URoleStoreInterface::CLIENT_UpdateStoreCart, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnGetGoodsListByIDList, &URoleStoreInterface::CLIENT_OnGetGoodsListByIDList, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddHasStoreAppearance, &URoleStoreInterface::AddHasStoreAppearance, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddStoreAppearance, &URoleStoreInterface::AddStoreAppearance, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RemoveStoreAppearance, &URoleStoreInterface::RemoveStoreAppearance, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateStoreBackAdornParam, &URoleStoreInterface::UpdateStoreBackAdornParam, int32, FString)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnUpdateStoreAppearance, &URoleStoreInterface::OnUpdateStoreAppearance, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnStoreBuyComplete, &URoleStoreInterface::OnStoreBuyComplete)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleStoreInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleStoreInterface::URoleStoreInterface()
{
}


URoleStoreInterface::~URoleStoreInterface()
{
}

void URoleStoreInterface::onEnterWorld()
{
	Init();
	Super::onEnterWorld();
}

void URoleStoreInterface::onLeaveWorld()
{
	ClearAllData();
	Super::onLeaveWorld();
}
void URoleStoreInterface::CLIENT_OnUpdateStoreGoods(const FString& cfgTime, const FVariant& FSTOREGOODS_DICT_1)
{
	FSTOREGOODS_DICT* goodsList = new FSTOREGOODS_DICT(FSTOREGOODS_DICT_1);
	TArray<FSTORE_GOODS_DATA_TABLE> GoodsList;
	for (auto i : goodsList->Datas1)
	{
		FSTORE_GOODS_DATA_TABLE Temp;
		Temp = AnalysisStoreGoods(i);
		GoodsList.Add(Temp);
	}
	OnUpdateStoreGoods(SortStoreGoods(GoodsList), cfgTime);
	if (GoodsList.Num() >= 1)
	{
		CLIENT_OnUpdateStoreGoodsOver(GoodsList[0].GoodsType, GoodsList[0].ItemType);
	}
}

void URoleStoreInterface::RPC_GetGoodsListByIDList(const TArray<int32>& GoodsIDList)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_RequestBuyStoreGoods no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(GoodsIDList));
	entity->BaseCall(TEXT("getGoodsListByIDList"), args);

}

void URoleStoreInterface::CLIENT_OnGetGoodsListByIDList(const FVariant& FSTOREGOODS_DICT_1)
{
	FSTOREGOODS_DICT* goodsList = new FSTOREGOODS_DICT(FSTOREGOODS_DICT_1);
	TArray<FSTORE_GOODS_DATA_TABLE> GoodsList;
	for (auto i : goodsList->Datas1)
	{
		FSTORE_GOODS_DATA_TABLE Temp;
		Temp = AnalysisStoreGoods(i);
		GoodsList.Add(Temp);
		StoreGoodsDatas.Add(Temp.ID, Temp);
	}
	OnGetGoodsListByIDListOver(GoodsList);
}

void URoleStoreInterface::CLIENT_OnGetRecommentGoods(const FVariant& FSTOREGOODS_DICT_1)
{
	FSTOREGOODS_DICT* goodsList = new FSTOREGOODS_DICT(FSTOREGOODS_DICT_1);
	TArray<FSTORE_GOODS_DATA_TABLE> GoodsList;
	for (auto i : goodsList->Datas1)
	{
		FSTORE_GOODS_DATA_TABLE Temp;
		Temp = AnalysisStoreGoods(i);
		GoodsList.Add(Temp);
	}
	OnUpdateRecommentGoods(SortStoreGoods(GoodsList));
	OnGetRecommentGoodsOver();
}

FSTORE_GOODS_DATA_TABLE URoleStoreInterface::AnalysisStoreGoods(FSTOREGOODS Value)
{
	FSTORE_GOODS_DATA_TABLE Temp;
	Temp.ID = Value.ID1;
	Temp.GoodsType = Value.GoodsType2;
	Temp.GoodsState = Value.GoodsState3;
	Temp.ItemType = Value.ItemType4;
	Temp.ItemID = Value.ItemID5;
	Temp.Price = Value.Price6;
	Temp.LimitTime = Value.LimitTime7;
	Temp.LimitAmount = Value.LimitAmount8;
	Temp.ServeLimitAmount = Value.ServeLimitAmount9;
	Temp.DiscountTime = Value.DiscountTime10;
	Temp.DiscountPrice = Value.DiscountPrice11;
	Temp.RefreshType = Value.RefreshType12;
	Temp.Description = Value.Description13;
	Temp.ThirdLable = Value.ThirdLable14;
	Temp.RebateRate = Value.RebateRate15;
	return Temp;

}

void URoleStoreInterface::CLIENT_OnUpdateStoreGoodsOver_Implementation(const int32& GoodType, const int32& ItemType)
{

}

void URoleStoreInterface::RPC_GetStoreNewGoods(const int32& GoodType)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_GetStoreNewGoods no this Entity!"));
		return;
	}
	FString strArgs = TEXT("");
	if (NewGoodsConfigTime.Contains(GoodType))
	{
		strArgs = NewGoodsConfigTime[GoodType];
	}
	KBEngine::FVariantArray args;
	args.Add(GoodType);
	args.Add(strArgs);
	entity->BaseCall(TEXT("getStoreNewGoods"), args);
}

void URoleStoreInterface::CLIENT_OnGetStoreNewGoods(const FString& cfgTime, const FVariant& FSTOREGOODS_DICT_1)
{
	FSTOREGOODS_DICT* goodsList = new FSTOREGOODS_DICT(FSTOREGOODS_DICT_1);
	TArray<FSTORE_GOODS_DATA_TABLE> GoodsList;
	for (auto i : goodsList->Datas1)
	{
		FSTORE_GOODS_DATA_TABLE Temp;
		Temp = AnalysisStoreGoods(i);
		GoodsList.Add(Temp);
	}
	OnUpdateStoreNewGoods(SortStoreGoods(GoodsList));
	int32 GoodsType = 0;
	if (GoodsList.Num() >= 1)
	{
		GoodsType = GoodsList[0].GoodsType;
		NewGoodsConfigTime.Add(GoodsType, cfgTime);
	}
	CLIENT_OnUpdateStoreNewGoodsOver(GoodsType);
}

void URoleStoreInterface::CLIENT_OnUpdateStoreNewGoodsOver_Implementation(const int32& GoodType)
{


}
void URoleStoreInterface::CLIENT_OnUpdateBuyRecords(const FVariant& FSTORE_BUY_RECORD_DICT_1)
{
	FSTORE_BUY_RECORD_DICT* Records = new FSTORE_BUY_RECORD_DICT(FSTORE_BUY_RECORD_DICT_1);
	TArray <FSTORE_BUY_RECORD_DATA> Temp;
	for (auto i : Records->Datas1)
	{
		FSTORE_BUY_RECORD_DATA TempData = AnalysisBuyRecord(i);
		Temp.Add(TempData);
	}
	SetBuyRecords(Temp);
	OnQueryBuyRecords();
}

FSTORE_BUY_RECORD_DATA URoleStoreInterface::AnalysisBuyRecord(FSTORE_BUY_RECORD data)
{
	FSTORE_BUY_RECORD_DATA TempData;
	TempData.goodsID = data.goodsID1;
	TempData.amount = data.amount2;
	TempData.buyTime = data.buyTime3;
	TempData.uid = data.uid4;
	TempData.price = data.price5;
	TempData.goodsType = data.goodsType6;
	TempData.itemID = data.itemID7;

	return TempData;
}

void URoleStoreInterface::CLIENT_OnRequestStoreLimitGoodsList_Implementation(const TArray<int32>& goodsIDList, const TArray<int32>& amountList)
{

}

void URoleStoreInterface::CLIENT_StoreNotEnoughMoney_Implementation(const int32& GoodType)
{

}

void URoleStoreInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnUpdateStoreGoods");
	ArrBlueFunc.Add("CLIENT_OnRequestStoreLimitGoodsList");
	ArrBlueFunc.Add("CLIENT_OnUpdateBuyRecords");
	ArrBlueFunc.Add("CLIENT_OnUpdatePresentRecords");
	ArrBlueFunc.Add("CLIENT_OnUpdateStoreGoodsOver");
	ArrBlueFunc.Add("CLIENT_OnUpdateGiftBox");
	ArrBlueFunc.Add("CLIENT_StoreNotEnoughMoney");
	ArrBlueFunc.Add("CLIENT_OnGetGoodsListByIDList");
	ArrBlueFunc.Add("CLIENT_OnGetStoreNewGoods");
	ArrBlueFunc.Add("OnUpdateStoreNewGoodsOver");
	ArrBlueFunc.Add("CLIENT_UpdateStoreCart");
	ArrBlueFunc.Add("CLIENT_OnAddStoreCartGoods");
	ArrBlueFunc.Add("CLIENT_OnDeleteStoreCartGoods");
	ArrBlueFunc.Add("CLIENT_OnClearStoreCartGoods");
	ArrBlueFunc.Add("CLINET_OnDeleteBuyRecord");
	ArrBlueFunc.Add("CLINET_OnDeleteBuyRecords");
	ArrBlueFunc.Add("CLINET_OnDeletePresentRecord");
	ArrBlueFunc.Add("CLINET_OnDeletePresentRecords");
	ArrBlueFunc.Add("CLINET_OnDeleteGiftBoxReceiveRecord");
	ArrBlueFunc.Add("CLINET_OnDeleteGiftBoxReceiveRecords");
	ArrBlueFunc.Add("CLINET_OnDeleteGiftBoxSendRecord");
	ArrBlueFunc.Add("CLINET_OnDeleteGiftBoxSendRecords"); 
	ArrBlueFunc.Add("CLIENT_OnUpdateStoreNewGoodsOver");
	ArrBlueFunc.Add("CLIENT_OnRequestPresentGift");
	ArrBlueFunc.Add("CLIENT_OnGetRecommentGoods");
	ArrBlueFunc.Add("CLINET_GiftBoxShowRedPoint");
	Supper::InitBlueCB();
}

void URoleStoreInterface::RPC_RequestBuyStoreGoods(int32 GoodsID, int32 Amount)
{

	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_RequestBuyStoreGoods no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(GoodsID);
	args.Add(Amount);
	entity->BaseCall(TEXT("requestBuyStoreGoods"), args);
}

void URoleStoreInterface::RPC_DeleteBuyRecord(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteBuyRecord no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UID);
	entity->BaseCall(TEXT("deleteBuyRecord"), args);
}

void URoleStoreInterface::CLINET_OnDeleteBuyRecord_Implementation(const FString& UID)
{
	DeleteBuyRecord(UID);
}

void URoleStoreInterface::RPC_DeleteBuyRecords()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteBuyRecords no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("deleteBuyRecords"), args);
}

void URoleStoreInterface::CLINET_OnDeleteBuyRecords_Implementation()
{
	DeleteBuyRecords();
}

void URoleStoreInterface::RPC_RequestStoreLimitGoodsList()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_RequestStoreLimitGoodsList no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("requestStoreLimitGoodsList"), args);
}

void URoleStoreInterface::RPC_QueryBuyRecords()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_QueryBuyRecords no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("queryBuyRecords"), args);
}

void URoleStoreInterface::RPC_RequestPresentGift(const int32 GoodsID, const int32& Amount, const FString& ReceiverName, const FString& ReceiverDBID, const FString& Message)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_QueryBuyRecords no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(GoodsID);
	args.Add(Amount);
	args.Add(ReceiverName);
	args.Add(ReceiverDBID);
	args.Add(Message);
	entity->BaseCall(TEXT("requestPresentGift"), args);
}

void URoleStoreInterface::RPC_QueryPresentRecords()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_QueryPresentRecords no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("queryPresentRecords"), args);
}

void URoleStoreInterface::CLIENT_OnUpdatePresentRecords(const FVariant& FSTORE_PRESENT_RECORD_DICT_1)
{
	FSTORE_PRESENT_RECORD_DICT* Records = new FSTORE_PRESENT_RECORD_DICT(FSTORE_PRESENT_RECORD_DICT_1);
	TArray <FSTORE_PRESENT_RECORD_DATA> Temp;
	for (auto i : Records->Datas1)
	{
		FSTORE_PRESENT_RECORD_DATA TempData = AnalysisPresentRecord(i);
		Temp.Add(TempData);
	}

	SetPresentRecords(Temp);
	OnUpdatePresentRecords();
}

FSTORE_PRESENT_RECORD_DATA URoleStoreInterface::AnalysisPresentRecord(FSTORE_PRESENT_RECORD data)
{
	FSTORE_PRESENT_RECORD_DATA TempData;
	TempData.goodsID = data.goodsID1;
	TempData.amount = data.amount2;
	TempData.buyTime = data.buyTime3;
	TempData.uid = data.uid6;
	TempData.sender = data.sender4;
	TempData.receiver = data.receiver5;
	TempData.price = data.price7;
	TempData.receiverDBID = data.receiverDBID8;
	TempData.senderDBID = data.senderDBID9;
	TempData.itemID = data.itemID10;

	return TempData;
}

void URoleStoreInterface::RPC_DeletePresentRecord(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeletePresentRecord no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UID);
	entity->BaseCall(TEXT("deletePresentRecord"), args);
}

void URoleStoreInterface::CLINET_OnDeletePresentRecord_Implementation(const FString& UID)
{
	DeletePresentRecord(UID);
}

void URoleStoreInterface::RPC_DeletePresentRecords()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeletePresentRecord no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("deletePresentRecords"), args); 

}
void URoleStoreInterface::CLINET_OnDeletePresentRecords_Implementation()
{
	DeletePresentRecords();
}

void URoleStoreInterface::RPC_requestOpenGiftBox()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_QueryBuyRecords no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("requestOpenGiftBox"), args);
}

void URoleStoreInterface::CLIENT_OnRequestPresentGift(const FVariant& FSTORE_GIFT_BOX_DATA_1)
{
	FSTORE_GIFT_BOX_DATA* SendGift = new FSTORE_GIFT_BOX_DATA(FSTORE_GIFT_BOX_DATA_1);
	FSTORE_GIFT_BOX Temp = AnalysisGiftBox(*SendGift);
	OnRequestPresentGift(Temp);
	OnRequestPresentGiftOver(Temp);
}

void URoleStoreInterface::CLIENT_OnUpdateGiftBox(const  FVariant& FSTORE_GIFT_BOX_DATA_DICT_1, const FVariant& FSTORE_GIFT_BOX_DATA_DICT_2)
{
	FSTORE_GIFT_BOX_DATA_DICT* SendGiftDict = new FSTORE_GIFT_BOX_DATA_DICT(FSTORE_GIFT_BOX_DATA_DICT_1);
	FSTORE_GIFT_BOX_DATA_DICT* ReceiveGiftDict = new FSTORE_GIFT_BOX_DATA_DICT(FSTORE_GIFT_BOX_DATA_DICT_2);
	TArray <FSTORE_GIFT_BOX> TempList1;
	TArray <FSTORE_GIFT_BOX> TempList2;
	for (auto i : SendGiftDict->Datas1)
	{
		FSTORE_GIFT_BOX Temp1 = AnalysisGiftBox(i);
		TempList1.Add(Temp1);
	}

	for (auto i : ReceiveGiftDict->Datas1)
	{
		FSTORE_GIFT_BOX Temp2 = AnalysisGiftBox(i);
		TempList2.Add(Temp2);
	}
	OnRequestOpenGiftBox(TempList1, TempList2);
	OnUpdateGiftBox();
	OnUpdateReceiveGiftBoxAmount(GetNoStateGiftBoxAmount());

}

FSTORE_GIFT_BOX URoleStoreInterface::AnalysisGiftBox(FSTORE_GIFT_BOX_DATA data)
{
	FSTORE_GIFT_BOX temp;
	temp.goodsID = data.goodsID1;
	temp.amount = data.amount2;
	temp.receiverName = data.receiverName3;
	temp.receiverDBID = data.receiverDBID4;
	temp.senderName = data.senderName5;
	temp.senderDBID = data.senderDBID6;
	temp.endTime = data.endTime7;
	temp.giftState = data.giftState8;
	temp.message = data.message9;
	temp.uid = data.uid10;
	temp.overtime = data.overtime11;
	temp.price = data.price12;
	temp.itemID = data.itemID13;

	return temp;
}

void URoleStoreInterface::RPC_AcceptGift(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_AcceptGift no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UID);
	entity->BaseCall(TEXT("acceptGift"), args);
}

void URoleStoreInterface::RPC_AcceptGifts()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_AcceptGifts no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("acceptGifts"), args);
}

void URoleStoreInterface::RPC_RefuseGift(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_RefuseGift no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UID);
	entity->BaseCall(TEXT("refuseGift"), args);
}

void URoleStoreInterface::RPC_RefuseGifts()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_RefuseGifts no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("refuseGifts"), args);
}

void URoleStoreInterface::RPC_DeleteGiftBoxReceiveRecord(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteGiftBoxReceiveRecord no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UID);
	entity->BaseCall(TEXT("deleteGiftBoxReceiveRecord"), args);
}

void URoleStoreInterface::CLINET_OnDeleteGiftBoxReceiveRecord_Implementation(const FString& UID)
{
	DeleteReceiverGiftBox(UID);
}

void URoleStoreInterface::RPC_DeleteGiftBoxReceiveRecords()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteGiftBoxReceiveRecords no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("deleteGiftBoxReceiveRecords"), args);
}

void URoleStoreInterface::CLINET_OnDeleteGiftBoxReceiveRecords_Implementation()
{
	DeleteReceiverGiftBoxs();
}

void URoleStoreInterface::RPC_GetBackGift(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_GetBackGift no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UID);
	entity->BaseCall(TEXT("getBackGift"), args);
}

void URoleStoreInterface::RPC_GetBackGifts()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_GetBackGifts no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("getBackGifts"), args);
}

void URoleStoreInterface::RPC_DeleteGiftBoxSendRecord(const FString& UID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteGiftBoxSendRecord no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UID);
	entity->BaseCall(TEXT("deleteGiftBoxSendRecord"), args);
}

void URoleStoreInterface::CLINET_OnDeleteGiftBoxSendRecord_Implementation(const FString& UID)
{
	DeleteSenderGiftBox(UID);
}

void URoleStoreInterface::RPC_DeleteGiftBoxSendRecords()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteGiftBoxSendRecords no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("deleteGiftBoxSendRecords"), args);
}

void URoleStoreInterface::CLINET_OnDeleteGiftBoxSendRecords_Implementation()
{
	DeleteSenderGiftBoxs();
}

void URoleStoreInterface::RPC_TransferPresent(const FString& UID, const FString& ReceiverName, const FString& ReceiverDBID, const FString& Message)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteGiftBoxSendRecords no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UID);
	args.Add(ReceiverName);
	args.Add(ReceiverDBID);
	args.Add(Message);
	entity->BaseCall(TEXT("transferPresent"), args);
}

void URoleStoreInterface::RPC_BuyStoreCartGoods(TArray<int32> GoodsIDList, TArray<int32> AmountList)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_BuyStoreCartGoods no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(GoodsIDList));
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(AmountList));
	entity->BaseCall(TEXT("buyStoreCartGoods"), args);
}

void URoleStoreInterface::RPC_PresentStoreCartGoods(TArray<int32> GoodsIDList, TArray<int32> AmountList, const FString& ReceiverName, const FString& ReceiverDBID, const FString& Message)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_PresentStoreCartGoods no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(GoodsIDList));
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(AmountList));
	args.Add(ReceiverName);
	args.Add(ReceiverDBID);
	args.Add(Message);
	entity->BaseCall(TEXT("presentStoreCartGoods"), args);
}

void URoleStoreInterface::RPC_AddStoreCartGoods(int32 GoodsType, int32 GoodsID, int32 Amount)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_AddStoreCartGoods no this Entity!"));
		return;
	}

	int32 Max = UUECS3GameInstance::Instance->ConstDataBP->STORE_CART_CAPACIYT;
	int32 CartType = GetCartTypeByGoodsType(GoodsType);
	if (StoreCart.Contains(CartType))
	{
		if (StoreCart[CartType].Num() >= Max)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5221);
			return;
		}
		if (StoreCart[CartType].Contains(GoodsID))
		{
			if (StoreCart[CartType][GoodsID].GoodsState == (int32)STORE_GOODS_STATE::STORE_GOODS_STATE_SOLD_OUT)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5211);
				return;
			}
			//LimitAmount=-1表示不限制购买，但购物车限制一次性最多购买999
			//LimitAmount不为0表示限制购买
			int32 LimitAmount = StoreCart[CartType][GoodsID].LimitAmount;
			int32 NewAmount = StoreCart[CartType][GoodsID].Amount + Amount;
			if ((LimitAmount < 0 && NewAmount > BuyLimitAmount) || (LimitAmount >= 0 && NewAmount > LimitAmount))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(1305);
				return;
			}
		}
	}	
	KBEngine::FVariantArray args;
	args.Add(CartType);
	args.Add(GoodsID);
	args.Add(Amount);
	entity->BaseCall(TEXT("addStoreCartGoods"), args);
}

void URoleStoreInterface::CLIENT_OnAddStoreCartGoods_Implementation(int32 GoodsType, int32 GoodsID, int32 Amount)
{
	int32 CartType = GetCartTypeByGoodsType(GoodsType);
	if (StoreCart.Contains(CartType))
	{
		if (StoreCart[CartType].Contains(GoodsID))
		{
			StoreCart[CartType][GoodsID].Amount += Amount;
		}
		else
		{
			FSTORE_GOODS_DATA_TABLE Goods = GetStoreGoodsByID(GoodsID);
			Goods.Amount = Amount;
			StoreCart[CartType].Add(GoodsID, Goods);
		}
	}
	else
	{
		TMap<int32, FSTORE_GOODS_DATA_TABLE> Temp;
		FSTORE_GOODS_DATA_TABLE Goods = GetStoreGoodsByID(GoodsID);
		Goods.Amount = Amount;
		Temp.Add(GoodsID, Goods);
		StoreCart.Add(CartType, Temp);
	}

}

void URoleStoreInterface::RPC_DeleteStoreCartGoods(int32 GoodsType, int32 GoodsID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteStoreCartGoods no this Entity!"));
		return;
	}
	int32 CartType = GetCartTypeByGoodsType(GoodsType);
	if (!StoreCart.Contains(CartType))
	{
		return;
	}
	if (!StoreCart[CartType].Contains(GoodsID))
	{
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(CartType);
	args.Add(GoodsID);
	entity->BaseCall(TEXT("deleteStoreCartGoods"), args);
	OnDeleteStoreCartGoods(CartType, GoodsID);
}

void URoleStoreInterface::CLIENT_OnDeleteStoreCartGoods_Implementation(int32 GoodsType, int32 GoodsID)
{
	int32 CartType = GetCartTypeByGoodsType(GoodsType);
	if (StoreCart.Contains(CartType) && StoreCart[CartType].Contains(GoodsID))
	{
		StoreCart[CartType].Remove(GoodsID);
		if (StoreCart[CartType].Num() == 0)
		{
			StoreCart.Remove(CartType);
		}
	}
}

void URoleStoreInterface::RPC_ClearStoreCartGoods(int32 CartType)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_ClearStoreCartGoods no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(CartType);
	entity->BaseCall(TEXT("clearStoreCartGoods"), args);
}

void URoleStoreInterface::CLIENT_OnClearStoreCartGoods_Implementation(int32 CartType)
{
	if (StoreCart.Contains(CartType))
	{
		StoreCart.Remove(CartType);
	}
}

void URoleStoreInterface::RPC_DeleteSoldOutStoreCartGoods(const int32& CartType)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_DeleteSoldOutStoreCartGoods no this Entity!"));
		return;
	}
	if (!StoreCart.Contains(CartType))
	{
		return;
	}
	TArray<int32> GoodsIDs;
	for (auto goods: StoreCart[CartType])
	{
		if (goods.Value.GoodsState == (int32)STORE_GOODS_STATE::STORE_GOODS_STATE_SOLD_OUT)
		{
			GoodsIDs.Add(goods.Key);
		}
	}
	if (GoodsIDs.Num() == 0)
	{
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(CartType);
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(GoodsIDs));
	entity->BaseCall(TEXT("deleteSoldOutStoreCartGoods"), args);
}

void URoleStoreInterface::OnDeleteSoldOutStoreCartGoods_Implementation(const int32& CartType, const TArray<int32>& GoodsIDs)
{
	if (StoreCart.Contains(CartType))
	{
		for (auto goodsID : GoodsIDs)
		{
			if (StoreCart[CartType].Contains(goodsID))
			{
				StoreCart[CartType].Remove(goodsID);
			}
		}
		if (StoreCart[CartType].Num() == 0)
		{
			StoreCart.Remove(CartType);
		}
	}
	OnUpdateStoreCart();
}

void URoleStoreInterface::RPC_SynStoreCartGoods()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_SynStoreCartGoods no this Entity!"));
		return;
	}
	for (auto i : StoreCart)
	{
		TArray<int32> GoodsIDList; TArray<int32> AmountList;
		for (auto j : i.Value)
		{
			GoodsIDList.Add(j.Value.ID);
			AmountList.Add(j.Value.Amount);
		}
		KBEngine::FVariantArray args;
		args.Add(i.Key);
		args.Add(UGolbalBPFunctionLibrary::ListToFVariant(GoodsIDList));
		args.Add(UGolbalBPFunctionLibrary::ListToFVariant(AmountList));
		entity->BaseCall(TEXT("synStoreCartGoods"), args);
	}

}

void URoleStoreInterface::RPC_OpenStoreCart()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_OpenStoreCart no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("openStoreCart"), args);
}

void URoleStoreInterface::CLIENT_UpdateStoreCart(const FVariant& FSTORE_CART_DATA_DICT_1)
{
	FSTORE_CART_DATA_DICT* Data = new FSTORE_CART_DATA_DICT(FSTORE_CART_DATA_DICT_1);
	for (auto i : Data->Datas1)
	{
		FSTORE_GOODS_DATA_TABLE Goods = GetStoreGoodsByID(i.goodsID2);
		Goods.Amount = i.amount3;
		int32 CartType = GetCartTypeByGoodsType(i.goodsType1);
		if (!StoreCart.Contains(CartType))
		{
			TMap<int32, FSTORE_GOODS_DATA_TABLE> Temp;
			Temp.Add(Goods.ID, Goods);
			StoreCart.Add(CartType, Temp);
		}
		StoreCart[CartType].Add(i.goodsID2, Goods);
	}
	OnUpdateStoreCart();

}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetStoreCartGoods(int32 CartType)
{
	TArray<FSTORE_GOODS_DATA_TABLE> Temp;
	if (StoreCart.Contains(CartType))
	{
		for (auto i : StoreCart[CartType])
		{
			Temp.Add(i.Value);
		}
	}
	return Temp;
}

int32 URoleStoreInterface::GetAllStoreCartGoodsAmount()
{
	int32 Amount = 0;
	for (auto i : StoreCart)
	{

		Amount += i.Value.Num();
	}
	return Amount;
}

void URoleStoreInterface::SetStoreCartGoods(int32 GoodsType, int32 GoodsID, int32 Amount)
{
	int32 CartType = GetCartTypeByGoodsType(GoodsType);
	if (StoreCart.Contains(CartType) && StoreCart[CartType].Contains(GoodsID))
	{
		if ((StoreCart[CartType][GoodsID].Amount) <= StoreCart[CartType][GoodsID].LimitAmount || StoreCart[CartType][GoodsID].LimitAmount == -1)
		{
			StoreCart[CartType][GoodsID].Amount = Amount;
			OnUpdateStoreCartGoodsAmount(GoodsType, GoodsID, Amount);
		}
	}
} 

int32 URoleStoreInterface::GetCartTypeByGoodsType(int32 GoodsType)
{
	switch (GoodsType)
	{
	case 1:	//对应 STORE_GOODS_TYPE
		return 1;	//对应STORE_TYPE
	case 2:
		return 1;
	case 3:
		return 1;
	case 4:
		return 3;
	default:
		return 1;
	}
}

void URoleStoreInterface::GetAppearanceData(int32 GoodsID, int32& AppearType, FString& AppearID)
{
	FSTORE_GOODS_DATA_TABLE GoodsData = GetStoreGoodsByID(GoodsID);
	GetAppearanceDataByItemID(GoodsData.ItemID, AppearType, AppearID);
}

void URoleStoreInterface::GetAppearanceDataByItemID(int32 ItemID, int32& AppearType, FString& AppearID)
{
	FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(ItemID);
	AppearType = FSTRING_TO_INT(ItemData.Param1);
	AppearID = ItemData.Param2;
}

void URoleStoreInterface::ChangeWeather(bool IsNightWeather)
{
	if (IsNightWeather)
	{
		UUECS3GameInstance::Instance->GEventManager->OnTriggerDynamicEnvironmentEvent.Broadcast(TEXT("L_HRG_Heiye"), 1);
	}
	else
	{
		UUECS3GameInstance::Instance->GEventManager->OnBackDynamicEnvironmentEvent.Broadcast();
	}
}

void URoleStoreInterface::AddHasStoreAppearance(const int32 & ItemID)
{
	if (!HasStoreAppearances.Contains(ItemID))
	{
		HasStoreAppearances.Add(ItemID);
	}
	OnAddHasStoreAppearance(ItemID);
}

void URoleStoreInterface::OnAddHasStoreAppearance(const int32& ItemID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAddHasStoreAppearance.Broadcast(ItemID);
	}
}

void URoleStoreInterface::RPC_PutOnStoreAppearance(int32 AppearanceType, FString AppearanceID, int32 ItemID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_PutOnStoreAppearance : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(AppearanceType);
	args.Add(AppearanceID);
	args.Add(ItemID);
	GetEntity()->CellCall(TEXT("putOnStoreAppearance"), args);
}

void URoleStoreInterface::RPC_TakeOffStoreAppearance(int32 AppearanceType, FString AppearanceID, int32 ItemID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_TakeOffStoreAppearance : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(AppearanceType);
	args.Add(AppearanceID);
	args.Add(ItemID);
	GetEntity()->CellCall(TEXT("takeOffStoreAppearance"), args);
}

void URoleStoreInterface::AddStoreAppearance(const int32 & ItemID)
{
	if (!StoreAppearances.Contains(ItemID))
	{
		StoreAppearances.Add(ItemID);
	}
	OnAddStoreAppearance(ItemID);
}

void URoleStoreInterface::OnAddStoreAppearance(const int32& ItemID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAddStoreAppearance.Broadcast(ItemID);
	}
}

void URoleStoreInterface::RemoveStoreAppearance(const int32 & ItemID)
{
	if (StoreAppearances.Contains(ItemID))
	{
		StoreAppearances.Remove(ItemID);
	}
	OnRemoveStoreAppearance(ItemID);
}

void URoleStoreInterface::OnRemoveStoreAppearance(const int32& ItemID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRemoveStoreAppearance.Broadcast(ItemID);
	}
}

void URoleStoreInterface::OnAddStoreTryAppearances(const int32& PartType, const int32& GoodsID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAddStoreTryAppearance.Broadcast(PartType, GoodsID);
	}
}

void URoleStoreInterface::OnRemoveStoreTryAppearances(const int32& PartType, const int32& GoodsID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRemoveStoreTryAppearance.Broadcast(PartType, GoodsID);
	}
}

void URoleStoreInterface::OnClearStoreTryAppearances()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnClearStoreTryAppearance.Broadcast();
	}
}

void URoleStoreInterface::RPC_SetStoreBackAdornParam(int32 ItemID, FVector Location, FRotator Rotation)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestReplacePetSkill : GetEntity()!"));
		return;
	}
	FString ParamStr = INT_TO_FSTRING((int32)Location.X);
	ParamStr += ",";
	ParamStr += INT_TO_FSTRING((int32)Location.Y);
	ParamStr += ",";
	ParamStr += INT_TO_FSTRING((int32)Location.Z);
	ParamStr += "|";
	ParamStr += INT_TO_FSTRING((int32)Rotation.Pitch);
	ParamStr += ",";
	ParamStr += INT_TO_FSTRING((int32)Rotation.Yaw);
	ParamStr += ",";
	ParamStr += INT_TO_FSTRING((int32)Rotation.Roll);
	KBEngine::FVariantArray args;
	args.Add(ItemID);
	args.Add(ParamStr);
	GetEntity()->CellCall(TEXT("setStoreBackAdornParam"), args);
}

void URoleStoreInterface::UpdateStoreBackAdornParam(int32 ItemID, FString ParamStr)
{
	FSTORE_BACK_ADORN_PARAM Temp;
	TArray<FString> strArr = UGolbalBPFunctionLibrary::SplitString(ParamStr);
	if (strArr.Num() == 2)
	{
		TArray<int32> LocationArray = UGolbalBPFunctionLibrary::StringListToIntList(UGolbalBPFunctionLibrary::SplitString(strArr[0], false, ","));
		TArray<int32> RotationArray = UGolbalBPFunctionLibrary::StringListToIntList(UGolbalBPFunctionLibrary::SplitString(strArr[1], false, ","));
		if (LocationArray.Num() == 3)
		{
			Temp.Location = FVector(LocationArray[0], LocationArray[1], LocationArray[2]);
		}
		if (RotationArray.Num() == 3)
		{
			Temp.Rotation = FRotator(RotationArray[0], RotationArray[1], RotationArray[2]);
		}
		StoreBackAdornParam.Add(ItemID, Temp);
	}

}

FSTORE_BACK_ADORN_PARAM URoleStoreInterface::GetStoreBackAdornParam(const int32 & ItemID)
{
	if (StoreBackAdornParam.Contains(ItemID))
	{
		return StoreBackAdornParam[ItemID];
	}
	return FSTORE_BACK_ADORN_PARAM();
}

bool URoleStoreInterface::IsItemAppearacesExpired(const int32 & ItemID)
{
	FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(ItemID);
	FString LimitTime = ItemData.LimitTime;
	if (LimitTime == "") return false;
	TArray<FString> strArr = UGolbalBPFunctionLibrary::SplitString(LimitTime);
	if (strArr.Num() <2) return false;
	if (FSTRING_TO_INT(strArr[0]) == 1)
	{
		URoleKitBagInterface *kitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), EntityID));
		if (kitBagInterface)
		{
			TArray<UItemBase*> ItemList = kitBagInterface->GetItemsByItemID(ItemID);
			if (ItemList.Num() == 0) return false;
			for (auto i : ItemList)
			{
				if (i->ItemOrder >= BAG_APPEARANCES_START && i->ItemOrder < BAG_APPEARANCES_START + STORE_APPEARANCE_CAPACITY)
				{
					UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
					if (i->ItemEndTime == "")
					{
						return false;
					}
					FDateTime EndTime = TimeManager->ServerTimeToClientTime(FSTRING_TO_INT64(i->ItemEndTime));
					int64 Time = (FDateTime::UtcNow() - EndTime).GetTicks();
					return Time <= 0;
				}
			}
		}
	} else if (FSTRING_TO_INT(strArr[0]) == 2)
	{
		TArray<FString> Time1StrArr = UGolbalBPFunctionLibrary::SplitString(strArr[1], false, TEXT("/"));
		if (Time1StrArr.Num() != 4) return false;
		TArray<FString> Time2StrArr = UGolbalBPFunctionLibrary::SplitString(strArr[3], false, TEXT(":"));
		if (Time2StrArr.Num() != 3) return false;
		int Year = FSTRING_TO_INT(Time1StrArr[0]);
		int Month = FSTRING_TO_INT(Time1StrArr[1]);
		int Day = FSTRING_TO_INT(Time1StrArr[2]);
		int Hour = FSTRING_TO_INT(Time2StrArr[0]);
		int Minute = FSTRING_TO_INT(Time2StrArr[1]);
		int Seconds = FSTRING_TO_INT(Time2StrArr[2]);
		int64 Time = (FDateTime::UtcNow() - FDateTime(Year, Month, Day, Hour, Minute, Seconds)).GetTicks();
		return Time <= 0;
	}
	return false;
}

STORE_APPEARANCE_STATE URoleStoreInterface::StoreAppearanceState(const int32 & GoodsID)
{
	FSTORE_GOODS_DATA_TABLE goods = GetStoreGoodsByID(GoodsID);
	int32 ItemID = goods.ItemID;
	FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(ItemID);
	FString LimitTime = ItemData.LimitTime;
	if (HasStoreAppearances.Contains(ItemID) && StoreAppearances.Contains(ItemID))
	{
		return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_WEAR;
	} else if (!HasStoreAppearances.Contains(ItemID) && IsStoreTryAppearance(ItemID)) {
		return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_TRY;
	} else if (!HasStoreAppearances.Contains(ItemID)&& LimitTime != "" ) {
		return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_COUNTDOWN;
	} else if (HasStoreAppearances.Contains(ItemID) && LimitTime != "" && !IsItemAppearacesExpired(ItemID)) {
		return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_HAS_COUNTDOWN;
	} else if (HasStoreAppearances.Contains(ItemID) && LimitTime != "" && IsItemAppearacesExpired(ItemID)) {
		return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_EXPIRED;
	} else if (HasStoreAppearances.Contains(ItemID)) {
		return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_HAS;
	} else if (!HasStoreAppearances.Contains(ItemID)) {
		return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_HAS_NOT;
	}
	return STORE_APPEARANCE_STATE::STORE_APPEARANCE_STATE_HAS_NOT;
}

void URoleStoreInterface::AddStoreTryAppearances(const int32& PartType, const int32 & GoodsID)
{
	if (StoreTryAppearances.Contains(PartType))
	{
		int32 OldGoodsID = StoreTryAppearances[PartType];
		StoreTryAppearances[PartType] = GoodsID;
		OnRemoveStoreTryAppearances(PartType, OldGoodsID);//改完了数据才能调用，不然外观状态显示会不对
		OnAddStoreTryAppearances(PartType, GoodsID);
	}
	else
	{
		StoreTryAppearances.Add(PartType);
		StoreTryAppearances[PartType] = GoodsID;
		OnAddStoreTryAppearances(PartType, GoodsID);
	}
}

void URoleStoreInterface::RemoveStoreTryAppearances(const int32& PartType)
{
	if (StoreTryAppearances.Contains(PartType))
	{
		int32 GoodsID = StoreTryAppearances[PartType];
		StoreTryAppearances.Remove(PartType);
		OnRemoveStoreTryAppearances(PartType, GoodsID);//改完了数据才能调用，不然外观状态显示会不对
	}
}

void URoleStoreInterface::ClearStoreTryAppearances()
{
	StoreTryAppearances.Empty();
	OnClearStoreTryAppearances();
}

TMap<int32, int32> URoleStoreInterface::GetStoreTryAppearances()
{
	return StoreTryAppearances;
}

bool URoleStoreInterface::IsStoreTryAppearance(int32 ItemID)
{
	for (TPair<int32, int32>& AppaerGoods : StoreTryAppearances)
	{
		int32 GoodsID = AppaerGoods.Value;
		FSTORE_GOODS_DATA_TABLE GoodsData = GetStoreGoodsByID(GoodsID);
		if (GoodsData.ItemID == ItemID)
		{
			return true;
		}
	}
	return false;
}

TMap<MODEL_PART_TYPE, FString> URoleStoreInterface::GetStoreTryAppearancePart()
{
	TMap<MODEL_PART_TYPE, FString> PartMap;
	for (TPair<int32, int32>& AppaerGoods : StoreTryAppearances)
	{
		int32 GoodsID = AppaerGoods.Value;
		int32 AppearType;
		FString AppearID;
		FSTORE_GOODS_DATA_TABLE GoodsData = GetStoreGoodsByID(GoodsID);
		GetAppearanceDataByItemID(GoodsData.ItemID, AppearType, AppearID);
		if (AppearType != -1)
		{
			PartMap.Add(MODEL_PART_TYPE(AppearType), AppearID);
		}
	}
	return PartMap;
}

TArray<int32> URoleStoreInterface::GetStoreWearAppearances()
{
	return StoreAppearances;
}

int32 URoleStoreInterface::GetStoreHasAppearancesAmount(int32 AppearanceType)
{
	int32 Amount = 0;
	for (auto ItemID : HasStoreAppearances)
	{
		FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(ItemID);
		int32 AppearType = FSTRING_TO_INT(ItemData.Param1);
		if (AppearType == AppearanceType && ItemData.LimitTime == "")
		{
			++Amount;
		}
	}
	return Amount;
}


TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::FilterHasAppearances(TArray<FSTORE_GOODS_DATA_TABLE> GoodsDatas)
{
	TArray<FSTORE_GOODS_DATA_TABLE> ReturnGoodsDatas;
	for (FSTORE_GOODS_DATA_TABLE Goods : GoodsDatas)
	{
		if (HasStoreAppearances.Contains(Goods.ItemID))
		{
			ReturnGoodsDatas.Add(Goods);
		}
	}
	return ReturnGoodsDatas;
}

FCARRIER_DATA URoleStoreInterface::GetCarrierConfigData(FString CarrierID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FCARRIER_DATA *CarrierData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CARRIER)->GetRow<FCARRIER_DATA>(FSTRING_TO_FNAME(CarrierID));
	if (CarrierData)
	{
		return *CarrierData;
	}
	return FCARRIER_DATA();
}

void URoleStoreInterface::OnUpdateStoreAppearance(const int32 & AppearanceType)
{
	if (IsValid(GetStoreCharacter()))
	{
		//脱和穿都是取玩家最新的部件值，所以等同于单个部件重置一样逻辑
		GetStoreCharacter()->ResetStoreModelPart(MODEL_PART_TYPE(AppearanceType));
	}
}

AModifyFaceCharacter* URoleStoreInterface::GetStoreCharacter()
{
	AClothesHostsLevel* LevelScriptActor = Cast<AClothesHostsLevel>(UGolbalBPFunctionLibrary::GetMainLevelActor());
	if (IsValid(LevelScriptActor) && IsValid(LevelScriptActor->ModifyFaceCharacter))
	{
		return Cast<AModifyFaceCharacter>(LevelScriptActor->ModifyFaceCharacter);
	}
	return nullptr;
}

float URoleStoreInterface::SetVectorForFloat(FVector CurVector, AGameCharacter* TargetCharacter, FString PartID)
{
	auto ModelPartTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);
	const FMODEL_PART_DATA* ModelPartData = ModelPartTable->GetRow<FMODEL_PART_DATA>(PartID);
	if (ModelPartData&& IsValid(TargetCharacter))
	{
		FVector DirftLocation = CurVector - ModelPartData->PartTransform.RelativeLocation;
		//FVector PutLocation = UKismetMathLibrary::Divide_VectorVector(DirftLocation, TargetCharacter->GetCapsuleComponent()->GetRightVector());t
		float Ardon = DirftLocation.Y / (TargetCharacter->GetCapsuleComponent()->GetRightVector().Y*-1);
		return Ardon;
	}
	return 0.0f;
}

FVector URoleStoreInterface::SetFloatForVector(float CurDeviation, AGameCharacter* TargetCharacter, FString PartID)
{
	auto ModelPartTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);
	const FMODEL_PART_DATA* ModelPartData = ModelPartTable->GetRow<FMODEL_PART_DATA>(PartID);
	if (ModelPartData && IsValid(TargetCharacter))
	{
		FVector PutLocation = CurDeviation* (TargetCharacter->GetCapsuleComponent()->GetRightVector()*-1);
		FVector DirftLocation = PutLocation + ModelPartData->PartTransform.RelativeLocation;
		return DirftLocation;
	}
	return FVector::ZeroVector;
}

void URoleStoreInterface::Init()
{
	InitRemommentConfigData();
	InitStoreConfigData();
	InitStoreSearchConfigData();
}

void URoleStoreInterface::OnUpdateStoreGoods(const TArray<FSTORE_GOODS_DATA_TABLE> goodsList, const FString cfgTime)
{
	int32 GoodsType = 0;
	int32 ItemType = 0;
	for (auto goods : goodsList)
	{
		StoreGoodsDatas.Add(goods.ID, goods);
		GoodsType = goods.GoodsType;
		ItemType = goods.ItemType;
	}
	if (GoodsType == 0 || ItemType == 0)
	{
		return;
	}
	if (!StoreGoodsListDatas.Contains(GoodsType))
	{
		TMap<int32, TArray<FSTORE_GOODS_DATA_TABLE>> Temps;
		StoreGoodsListDatas.Add(GoodsType, Temps);
	}
	StoreGoodsListDatas[GoodsType].Add(ItemType, goodsList);
	if (!ConfigTime.Contains(GoodsType))
	{
		TMap<int32, FString> Temp;
		ConfigTime.Add(GoodsType, Temp);
	}
	ConfigTime[GoodsType].Add(ItemType, cfgTime);
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::SortStoreGoods(TArray<FSTORE_GOODS_DATA_TABLE> GoodsList)
{
	TMap<int32, int32> SortKey;
	SortKey.Add((int32)STORE_GOODS_STATE::STORE_GOODS_STATE_NEW_PRODUCT, 1);
	SortKey.Add((int32)STORE_GOODS_STATE::STORE_GOODS_STATE_HOT_SELL, 2);
	SortKey.Add((int32)STORE_GOODS_STATE::STORE_GOODS_STATE_NONE, 3);
	SortKey.Add((int32)STORE_GOODS_STATE::STORE_GOODS_STATE_SOLD_OUT, 4);
	GoodsList.Sort([this, SortKey](const FSTORE_GOODS_DATA_TABLE data1, const FSTORE_GOODS_DATA_TABLE data2)
	{
		if (SortKey[data1.GoodsState] < SortKey[data2.GoodsState])
		{
			return true;
		}
		else if (SortKey[data1.GoodsState] == SortKey[data2.GoodsState])
		{
			float Data1Discount = data1.DiscountPrice > 0 ? (data1.DiscountPrice / (float)data1.Price) : 1.0;
			float Data2Discount = data2.DiscountPrice > 0 ? (data2.DiscountPrice / (float)data2.Price) : 1.0;
			if (Data1Discount < Data2Discount)
			{
				return true;
			}
			else
			{
				return false;
			}

		}
		else
		{
			return false;
		}				
	});
	
	return GoodsList;
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::SortStoreAppearanceGoods(TArray<FSTORE_GOODS_DATA_TABLE> GoodsList)
{
	TArray<FSTORE_GOODS_DATA_TABLE> NoHasGoods;
	TArray<FSTORE_GOODS_DATA_TABLE> HasGoods;
	for (auto i : GoodsList)
	{
		if (HasStoreAppearances.Contains(i.ItemID))
		{
			HasGoods.Add(i);
		} else {
			NoHasGoods.Add(i);
		}
	}
	HasGoods.Sort([this](const FSTORE_GOODS_DATA_TABLE data1, const FSTORE_GOODS_DATA_TABLE data2)
		{
			if (HasStoreAppearances.Contains(data1.ItemID) && HasStoreAppearances.Contains(data2.ItemID))
			{
				FCS3ItemData Item1Data = UItemFactory::GetStaticDataByItemID(data1.ItemID);
				FCS3ItemData Item2Data = UItemFactory::GetStaticDataByItemID(data2.ItemID);
				FString LimitTime1 = Item1Data.LimitTime;
				FString LimitTime2 = Item2Data.LimitTime;
				if (LimitTime1 != "" && LimitTime2 != "")
				{
					if (IsItemAppearacesExpired(data1.ItemID) && !IsItemAppearacesExpired(data1.ItemID))
					{
						return true;
					}
					else
					{
						return false;
					}
					return true;
				}
				return true;
			}
			return true;
		});
	TArray<FSTORE_GOODS_DATA_TABLE> Goods = SortStoreGoods(NoHasGoods);
	Goods.Append(HasGoods);
	return Goods;
}

void URoleStoreInterface::OnUpdateRecommentGoods(const TArray<FSTORE_GOODS_DATA_TABLE> goodsList)
{
	for (auto goods : goodsList)
	{
		if (HomeRecommentGoodsIDs.Contains(goods.ID))
		{
			HomeRecommentGoods.Add(goods);
		}
		if (RecommentGoodsIDs.Contains(goods.ID))
		{
			if (!RecommentGoods.Contains(goods.ItemType))
			{
				TArray<FSTORE_GOODS_DATA_TABLE> Temp;
				RecommentGoods.Add(goods.ItemType, Temp);
			}
			RecommentGoods[goods.ItemType].Add(goods);
			if (goods.GoodsState == (int32)STORE_GOODS_STATE::STORE_GOODS_STATE_NEW_PRODUCT)
			{
				RecommentNewGoods.Add(goods);
			}
		}
		StoreGoodsDatas.Add(goods.ID, goods);
	}
}

void URoleStoreInterface::RPC_UpdateRecommentGoods()
{
	if (HomeRecommentGoods.Num() > 0)
	{
		return;
	}

	TArray<int32> GoodsIDList;
	for (auto i : HomeRecommentGoodsIDs)
	{
		GoodsIDList.Add(i);
	}
	for (auto i : RecommentGoodsIDs)
	{
		if (!GoodsIDList.Contains(i))
		{
			GoodsIDList.Add(i);
		}
	}

	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_RequestBuyStoreGoods no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(GoodsIDList));
	entity->BaseCall(TEXT("getRecommentGoods"), args);

}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetStoreGoodsByType(const int32& GoodsType, const int32& ItemType)
{
	TArray<FSTORE_GOODS_DATA_TABLE> Goods;
	if (StoreGoodsListDatas.Contains(GoodsType))
	{
		if (StoreGoodsListDatas[GoodsType].Contains(ItemType))
		{
			return StoreGoodsListDatas[GoodsType][ItemType];
		}
	}
	return Goods;
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetStoreGoodsByLable(const int & GoodType, const int32 & ItemType, const int32 & ThirdLable)
{
	TArray<FSTORE_GOODS_DATA_TABLE> Goods;
	for (auto i : StoreGoodsDatas)
	{
		FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(i.Value.ItemID);
		if (!ItemData.Param3.IsEmpty() && HasStoreAppearances.Contains(FSTRING_TO_INT(ItemData.Param3)))
		{
			continue;
		}
		///0代表全部
		if (ItemType == 0)
		{
			if (i.Value.GoodsType == GoodType)
			{
				Goods.Add(i.Value);
			}
		} else if(ThirdLable == 0){
			if (i.Value.GoodsType == GoodType && i.Value.ItemType == ItemType)
			{
				Goods.Add(i.Value);
			}
		} else {
			if (i.Value.GoodsType == GoodType && i.Value.ItemType == ItemType && i.Value.ThirdLable == ThirdLable)
			{
				Goods.Add(i.Value);
			}
		}

	}
	TArray<FSTORE_GOODS_DATA_TABLE> GoodsTemp = SortStoreGoods(Goods);

	return GoodsTemp;
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetStoreAppearancesByLable(const int & GoodType, const int32 & ItemType, const int32 & ThirdLable)
{
	TArray<FSTORE_GOODS_DATA_TABLE> Goods;
	for (auto i : StoreAppearancesDatas)
	{
		FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(i.Value.ItemID);
		if (!ItemData.Param3.IsEmpty() && HasStoreAppearances.Contains(FSTRING_TO_INT(ItemData.Param3)))
		{
			continue;
		}
		KBEngine::Entity* entity = GetEntity();
		if (entity != nullptr)
		{
			int32 Gender = (int32)entity->GetDefinedProperty(TEXT("gender"));
			if (ItemData.ReqGender != 0 && Gender != ItemData.ReqGender)
			{
				continue;
			}
		}
		///0代表全部
		if (ItemType == 0)
		{
			if (i.Value.GoodsType == GoodType)
			{
				Goods.Add(i.Value);
			}
		}
		else if (ThirdLable == 0) {
			if (i.Value.GoodsType == GoodType && i.Value.ItemType == ItemType)
			{
				Goods.Add(i.Value);
			}
		}
		else {
			if (i.Value.GoodsType == GoodType && i.Value.ItemType == ItemType && i.Value.ThirdLable == ThirdLable)
			{
				Goods.Add(i.Value);
			}
		}
	}
	TArray<FSTORE_GOODS_DATA_TABLE> GoodsTemp = SortStoreAppearanceGoods(Goods);
	return GoodsTemp;
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetStoreNewGoods(const int32& GoodsType)
{
	TArray<FSTORE_GOODS_DATA_TABLE> Goods;
	for (auto i : StoreGoodsDatas)
	{
		if (i.Value.GoodsType == GoodsType && i.Value.GoodsState == (int32)STORE_GOODS_STATE::STORE_GOODS_STATE_NEW_PRODUCT)
		{
			Goods.Add(i.Value);
		}
	}
	return Goods;
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetStoreRecommentNewGoods()
{
	return RecommentNewGoods;
}

void URoleStoreInterface::OnUpdateStoreNewGoods(const TArray<FSTORE_GOODS_DATA_TABLE> goodsList)
{
	for (auto goods : goodsList)
	{
		StoreGoodsDatas.Add(goods.ID, goods);
	}
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetStoreRecommentGoodsByType(int32 ItemType)
{
	TArray<FSTORE_GOODS_DATA_TABLE> Goods;
	if (RecommentGoods.Contains(ItemType))
	{
		return RecommentGoods[ItemType];
	}
	return Goods;
}

FSTORE_GOODS_DATA_TABLE URoleStoreInterface::GetStoreGoodsByID(const int32& GoodsID)
{
	if (StoreGoodsDatas.Contains(GoodsID))
		return StoreGoodsDatas[GoodsID];
	FSTORE_GOODS_DATA_TABLE temp;
	return temp;
}

bool URoleStoreInterface::IsValidStoreGoods(const int32& GoodsID)
{
	if (StoreGoodsDatas.Contains(GoodsID))
		return true;
	return false;
}

void URoleStoreInterface::RPC_openStoreUI(const int32& GoodsType, const int32& ItemType)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_BASE_requestOpenStoreUI no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(GoodsType);
	args.Add(ItemType);
	if (ConfigTime.Contains(GoodsType) && ConfigTime[GoodsType].Contains(ItemType))
	{
		args.Add(ConfigTime[GoodsType][ItemType]);
	}
	else {

		args.Add(TEXT(""));
	}
	entity->BaseCall(TEXT("requestOpenStoreUI"), args);

}

void URoleStoreInterface::SetBuyRecords(TArray <FSTORE_BUY_RECORD_DATA> Records)
{
	for (auto Record : Records)
	{
		BuyRecords.Add(Record.uid, Record);
	}

}

TArray<FSTORE_BUY_RECORD_DATA> URoleStoreInterface::GetBuyRecords()
{
	TArray<FSTORE_BUY_RECORD_DATA> Temp;
	for (auto BuyRecord : BuyRecords)
	{
		Temp.Add(BuyRecord.Value);
	}
	Temp.Sort([this](const FSTORE_BUY_RECORD_DATA data1, const FSTORE_BUY_RECORD_DATA data2)
	{
		return FSTRING_TO_INT64(data1.buyTime) > FSTRING_TO_INT64(data2.buyTime);
	});
	return Temp;
}

void URoleStoreInterface::DeleteBuyRecord(const FString& UID)
{
	if (BuyRecords.Contains(UID))
	{
		BuyRecords.Remove(UID);
	}
}

void URoleStoreInterface::DeleteBuyRecords()
{
	BuyRecords.Empty();
}

void URoleStoreInterface::SetPresentRecords(TArray <FSTORE_PRESENT_RECORD_DATA> Records)
{
	for (auto Record : Records)
	{
		PresendRecords.Add(Record.uid, Record);
	}
}

TArray<FSTORE_PRESENT_RECORD_DATA> URoleStoreInterface::GetPresentRecords()
{
	TArray<FSTORE_PRESENT_RECORD_DATA> Temp;
	for (auto PresendRecord : PresendRecords)
	{
		Temp.Add(PresendRecord.Value);
	}
	Temp.Sort([this](const FSTORE_PRESENT_RECORD_DATA data1, const FSTORE_PRESENT_RECORD_DATA data2)
	{
		return FSTRING_TO_INT64(data1.buyTime) > FSTRING_TO_INT64(data2.buyTime);
	});
	return Temp;
}

void URoleStoreInterface::DeletePresentRecord(const FString& UID)
{
	if (PresendRecords.Contains(UID))
	{
		PresendRecords.Remove(UID);
	}
}

void URoleStoreInterface::DeletePresentRecords()
{
	PresendRecords.Empty();
}

void URoleStoreInterface::OnStoreBuyComplete()
{
	UBaseWindow* SettlementWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("AppearanceSettlement"));
	if (IsValid(SettlementWindow))
	{
		///<关闭界面
		SettlementWindow->Hide();
	}
}

void URoleStoreInterface::OnRequestPresentGift(FSTORE_GIFT_BOX SenderGift)
{
	SenderGiftBox.Add(SenderGift.uid, SenderGift);
}

void URoleStoreInterface::OnRequestOpenGiftBox(TArray <FSTORE_GIFT_BOX> SenderGiftList, TArray <FSTORE_GIFT_BOX> ReceiverGiftList)
{
	for (auto SenderGift : SenderGiftList)
	{
		SenderGiftBox.Add(SenderGift.uid, SenderGift);
	}
	for (auto ReceiverGift : ReceiverGiftList)
	{
		ReceiverGiftBox.Add(ReceiverGift.uid, ReceiverGift);
	}
}

TArray<FSTORE_GIFT_BOX> URoleStoreInterface::GetSenderGiftBox()
{
	TArray<FSTORE_GIFT_BOX> temp;
	for (auto i : SenderGiftBox)
	{
		temp.Add(i.Value);
	}
	temp.Sort([this](const FSTORE_GIFT_BOX data1, const FSTORE_GIFT_BOX data2)
	{
		return FSTRING_TO_INT64(data1.overtime) > FSTRING_TO_INT64(data2.overtime);
	});
	return temp;
}

void URoleStoreInterface::DeleteSenderGiftBox(const FString& UID)
{
	if (SenderGiftBox.Contains(UID))
	{
		SenderGiftBox.Remove(UID);
	}
}

void URoleStoreInterface::DeleteSenderGiftBoxs()
{
	TArray<FString> RemoveList;
	for (auto i : SenderGiftBox)
	{
		if (!i.Value.endTime.IsEmpty())
		{
			RemoveList.Add(i.Key);
		}
	}
	for (auto i : RemoveList)
	{
		SenderGiftBox.Remove(i);
	}
}

TArray<FSTORE_GIFT_BOX> URoleStoreInterface::GetReceiverGiftBox()
{
	TArray<FSTORE_GIFT_BOX> temp;
	for (auto i : ReceiverGiftBox)
	{
		temp.Add(i.Value);
	}
	temp.Sort([this](const FSTORE_GIFT_BOX data1, const FSTORE_GIFT_BOX data2)
	{
		return FSTRING_TO_INT64(data1.overtime) > FSTRING_TO_INT64(data2.overtime);
	});
	return temp;
}

void URoleStoreInterface::DeleteReceiverGiftBox(const FString& UID)
{
	if (ReceiverGiftBox.Contains(UID))
	{
		ReceiverGiftBox.Remove(UID);
	}
}

void URoleStoreInterface::DeleteReceiverGiftBoxs()
{
	TArray<FString> RemoveList;
	for (auto i : ReceiverGiftBox)
	{
		if (!i.Value.endTime.IsEmpty())
		{
			RemoveList.Add(i.Key);
		}
	}
	for (auto i : RemoveList)
	{
		ReceiverGiftBox.Remove(i);
	}
}

void URoleStoreInterface::InitRemommentConfigData()
{
	HomeRecommentGoodsIDs.Empty();
	RecommentGoodsIDs.Empty();
	const UConfigTable* RemommentConfigDataTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MALL_RECOMMENT_DATA);
	for (auto RowName : RemommentConfigDataTable->GetRowNames())
	{
		const FSTORE_RECOMMENT_GOODS_DATA* ConfigData = RemommentConfigDataTable->GetRow<FSTORE_RECOMMENT_GOODS_DATA>(RowName);
		if (ConfigData)
		{
			if (ConfigData->IsHome)
			{
				HomeRecommentGoodsIDs.Add(ConfigData->ID);
			}
			if (ConfigData->IsRecomment)
			{
				RecommentGoodsIDs.Add(ConfigData->ID);
			}
		}
	}
}

void URoleStoreInterface::InitStoreConfigData()
{
	StoreGoodsDatas.Empty();
	const UConfigTable* StoreConfigDataTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STORE_GOODS_DATA);
	for (auto RowName : StoreConfigDataTable->GetRowNames())
	{
		const FSTORE_GOODS_DATA_TABLE* ConfigData = StoreConfigDataTable->GetRow<FSTORE_GOODS_DATA_TABLE>(RowName);
		if (ConfigData)
		{
			StoreGoodsDatas.Add(ConfigData->ID,*ConfigData);
		}
	}
	StoreAppearancesDatas.Empty();
	const UConfigTable* StoreAppearancesConfigDataTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STORE_APPEARANCE_DATA);
	for (auto RowName : StoreAppearancesConfigDataTable->GetRowNames())
	{
		const FSTORE_GOODS_DATA_TABLE* ConfigData = StoreAppearancesConfigDataTable->GetRow<FSTORE_GOODS_DATA_TABLE>(RowName);
		if (ConfigData)
		{
			StoreAppearancesDatas.Add(ConfigData->ID, *ConfigData);
		}
	}
}

void URoleStoreInterface::InitStoreSearchConfigData()
{
	StoreSearchConfigDatas.Empty();
	const UConfigTable* StoreSearchConfigDataTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MALL_GOODS_DATA);
	for (auto RowName : StoreSearchConfigDataTable->GetRowNames())
	{
		const FSTORE_SEARCH_DATA* ConfigData = StoreSearchConfigDataTable->GetRow<FSTORE_SEARCH_DATA>(RowName);
		if (ConfigData)
		{
			StoreSearchConfigDatas.Add(*ConfigData);
		}
	}

}

int32 URoleStoreInterface::GetNoStateGiftBoxAmount()
{
	int32 Amount = 0;
	for (auto i : ReceiverGiftBox)
	{
		if (i.Value.giftState == (int32)STORE_GIFT_STATE::STORE_GIFT_STATE_NONE)
		{
			++Amount;
		}
	}
	return Amount;
}

int32 URoleStoreInterface::GetRebate(const int32& Price, const int32& GoodsID)
{
	if (GoodsID == 0) return Price;
	FSTORE_GOODS_DATA_TABLE goods = GetStoreGoodsByID(GoodsID);
	return (int)(goods.RebateRate * Price);
}

TArray<FSTORE_GOODS_DATA_TABLE> URoleStoreInterface::GetSearchGoodsList(const FString& SearchString)
{
	TArray<FSTORE_GOODS_DATA_TABLE> GoodsArray;
	for (TPair<int32, FSTORE_GOODS_DATA_TABLE> Data : StoreGoodsDatas)
	{
		FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(Data.Value.ItemID);
		if (ItemData.ItemName.Contains(SearchString))
		{
			GoodsArray.Add(Data.Value);
		}
	}
	return GoodsArray;
}

void URoleStoreInterface::ClearAllData()
{
	HomeRecommentGoods.Empty();
	ConfigTime.Empty();
	StoreGoodsListDatas.Empty();
	StoreGoodsDatas.Empty();
	BuyRecords.Empty();
	PresendRecords.Empty();
	SenderGiftBox.Empty();
	ReceiverGiftBox.Empty();
	HomeRecommentGoodsIDs.Empty();
	RecommentGoodsIDs.Empty();
	RecommentGoods.Empty();
	RecommentNewGoods.Empty();
	NewGoodsConfigTime.Empty();
	StoreCart.Empty();
}

void URoleStoreInterface::CLINET_GiftBoxShowRedPoint_Implementation(const int32& Type)
{

}

void URoleStoreInterface::RPC_OnShowGiftBoxRedPoint(const int32& Type)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleStoreInterface::RPC_OnShowGiftBoxRedPoint no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(Type);
	entity->BaseCall(TEXT("onShowGiftBoxRedPoint"), args);
}

CONTROL_COMPILE_OPTIMIZE_END