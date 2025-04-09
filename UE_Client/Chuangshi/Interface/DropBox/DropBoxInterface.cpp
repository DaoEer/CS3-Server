// Fill out your copyright notice in the Description page of Project Settings.


#include "DropBoxInterface.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Kismet/KismetMathLibrary.h"
#include "Util/ConvertUtil.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/Item/ItemFactory.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UDropBoxInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UDropBoxInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UDropBoxInterface::UDropBoxInterface()
{

}

UDropBoxInterface::~UDropBoxInterface()
{

}

void UDropBoxInterface::ClearPickUpItemList()
{
	FPK_ItemList.Empty();
}

bool UDropBoxInterface::HasUIdInItemList(const FString& UId)
{
	for (auto item : FPK_ItemList)
	{
		if (UId == item->UID)
		{
			return true;
		}
	}
	return false;
}

void UDropBoxInterface::UpdateItemList(const FString& UId, int32 LeftAmount)
{
	for (auto item : FPK_ItemList)
	{
		if (UId == item->UID)
		{
			if (LeftAmount == 0)
			{
				FPK_ItemList.Remove(item);
			}
			else if (item->Amount != LeftAmount)
			{
				item->Amount = LeftAmount;
			}
			break;
		}
	}
}

void UDropBoxInterface::InitBlueCB()
{
	ArrBlueFunc.Add("updateDropBoxModelVisible");
	Supper::InitBlueCB();
}

