// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleLingShiTradeInterface.h"
#include "Util/CS3Debug.h"
#include "CS3Base/CS3Entity.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"
#include "Json.h"
#include "JsonFieldData.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleLingShiTradeInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(GetAllOrderCB, &URoleLingShiTradeInterface::GetAllOrderCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddOrderCB, &URoleLingShiTradeInterface::AddOrderCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RefreshMyOrderCB, &URoleLingShiTradeInterface::RefreshMyOrderCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RefreshAllSellOrderCB, &URoleLingShiTradeInterface::RefreshAllSellOrderCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RefreshAllCollectOrder, &URoleLingShiTradeInterface::RefreshAllCollectOrder, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataMyOrderToClient, &URoleLingShiTradeInterface::UpdataMyOrderToClient, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataOrder, &URoleLingShiTradeInterface::UpdataOrder, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleLingShiTradeInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

CONTROL_COMPILE_OPTIMIZE_START
URoleLingShiTradeInterface::URoleLingShiTradeInterface()
{

}

URoleLingShiTradeInterface::~URoleLingShiTradeInterface()
{

}

void URoleLingShiTradeInterface::GetAllOrderCB(const FVariant& variant)
{
	FALL_ORDER_DATAS allOrederData = FALL_ORDER_DATAS(variant);
	TArray<FORDER_DATA> myOrderData = allOrederData.lingShiTradeOrder;
	TArray<FORDER_DATA> sellOrderData = allOrederData.allLingShiTradeSellOrder;
	TArray<FORDER_DATA> collectOrderData = allOrederData.allLingShiTradeCollectOrder;
	TradeTax = allOrederData.tax;
	InitLingShiTradeData(myOrderData);
	InitAllLingShiTradeSellOrder(sellOrderData);
	InitAllLingShiTradeCollectOrder(collectOrderData);
}
	


void URoleLingShiTradeInterface::AddOrderCB(const FVariant& variant)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AddOrderCB*********| %s |******* "), *data);
	FORDER_DATA tempData = FORDER_DATA( variant );
	FTradeOrderData tradeOrder = GetOrderFromJsonData(tempData);
	if (tradeOrder.Uid.Len() == 0 )
	{
		return;
	}
	LingShiTradeOrder.Add(tradeOrder);
	if (tradeOrder.TradeType == int(TRADETYPE::LINGSHI_TRADE_SELL))
	{
		AllLingShiTradeSellOrder.Add(tradeOrder);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AllLingShiTradeSellOrder*********| %d,%s |******* "), AllLingShiTradeSellOrder.Num(),*AllLingShiTradeSellOrder[0].Uid);
	}
	else if (tradeOrder.TradeType == int(TRADETYPE::LINGSHI_TRADE_COLLECT))
	{ 
		AllLingShiTradeCollectOrder.Add(tradeOrder);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AllLingShiTradeSellOrder*********| %d,%s |******* "), AllLingShiTradeCollectOrder.Num(), *AllLingShiTradeCollectOrder[0].Uid);
	}
	//通知界面增加订单
	OnAddMyOrder(tradeOrder);
	OnAddOrderOfAll(tradeOrder.TradeType, tradeOrder);
}

void URoleLingShiTradeInterface::UpdataMyOrderToClient(const FVariant& variant)
{
	FORDER_DATA tempData = FORDER_DATA(variant);
	FString uid = tempData.uid;
	FTradeOrderData tradeOrder = GetOrder(uid, LingShiTradeOrder);
	if (tradeOrder.Uid.Len() == 0)
	{
		return;
	}
	tradeOrder.Amount = tempData.amount;
	tradeOrder.RemainTime = FSTRING_TO_INT64(tempData.remainTime);
	tradeOrder.EarnMoney = tempData.earnMoney;
	//通知界面更新数据
	OnUpdataMyOrderToClient(tradeOrder);
}

