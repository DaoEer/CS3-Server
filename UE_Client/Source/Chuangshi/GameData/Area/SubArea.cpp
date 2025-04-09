// Fill out your copyright notice in the Description page of Project Settings.


#include "SubArea.h"
#include "Interface/CombatInterface.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/GameObject.h"

USubArea::USubArea()
{
}

USubArea::~USubArea()
{
}

void USubArea::InitDatas(FAREA_DATA* AreaRow)
{
	UBaseArea::InitDatas(AreaRow);
	if (AreaRow->Param1 != "")
	{
		AreaPvpRule = FSTRING_TO_INT(AreaRow->Param1);
	}
}

void USubArea::OnEnter(const FString SpaceScriptID)
{
	//UGolbalBPFunctionLibrary::StatusMessage(105, AreaName); //聊天框提示
	//UGolbalBPFunctionLibrary::StatusMessage(107, AreaName);	//屏幕中央提示
	if (AreaPvpRule != 0)
	{
		UCombatInterface * CombatInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.CombatInterface : nullptr;
		if (CombatInterface)
		{
			CombatInterface->RPC_setAreaRelationRuleFC(INT_TO_FSTRING(AreaPvpRule));
		}
	}
}

void USubArea::OnLeave(const FString SpaceScriptID)
{
	if (AreaPvpRule != 0)
	{
		UCombatInterface * CombatInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.CombatInterface : nullptr;
		if (CombatInterface)
		{
			CombatInterface->RPC_setAreaRelationRuleFC(INT_TO_FSTRING(0));
		}
	}
}
