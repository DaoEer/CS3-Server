// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleReviveInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "Util/ConvertUtil.h"
#include "GameData/Area.h"
#include "Util/CS3Debug.h"
#include "Manager/Operation/OperationModeMgr.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleReviveInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleReviveInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
void URoleReviveInterface::Revive(REVIVE_TYPE reviveType)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleReviveInterface::Revive : GetEntity()!"));
		return;
	}
	FString	type = INT_TO_FSTRING(int(reviveType));
	
	KBEngine::FVariantArray Args;
	Args.Add(type);
	this->GetEntity()->CellCall(TEXT("CELL_revive"), Args);
}

void URoleReviveInterface::ReviveOnArea(FString reviveSpace, FString revivePosition, FString reviveDirection)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleReviveInterface::ReviveOnArea : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(reviveSpace);
	Args.Add(revivePosition);
	Args.Add(reviveDirection);
	this->GetEntity()->CellCall(TEXT("CELL_reviveOnArea"), Args);
}

void URoleReviveInterface::SetRevivePos()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleReviveInterface::SetRevivePos : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray Args;
	this->GetEntity()->CellCall(TEXT("CELL_setRevivePos"), Args);
}

void URoleReviveInterface::LoadReviveCostConfig()
{
	if (reviveCostDatas.Num() > 0) return;//加载过不需要再加载
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)) return;
	const UConfigTable* reviveCostTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_REVIVE_COST_DATA);
	if (reviveCostTable)
	{
		TArray<FROLE_REVIVE_COST_DATA*> tempReviveCostDatas;
		reviveCostTable->GetAllRows(tempReviveCostDatas);
		for (FROLE_REVIVE_COST_DATA* costData : tempReviveCostDatas)
		{
			if (!reviveCostDatas.Contains(costData->ReviveType))
			{
				TArray<FROLE_REVIVE_COST_DATA*> tempDatas;
				tempDatas.Emplace(costData);
				reviveCostDatas.Emplace(costData->ReviveType, tempDatas);
			}
			else
			{
				reviveCostDatas[costData->ReviveType].Emplace(costData);
			}
		}
	}
	//按复活次数从小到大排序
	for (auto reviveCostData : reviveCostDatas)
	{
		reviveCostData.Value.Sort([](const FROLE_REVIVE_COST_DATA& A, const FROLE_REVIVE_COST_DATA& B) {
			return A.ReviveNumber < B.ReviveNumber;});
	}
}

int32 URoleReviveInterface::GetReviveCostByOriginType(REVIVE_TYPE reviveType, int32 number)
{
	LoadReviveCostConfig();
	int32 tempReviveCost = 0;
	for (auto reviveCostData : reviveCostDatas)
	{
		if (reviveCostData.Key == reviveType)
		{
			TArray<FROLE_REVIVE_COST_DATA*> tempReviveCostDatas = reviveCostData.Value;
			bool isFind = false;
			for (FROLE_REVIVE_COST_DATA* costData : tempReviveCostDatas)
			{
				if (costData->ReviveNumber == number)
				{
					isFind = true;
					tempReviveCost = costData->ReviveCost;
					return tempReviveCost;
				}
			}
			if (!isFind)
			{
				//如果没找到就用最大的消耗
				tempReviveCost = tempReviveCostDatas.Last()->ReviveCost;
			}
			break;
		}
	}
	return tempReviveCost;
}

/*
void URoleReviveInterface::RequestRevive(const int32& reviveType)
{
	KBEngine::FVariantArray Args;
	Args.Add(reviveType);
	this->GetEntity()->CellCall(TEXT("revive"), Args);
}

*/


void URoleReviveInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnHideRevive");
	ArrBlueFunc.Add("CLIENT_SetRevivePosStatus");
	ArrBlueFunc.Add("NotifyReviveSpaceScriptID");
	Supper::InitBlueCB();
}

void URoleReviveInterface::CLIENT_OnHideRevive_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		if (IsValid(OperationModeMgr)&&OperationModeMgr->IsHaveMode(EATTACT_STATE::BEHAVIOR_TRAINSOLDIER))
		{
			return;//练兵场模式，摄像机视角不一样
		}
		else
		{
			PlayerActor->ResetCameraData();
		}
	}
}

void URoleReviveInterface::NotifyReviveSpaceScriptID_Implementation(const FString& spaceScriptID)
{
}

void URoleReviveInterface::CLIENT_SetRevivePosStatus_Implementation(int32 statusID, const FString& spaceScriptID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AREA_DATA);
	TArray<FAREA_DATA*> AreaDatas;
	ConfigTable->GetAllRows(AreaDatas);
	for (FAREA_DATA* cfg : AreaDatas)
	{
		if (cfg->ScriptID.Equals(spaceScriptID))
		{
			UGolbalBPFunctionLibrary::StatusMessage(statusID, cfg->AreaName);
			return;
		}
	}
	
}

void URoleReviveInterface::RPC_requestReviveSpaceScriptID(REVIVE_TYPE reviveType)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleReviveInterface::RPC_requestReviveSpaceScriptID : GetEntity()!"));
		return;
	}
	FString	type = INT_TO_FSTRING(int(reviveType));
	KBEngine::FVariantArray Args;
	Args.Add(type);
	this->GetEntity()->CellCall(TEXT("requestReviveSpaceScriptID"), Args);
}