void URoleLingShiTradeInterface::UpdataOrder(const FVariant& variant)
{
	FUPDATA_ORDER_DATA tempData = FUPDATA_ORDER_DATA(variant);
	FALL_TRADE_DATA tempTradData = tempData.allTradeData;
	FString uid = tempTradData.uid;
	int tradeType = tempTradData.tradeType;
	FTradeOrderData tradeOrder;
	if (tradeType == int(TRADETYPE::LINGSHI_TRADE_SELL))
	{
		tradeOrder = GetOrder(uid, AllLingShiTradeSellOrder);
	}
	else if (tradeType == int(TRADETYPE::LINGSHI_TRADE_COLLECT))
	{
		tradeOrder = GetOrder(uid, AllLingShiTradeCollectOrder);
	}
	if (tradeOrder.Uid.Len() == 0)
	{
		return;
	}
	tradeOrder.Amount = tempTradData.amount;
	tradeOrder.RemainTime = FSTRING_TO_INT64(tempTradData.remainTime);
	/// 通知界面更新
	OnUpdataOrderOfAllOrades(tradeType, tradeOrder);


	FLINGSHITRADE_SUCCESS_DATA tempSuccessTradeData = tempData.allTradeSuccess;
	FTradeSuccessData successData;
	successData.Uid = tempSuccessTradeData.uid;
	successData.Amount = tempSuccessTradeData.amount *100;
	successData.Price = tempSuccessTradeData.price;
	successData.TotalPrice = tempSuccessTradeData.amount * successData.Price;
	int succtradeType = tempSuccessTradeData.tradeType;
	if(succtradeType == int(TRADETYPE::LINGSHI_TRADE_SELL))
	{
		//新增的需要在前面，插入到0位置
		LingShiTradeSellSuccessData.Insert(successData, 0);
		//界面只显示50条，超过50条，后面的顶掉前面的
		if (LingShiTradeSellSuccessData.Num() > 50)
		{
			LingShiTradeSellSuccessData.RemoveAt(LingShiTradeSellSuccessData.Num() - 1);
		}
	}
	else if (succtradeType == int(TRADETYPE::LINGSHI_TRADE_COLLECT))
	{
		//新增的需要在前面，插入到0位置
		LingShiTradeCollectSuccessData.Insert(successData, 0);
		//界面只显示50条，超过50条，后面的顶掉前面的
		if (LingShiTradeCollectSuccessData.Num() > 50)
		{
			LingShiTradeCollectSuccessData.RemoveAt(LingShiTradeCollectSuccessData.Num() - 1);
		}
	}
	///通知界面更新
	OnUpdataSuccessOrder(succtradeType, successData);
}

void URoleLingShiTradeInterface::RemoveLingShiTradeOrderCB_Implementation(const FString& uid)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("RemoveLingShiTradeOrderCB*********| %s |******* "), *uid);
	FTradeOrderData tradeOrder = GetOrder(uid, LingShiTradeOrder);
	if ( tradeOrder.Uid.Len() == 0 )
	{
		return;
	}
	if (tradeOrder.TradeType == int(TRADETYPE::LINGSHI_TRADE_SELL))
	{
		FTradeOrderData sellOrder = GetOrder(uid, AllLingShiTradeSellOrder);
		if (sellOrder.Uid.Len() == 0)
		{
			LingShiTradeOrder.Remove(tradeOrder);
			OnRemoveMyLingShiTradeOrder(tradeOrder);
			return;
		}
		LingShiTradeOrder.Remove(tradeOrder);
		AllLingShiTradeSellOrder.Remove(sellOrder);
	}
	else if (tradeOrder.TradeType == int(TRADETYPE::LINGSHI_TRADE_COLLECT))
	{
		FTradeOrderData collectOrder = GetOrder(uid, AllLingShiTradeCollectOrder);
		if (collectOrder.Uid.Len() == 0)
		{
			LingShiTradeOrder.Remove(tradeOrder);
			OnRemoveMyLingShiTradeOrder(tradeOrder);
			return;
		}
		LingShiTradeOrder.Remove(tradeOrder);
		AllLingShiTradeCollectOrder.Remove(collectOrder);
	}
	OnRemoveMyLingShiTradeOrder(tradeOrder);
	OnRemoveAllLingShiTradeOrder(tradeOrder.TradeType, tradeOrder);
}

void URoleLingShiTradeInterface::RefreshMyOrderCB(const FVariant& variant)
{
	TSharedPtr<FJsonObject> jsonParsed;
	FORDER_DATAS orderDatas = FORDER_DATAS(variant);
	InitLingShiTradeData( orderDatas.orderData);
}

