// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleFacadeBagInterface.h"
#include "Util/CS3Debug.h"
#include "GameData/Item/ItemFactory.h"
#include "Json.h"
#include "JsonFieldData.h"
#include"Chuangshi.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleFacadeBagInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleFacadeBagInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleFacadeBagInterface::URoleFacadeBagInterface()
{

}

URoleFacadeBagInterface::~URoleFacadeBagInterface()
{

}
/*
void URoleFacadeBagInterface::ReceiveFacadeBagItem(const FString& data)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("data = %s"), *data);
	int32 itemid;
	int32 itemorder;
	int32 amount;
	int32 bindtype;
	FString uid;
	int32 itemType;
	GetItemInfoByString(data, itemid, itemorder, amount, bindtype, uid,itemType);
	UItemBase* item = UItemFactory::GetItemByID(itemid);
	if (!IsValid(item) || item->ItemID == 0)
	{
		CS3_Warning(TEXT("add item by itemid[%d] failed!"), itemid);
		return;
	}
	item->UID = uid;
	item->Amount = amount;
	item->BindType = bindtype;
	item->ItemOrder = itemorder;
	TMap<FString, UItemBase*> value;
	value.Add("uid", item);
	//FFB_ItemList.Add()
}
*/
void URoleFacadeBagInterface::GetItemInfoByString(const FString& jsonstr, int32& itemid, int32& itemorder, int32& amount, int32& bindtype, FString& uid,int32& itemType )
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
		itemType = FSTRING_TO_INT(item->GetString(TEXT("itemType")));
	}
}

void URoleFacadeBagInterface::InitBlueCB()
{
	//ArrBlueFunc.Add("ReceiveFacadeBagItem");
	Supper::InitBlueCB();
}