void URoleLingShiTradeInterface::RefreshAllSellOrderCB(const FVariant& variant)
{
	FORDER_DATAS orderDatas = FORDER_DATAS(variant);
	InitAllLingShiTradeSellOrder(orderDatas.orderData);
}

void URoleLingShiTradeInterface::RefreshAllCollectOrder(const FVariant& variant)
{
	FORDER_DATAS orderDatas = FORDER_DATAS(variant);
	InitAllLingShiTradeCollectOrder(orderDatas.orderData);	
}

FTradeOrderData URoleLingShiTradeInterface::GetOrder(FString uid , TArray<FTradeOrderData> orderArray)
{	
	FTradeOrderData tempOrder;
	for (auto order: orderArray)
	{
		if (order.Uid == uid)
		{
			return order;
		}
	}
	tempOrder.Uid = "";
	return tempOrder;
}

void URoleLingShiTradeInterface::InitLingShiTradeData(const TArray<FORDER_DATA>& orderData)
{
	LingShiTradeOrder.Empty();
	for (auto data: orderData)
	{
		FTradeOrderData tradeOrder = GetOrderFromJsonData(data);
		if (tradeOrder.Uid.Len() == 0)
		{
			continue;
		}
		LingShiTradeOrder.Add(tradeOrder);
	}
	OnInitMyLingShiTradeOrder();
}

void URoleLingShiTradeInterface::InitAllLingShiTradeSellOrder(const TArray<FORDER_DATA>& orderData)
{
	AllLingShiTradeSellOrder.Empty();
	for (auto data : orderData)
	{
		FTradeOrderData tradeOrder = GetOrderFromJsonData(data);
		if (tradeOrder.Uid.Len() == 0)
		{
			continue;
		}
		AllLingShiTradeSellOrder.Add(tradeOrder);
	}
	OnInitAllLingShiTradeSellOrder();
}

void URoleLingShiTradeInterface::InitAllLingShiTradeCollectOrder(const TArray<FORDER_DATA>& orderData)
{
	AllLingShiTradeCollectOrder.Empty();
	for (auto data : orderData)
	{
		FTradeOrderData tradeOrder = GetOrderFromJsonData(data);
		if (tradeOrder.Uid.Len() == 0)
		{
			continue;
		}
		AllLingShiTradeCollectOrder.Add(tradeOrder);
	}
	OnInitAllLingShiTradeCollectOrder();
}

FTradeOrderData URoleLingShiTradeInterface::GetOrderFromJsonData(const FORDER_DATA& data)
{
	FTradeOrderData tradeOrder;
	tradeOrder.Uid = data.uid;
	tradeOrder.Amount = data.amount;
	tradeOrder.Price = data.price;
	tradeOrder.EarnMoney = data.earnMoney;
	tradeOrder.RemainTime = FSTRING_TO_INT64(data.remainTime);
	tradeOrder.TradeType = data.tradeType;
	return tradeOrder;
}

void URoleLingShiTradeInterface::DealLinShiTradeOrder(int32 type, int32 amount, int32 totalPrice, FString uid)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::DealLinShiTradeOrder : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****DealLinShiTradeOrder*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::DealLinShiTradeOrder : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::DealLinShiTradeOrder : pEntity_Player||pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(amount);
	args.Add(totalPrice);
	args.Add(uid);
	if (type == int(TRADETYPE::LINGSHI_TRADE_SELL))
	{
		this->GetEntity()->CellCall(TEXT("buyLinShiTradeOrder"), args);
	}
	else if (type == int(TRADETYPE::LINGSHI_TRADE_COLLECT))
	{
		this->GetEntity()->CellCall(TEXT("sellLingShiTradeOrder"), args);
	}
}

void URoleLingShiTradeInterface::AddOrder(int type, int32 price, int32 amount)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::AddOrder : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****AddOrder*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::AddOrder : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::AddOrder : pEntity_Player||pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(price);
	args.Add(amount);
	if (type == int(TRADETYPE::LINGSHI_TRADE_SELL))
	{
		this->GetEntity()->CellCall(TEXT("addSellOrder"), args);
	}
	else if (type == int(TRADETYPE::LINGSHI_TRADE_COLLECT))
	{
		this->GetEntity()->CellCall(TEXT("addCollectOrder"), args);
	}
}

void URoleLingShiTradeInterface::SortOrdersByPrice(int TradeType, bool IsDescendingOrder)
{
	switch (TradeType)
	{
	case 0:
	{
		if (IsDescendingOrder)
		{
			AllLingShiTradeSellOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Price > DataB.Price;
			});
		}
		else
		{
			AllLingShiTradeSellOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Price < DataB.Price;
			});
		}
		break;
	}
	case 1:
	{
		if (IsDescendingOrder)
		{
			AllLingShiTradeCollectOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Price > DataB.Price;
			});
		}
		else
		{
			AllLingShiTradeCollectOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Price < DataB.Price;
			});
		}
		break;
	}
	default:
		break;
	}
}

void URoleLingShiTradeInterface::SortOrdersByAmount(int TradeType, bool IsDescendingOrder)
{
	switch (TradeType)
	{
	case 0:
	{
		if (IsDescendingOrder)
		{
			AllLingShiTradeSellOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Amount > DataB.Amount;
			});
		}
		else
		{
			AllLingShiTradeSellOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Amount < DataB.Amount;
			});
		}
		
		break;
	}
	case 1:
	{
		if (IsDescendingOrder)
		{
			AllLingShiTradeCollectOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Amount > DataB.Amount;
			});
		}
		else
		{
			AllLingShiTradeCollectOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.Amount < DataB.Amount;
			});
		}
		break;
	}
	default:
		break;
	}
}

void URoleLingShiTradeInterface::SortOrdersByRemainTime(int TradeType, bool IsDescendingOrder)
{
	switch (TradeType)
	{
	case 0:
	{
		if (IsDescendingOrder)
		{
			AllLingShiTradeSellOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.RemainTime > DataB.RemainTime;
			});
		}
		else
		{
			AllLingShiTradeSellOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.RemainTime < DataB.RemainTime;
			});
		}
		break;
	}
	case 1:
	{
		if (IsDescendingOrder)
		{
			AllLingShiTradeCollectOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.RemainTime > DataB.RemainTime;
			});
		}
		else
		{
			AllLingShiTradeCollectOrder.Sort([](const FTradeOrderData& DataA, const FTradeOrderData& DataB)
			{
				return DataA.RemainTime < DataB.RemainTime;
			});
		}
		break;
	}
	default:
		break;
	}
}

void URoleLingShiTradeInterface::RPC_removeLingShiTradeOrder(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::RPC_removeLingShiTradeOrder : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->BaseCall(TEXT("removeLingShiTradeOrder"), args);
}

void URoleLingShiTradeInterface::RPC_refreshMyOrder()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::RPC_refreshMyOrder : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->BaseCall(TEXT("refreshMyOrder"), args);
}

void URoleLingShiTradeInterface::RPC_requestGetOrder()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::RPC_requestGetOrder : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->BaseCall(TEXT("requestGetOrder"), args);
}

void URoleLingShiTradeInterface::RPC_refreshAllSellOrder()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::RPC_refreshAllSellOrder : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->BaseCall(TEXT("refreshAllSellOrder"), args);
}

void URoleLingShiTradeInterface::RPC_refreshAllCollectOrder()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::RPC_refreshAllCollectOrder : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->BaseCall(TEXT("refreshAllCollectOrder"), args);
}

void URoleLingShiTradeInterface::RPC_takeOutMoney()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLingShiTradeInterface::RPC_takeOutMoney : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("takeOutMoney"), args);
}

void URoleLingShiTradeInterface::InitBlueCB()
{
	ArrBlueFunc.Add("AddOrderCB");
	ArrBlueFunc.Add("UpdataMyOrderToClient");
	ArrBlueFunc.Add("UpdataOrder");
	ArrBlueFunc.Add("RemoveLingShiTradeOrderCB");
	ArrBlueFunc.Add("RefreshMyOrderCB");
	ArrBlueFunc.Add("RefreshAllSellOrderCB");
	ArrBlueFunc.Add("RefreshAllCollectOrder");
	ArrBlueFunc.Add("GetAllOrderCB");
	Supper::InitBlueCB();
}
CONTROL_COMPILE_OPTIMIZE_END