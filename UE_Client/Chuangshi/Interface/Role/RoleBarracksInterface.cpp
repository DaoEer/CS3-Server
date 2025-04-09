// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleBarracksInterface.h"
#include "../../Util/CS3Debug.h"
#include "KBEngine.h"
#include "Entity/Alias.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "GameData/EnumCsvDefine.h"
#include "Util/ConvertUtil.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(URoleBarracksInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitRoleBarracksDatas, &URoleBarracksInterface::InitRoleBarracksDatas, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddRoleBarracksData, &URoleBarracksInterface::AddRoleBarracksData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitRoleArmyDatas, &URoleBarracksInterface::InitRoleArmyDatas, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(SaveArmyDataCB, &URoleBarracksInterface::SaveArmyDataCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnUpdateGuardSoldierSkill, &URoleBarracksInterface::OnUpdateGuardSoldierSkill,const FString&, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitBarracksByOccupyTrainGround, &URoleBarracksInterface::InitBarracksByOccupyTrainGround, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitBarracksByOccupyTrainGroundOver, &URoleBarracksInterface::InitBarracksByOccupyTrainGroundOver, const int32&, const int32&, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleBarracksInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(isCanOpenBarracks, &URoleBarracksInterface::Set_isCanOpenBarracks, uint8)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleBarracksInterface::URoleBarracksInterface()
{

}

URoleBarracksInterface::~URoleBarracksInterface()
{

}

void URoleBarracksInterface::RequestOpenBarracks()
{
	ClearRoleBarracksData();
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::RequestOpenBarracks : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("requestOpenBarracks"), args);
}

void URoleBarracksInterface::InitRoleBarracksDatas(const FVariant& Var)
{
	KBEngine::FVariantArray RoleBarrDatas = Var.GetValue<KBEngine::FVariantArray>();
	TArray<FROLEBARRACKSITEMDATA> RoleTempDatas = TArray<FROLEBARRACKSITEMDATA>();
	for (FVariant& data: RoleBarrDatas)
	{
		FBARRACKSSOLDIERDATA element1 = FBARRACKSSOLDIERDATA(data);
		FROLEBARRACKSITEMDATA temp;
		temp.Id = element1.id;
		temp.ScriptID = element1.scriptID;
		temp.Exp = element1.exp;
		temp.IsInArmy = element1.isInArmy!=0?true:false;
		temp.Level = element1.level;
		temp.MaxExp = element1.maxExp;
		for (auto skillData: element1.skillIDDatas)
		{
			FPASSIVESKILLDATA tempSkillData;
			tempSkillData.SkillID = skillData.skillID;
			tempSkillData.Exp = skillData.exp;
			tempSkillData.MaxExp = skillData.maxExp;
			temp.PassiveSkillDatas.Add(tempSkillData);
		}
		temp.SoldierType = ENUM_BARRACKS_SOLDIER_TYPE(element1.soldierType);
		temp.IsActive = element1.isActive;
		RoleTempDatas.Add(temp);
	}
	if (RoleTempDatas.Num() > 0)
	{
		if (RoleBarracksDatas.Contains(RoleTempDatas[0].ScriptID))
		{
			RoleBarracksDatas[RoleTempDatas[0].ScriptID].Append(RoleTempDatas);
		}
		else
		{
			RoleBarracksDatas.Add(RoleTempDatas[0].ScriptID, RoleTempDatas);
		}	
	}
}

void URoleBarracksInterface::AddRoleBarracksData(const FVariant& Var)
{
	FBARRACKSSOLDIERDATA tempData = FBARRACKSSOLDIERDATA(Var);
	FROLEBARRACKSITEMDATA temp;
	temp.Id = tempData.id;
	temp.ScriptID = tempData.scriptID;
	temp.Exp = tempData.exp;
	temp.IsInArmy = tempData.isInArmy != 0 ? true : false;
	temp.Level = tempData.level;
	temp.MaxExp = tempData.maxExp;
	temp.SoldierType = ENUM_BARRACKS_SOLDIER_TYPE(tempData.soldierType);
	temp.IsActive = tempData.isActive;
	for (auto skillData : tempData.skillIDDatas)
	{
		FPASSIVESKILLDATA tempSkillData;
		tempSkillData.SkillID = skillData.skillID;
		tempSkillData.Exp = skillData.exp;
		tempSkillData.MaxExp = skillData.maxExp;
		temp.PassiveSkillDatas.Add(tempSkillData);
	}
	if (RoleBarracksDatas.Contains(temp.ScriptID))
	{
		RoleBarracksDatas[temp.ScriptID].Add(temp);
	}
	else
	{
		TArray<FROLEBARRACKSITEMDATA> RoleTempDatas = TArray<FROLEBARRACKSITEMDATA>();
		RoleTempDatas.Add(temp);
		RoleBarracksDatas.Add(temp.ScriptID, RoleTempDatas);
	}
	OnAddRoleBarracksData(temp);
}

void URoleBarracksInterface::InitRoleBarracksDataOver_Implementation(const int32& soldierType)
{
	if (BarracksCfgDatas.Num() <= 0)
	{
		InitLoadBarracksCfgDatas(soldierType);
	}
	if (soldierType == int32(ENUM_BARRACKS_SOLDIER_TYPE::BARRACKS_SOLDIER_GUARD_TYPE))
	{
		InitLoadBarracksSoldierSkillCfgDatas();
	}
	InitBarracksReviveCostDatas();
}

void URoleBarracksInterface::InitLoadBarracksCfgDatas(const int32& soldierType)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BARRACKS_DATA);
		if (IsValid(ConfigTable))
		{
			TArray<FBARRACKS_TABLE_DATA*> BarracksDatas;
			ConfigTable->GetAllRows(BarracksDatas);
			for (auto data : BarracksDatas)
			{
				if (BarracksCfgDatas.Contains(data->SoldierType))
				{
					BarracksCfgDatas[data->SoldierType].Add(data->ScriptID, *data);
				}
				else
				{
					TMap<FString, FBARRACKS_TABLE_DATA> BarracksCfgDatasMap;
					BarracksCfgDatasMap.Add(data->ScriptID, *data);
					BarracksCfgDatas.Add(data->SoldierType, BarracksCfgDatasMap);
				}
			}
		}
	}
}

void URoleBarracksInterface::InitLoadBarracksSoldierSkillCfgDatas()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BARRACKS_SKILL_DATA);
		if (IsValid(ConfigTable))
		{
			TArray<FBARRACKS_GUARD_SOLDIER_SKILL_DATA*> BarracksSkillDatas;
			ConfigTable->GetAllRows(BarracksSkillDatas);
			for (auto data: BarracksSkillDatas)
			{
				if (BarracksSoldierSkillCfgData.Contains(data->ScriptID))
				{
					BarracksSoldierSkillCfgData[data->ScriptID].Add(data->CurrentSkillID, *data);
				}
				else
				{
					TMap<int32, FBARRACKS_GUARD_SOLDIER_SKILL_DATA> BarracksCfgSkillData;
					BarracksCfgSkillData.Add(data->CurrentSkillID, *data);
					BarracksSoldierSkillCfgData.Add(data->ScriptID, BarracksCfgSkillData);
				}
			}
		}
	}
}

void URoleBarracksInterface::InitBarracksReviveCostDatas()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BARRACKS_REVIVE_COST_DATA);
		if (IsValid(ConfigTable))
		{
			TArray<FBARRACKS_REVIVE_COST_DATA*> datas;
			ConfigTable->GetAllRows(datas);
			
			for (auto data : datas)
			{
				if (!BarracksReviveCostDatas.Contains(data->scriptID))
				{
					BarracksReviveCostDatas.Add((data->scriptID), {});
				}
				TMap<uint32, uint32> cost;
				for (auto it: data->item)
				{
					cost.Add(it.level, it.money);
				}
				
				BarracksReviveCostDatas[data->scriptID].Append(cost);
			}
		}
	}
}

void URoleBarracksInterface::InitRoleArmyDatas(const FVariant& Var)
{
	KBEngine::FVariantArray ArmyDatas = Var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& data : ArmyDatas )
	{
		FARMYDATA ArmyData = FARMYDATA(data);
		FROLEARMYDATA TempRoleArmyData;
		TempRoleArmyData.Id = ArmyData.id;
		TempRoleArmyData.BeBusy = ArmyData.controlArmyID;
		TempRoleArmyData.FirstGuardScriptID = ArmyData.firstGuardScriptID;
		TempRoleArmyData.SecondGuardScriptID = ArmyData.secondGuardScriptID;
		TempRoleArmyData.SoldierScriptID = ArmyData.soldierScriptID;
		TempRoleArmyData.SoldierIDs = ArmyData.soldierIDs;
		if (RoleArmyDatas.Contains(TempRoleArmyData.Id))
		{
			RoleArmyDatas.Remove(TempRoleArmyData.Id);
		}
		RoleArmyDatas.Add(TempRoleArmyData.Id, TempRoleArmyData);
	}
}

void URoleBarracksInterface::SaveArmyDataCB(const FVariant& Var)
{
	FARMYDATA ArmyData = FARMYDATA(Var);
	FROLEARMYDATA TempRoleArmyData;
	TempRoleArmyData.Id = ArmyData.id;
	TempRoleArmyData.BeBusy = ArmyData.controlArmyID;
	TempRoleArmyData.FirstGuardScriptID = ArmyData.firstGuardScriptID;
	TempRoleArmyData.SecondGuardScriptID = ArmyData.secondGuardScriptID;
	TempRoleArmyData.SoldierScriptID = ArmyData.soldierScriptID;
	TempRoleArmyData.SoldierIDs = ArmyData.soldierIDs;
	if (RoleArmyDatas.Contains(TempRoleArmyData.Id))
	{
		RoleArmyDatas.Remove(TempRoleArmyData.Id);
	}
	RoleArmyDatas.Add(TempRoleArmyData.Id, TempRoleArmyData);
	OnSaveArmyDataCB(TempRoleArmyData);
}

void URoleBarracksInterface::UpGradeGuardSoldierSkillLevel(const FString& scriptID, const int32& guardSoldierID, const int32& skillID, const int32& exp)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::UpGradeGuardSoldierSkillLevel : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(scriptID);
	args.Add(guardSoldierID);
	args.Add(skillID);
	args.Add(exp);
	GetEntity()->CellCall(TEXT("guardSoldierSkillUpLevel"), args);
}

void URoleBarracksInterface::OnUpdateGuardSoldierSkill(const FString& scriptID, const int32& soldierID, const int32& lastSkillID, const FVariant& Var)
{
	FSOLDIER_SPECIAL_SKILL_DATA SkillData = FSOLDIER_SPECIAL_SKILL_DATA(Var);
	FPASSIVESKILLDATA tempSkillData;
	tempSkillData.Exp = SkillData.exp;
	tempSkillData.MaxExp = SkillData.maxExp;
	tempSkillData.SkillID = SkillData.skillID;
	if (RoleBarracksDatas.Contains(scriptID))
	{
		for (auto& barracksItem : RoleBarracksDatas[scriptID])
		{
			if (barracksItem.Id == soldierID)
			{
				for (int32 i = 0; i < barracksItem.PassiveSkillDatas.Num(); ++i)
				{
					if (barracksItem.PassiveSkillDatas[i].SkillID == lastSkillID)
					{
						barracksItem.PassiveSkillDatas.RemoveAt(i);
						barracksItem.PassiveSkillDatas.Insert(tempSkillData, i);
						break;
					}
				}
				break;
			}
		}
	}
	OnUpdateGuardSoldierSkillBP(scriptID, soldierID,lastSkillID,tempSkillData);
}

void URoleBarracksInterface::InitRoleBarracksUnLockSoldiers_Implementation(const TArray<FString>& unLockSoldierScriptIDs)
{
	for (auto scriptID:unLockSoldierScriptIDs)
	{
		RoleUnLockSoldiers.AddUnique(scriptID);
	}
}

void URoleBarracksInterface::RemoveRoleBarracksData_Implementation(const FString& scriptID)
{
	if (RoleBarracksDatas.Contains(scriptID))
	{
		RoleBarracksDatas.Remove(scriptID);
	}
}

void URoleBarracksInterface::RemoveRoleBarracksSoldierData_Implementation(const FString& scriptID, const int32& soldierID)
{
	if (RoleBarracksDatas.Contains(scriptID))
	{
		for (auto barracksItem: RoleBarracksDatas[scriptID])
		{
			if (barracksItem.Id == soldierID)
			{
				RoleBarracksDatas[scriptID].Remove(barracksItem);
				break;
			}
		}
	}
}

void URoleBarracksInterface::UpdateSoldierLevelData_Implementation(const FString& scriptID, const int32& soldierID, const int32& level)
{
	if (RoleBarracksDatas.Contains(scriptID))
	{
		for (auto& barracksItem : RoleBarracksDatas[scriptID])
		{
			if (barracksItem.Id == soldierID)
			{
				barracksItem.Level = level;
				break;
			}
		}
	}
}

void URoleBarracksInterface::UpdateSoldierExpData_Implementation(const FString& scriptID, const int32& soldierID, const int32& exp, const int32& maxExp)
{
	if (RoleBarracksDatas.Contains(scriptID))
	{
		for (auto& barracksItem : RoleBarracksDatas[scriptID])
		{
			if (barracksItem.Id == soldierID)
			{
				barracksItem.Exp = exp;
				barracksItem.MaxExp = maxExp;
				break;
			}
		}
	}
}

void URoleBarracksInterface::UpdateSoldierIsInArmyData_Implementation(const FString& scriptID, const int32& soldierID, const int32& isInArmy)
{
	if (RoleBarracksDatas.Contains(scriptID))
	{
		for (auto& barracksItem : RoleBarracksDatas[scriptID])
		{
			if (barracksItem.Id == soldierID)
			{
				barracksItem.IsInArmy = isInArmy != 0 ? true : false;
				break;
			}
		}
	}
}

void URoleBarracksInterface::UpdateSoldierIsActive_Implementation(const FString& scriptID, const int32& soldierID, const int32& isActive)
{
	if (RoleBarracksDatas.Contains(scriptID))
	{
		for (auto& barracksItem : RoleBarracksDatas[scriptID])
		{
			if (barracksItem.Id == soldierID)
			{
				barracksItem.IsActive = (bool)isActive;
				break;
			}
		}
	}
}

void URoleBarracksInterface::RequestBuyBarracksSoldier(ENUM_BARRACKS_SOLDIER_TYPE soldierType, const FString& scriptID, const int32& count)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::RequestBuyBarracksSoldier : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(int(soldierType));
	args.Add(scriptID);
	args.Add(count);
	GetEntity()->CellCall(TEXT("requestBuyBarracksSoldier"), args);
}

void URoleBarracksInterface::RequestRevive(const FString& scriptID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::RequestBuyBarracksSoldier : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(scriptID);
	GetEntity()->CellCall(TEXT("requestReviveGuard"), args);
}

int32 URoleBarracksInterface::GetReviveCost(const FString & scriptID, int32 level)
{
	if (BarracksReviveCostDatas.Contains(scriptID) && BarracksReviveCostDatas[scriptID].Contains(level))
	{
		return BarracksReviveCostDatas[scriptID][level];
	}
	return -1;
}


void URoleBarracksInterface::DivideExpToSoldiers(ENUM_BARRACKS_SOLDIER_TYPE soldierType, const FString& scriptID, const int32& exp)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::DivideExpToSoldiers : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(int(soldierType));
	args.Add(scriptID);
	args.Add(exp);
	GetEntity()->CellCall(TEXT("divideExpToSoldiers"), args);
}

void URoleBarracksInterface::SaveArmyData(const int32& id, const FString& firstGuardScriptID, const FString& secondGuardScriptID, const FString& soldierScriptID, const TArray<int32>& soldierIDs)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::SaveArmyData : GetEntity()!"));
		return;
	}
	FARMYDATA tempArmyData;
	tempArmyData.id = id;
	tempArmyData.controlArmyID = 0;
	tempArmyData.firstGuardScriptID = firstGuardScriptID;
	tempArmyData.secondGuardScriptID = secondGuardScriptID;
	tempArmyData.soldierScriptID = soldierScriptID;
	tempArmyData.soldierIDs = soldierIDs;
	KBEngine::FVariantArray args;
	KBEngine::FVariantMap armyMap;
	tempArmyData.ToFVariantMap(armyMap);
	args.Add(FVariant(armyMap));
	GetEntity()->CellCall(TEXT("saveArmyData"), args);
}

TArray<FROLEBARRACKSITEMDATA> URoleBarracksInterface::GetRoleRarracksDatasByScriptID(const FString& scriptID)
{
	if (RoleBarracksDatas.Contains(scriptID))
	{
		return RoleBarracksDatas[scriptID];
	}
	TArray<FROLEBARRACKSITEMDATA> tempData;
	return tempData;
}

FBARRACKS_TABLE_DATA URoleBarracksInterface::GetRarracksCfgDatasByScriptID(const ENUM_BARRACKS_SOLDIER_TYPE soldierType, const FString& scriptID)
{
	if (BarracksCfgDatas.Contains(soldierType) && BarracksCfgDatas[soldierType].Contains(scriptID))
	{
		return BarracksCfgDatas[soldierType][scriptID];
	}
	FBARRACKS_TABLE_DATA tempData;
	return tempData;
}

TArray<FBARRACKS_TABLE_DATA> URoleBarracksInterface::GetRarracksCfgDatasBySoldierType(const ENUM_BARRACKS_SOLDIER_TYPE soldierType)
{
	TArray<FBARRACKS_TABLE_DATA> tempData;
	if (BarracksCfgDatas.Contains(soldierType))
	{
		for ( auto It = BarracksCfgDatas[soldierType].CreateIterator();It;++It)
		{
			tempData.Add(It.Value());
		}
	}
	return tempData;
}

FROLEARMYDATA URoleBarracksInterface::GetRoleArmyDatasByID(const int32& id)
{
	if (RoleArmyDatas.Contains(id))
	{
		return RoleArmyDatas[id];
	}
	FROLEARMYDATA tempArmyData;
	return tempArmyData;
}

TArray<FROLEBARRACKSITEMDATA> URoleBarracksInterface::GetRoleRarracksDatasBySoldierType(const ENUM_BARRACKS_SOLDIER_TYPE soldierType, const TArray<FString>& removeScriptIDs)
{
	TArray<FROLEBARRACKSITEMDATA> tempRoleBarracksDatas;
	for (auto It = RoleBarracksDatas.CreateIterator(); It; ++It)
	{
		if (soldierType == ENUM_BARRACKS_SOLDIER_TYPE::BARRACKS_SOLDIER_COMMON_TYPE && removeScriptIDs.Contains(It.Key()))
		{
			if (It.Value().Num() > 0 && It.Value()[0].SoldierType == soldierType)
			{
				int32 num = GetArmySoldierNumByScriptID(It.Key());
				if ((It.Value().Num() - num) > 0)
				{
					tempRoleBarracksDatas.Add(It.Value()[0]);
				}
			}
		}
		if (!removeScriptIDs.Contains(It.Key()))
		{
			if (It.Value()[0].IsActive && It.Value().Num() > 0 && It.Value()[0].SoldierType == soldierType)
			{
				tempRoleBarracksDatas.Add(It.Value()[0]);
			}
		}
	}
	return tempRoleBarracksDatas;
}

FString URoleBarracksInterface::GetRoleBarracksExp()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::GetRoleBarracksExp : GetEntity()!"));
		return "";
	}
	int64 barrackExp = GetEntity()->GetDefinedProperty(TEXT("barracksExp")).GetValue<int64>();
	return INT64_TO_FSTRING(barrackExp);
}

TArray<FBARRACKS_GUARD_SOLDIER_SKILL_DATA> URoleBarracksInterface::GetGuardSoldierFirstLevelSkillCfgData(const FString& scriptID)
{
	TArray<FBARRACKS_GUARD_SOLDIER_SKILL_DATA> tempSkillDatas;
	if (BarracksSoldierSkillCfgData.Contains(scriptID))
	{
		for (auto It = BarracksSoldierSkillCfgData[scriptID].CreateIterator();It;++It)
		{
			if (It.Value().Level == 1)
			{
				tempSkillDatas.Add(It.Value());
			}
		}
	}
	tempSkillDatas.Sort([](const FBARRACKS_GUARD_SOLDIER_SKILL_DATA& tempSkillData1, const FBARRACKS_GUARD_SOLDIER_SKILL_DATA& tempSkillData2) {return tempSkillData1.CurrentSkillID < tempSkillData2.CurrentSkillID; });
	return tempSkillDatas;
}

FBARRACKS_GUARD_SOLDIER_SKILL_DATA URoleBarracksInterface::GetGuardSoldierSkillCfgDataBySkillID(const FString& scriptID, const int32& skillID)
{
	if (BarracksSoldierSkillCfgData.Contains(scriptID) && BarracksSoldierSkillCfgData[scriptID].Contains(skillID))
	{
		return BarracksSoldierSkillCfgData[scriptID][skillID];
	}
	FBARRACKS_GUARD_SOLDIER_SKILL_DATA tempSkillData;
	return tempSkillData;
}

void URoleBarracksInterface::OnRep_barracksExp()
{
	OnBarracksExpChange();
}

TArray<FROLEBARRACKSITEMDATA> URoleBarracksInterface::GetRoleRarracksDatasBySortLevel(const FString& scriptID, const TArray<int32>& removeSoldierIDs,const int32& count)
{
	TArray<FROLEBARRACKSITEMDATA> tempRoleBarracksDatas;
	if (RoleBarracksDatas.Contains(scriptID))
	{
		for (auto roleBarracksData:RoleBarracksDatas[scriptID])
		{
			tempRoleBarracksDatas.Add(roleBarracksData);
		}
		tempRoleBarracksDatas.Sort([](const FROLEBARRACKSITEMDATA& DataA, const FROLEBARRACKSITEMDATA& DataB)
		{
			return DataA.Level > DataB.Level;
		});
		TArray<FROLEBARRACKSITEMDATA> realRoleBarracksDatas;
		for (auto tempRoleBarracksData:tempRoleBarracksDatas)
		{
			if (!removeSoldierIDs.Contains(tempRoleBarracksData.Id))
			{
				realRoleBarracksDatas.Add(tempRoleBarracksData);
			}
		}
		if (realRoleBarracksDatas.Num() < count)
		{
			return realRoleBarracksDatas;
		}
		else
		{
			TArray<FROLEBARRACKSITEMDATA> returnRoleBarracksDatas;
			for (int32 index = 0; index < count; ++index)
			{
				returnRoleBarracksDatas.Add(realRoleBarracksDatas[index]);
			}
			return returnRoleBarracksDatas;
		}

	}
	return tempRoleBarracksDatas;
}

bool URoleBarracksInterface::CheckSoldierIsUnLock(const FString& scriptID)
{
	if (RoleUnLockSoldiers.Contains(scriptID))
	{
		return true;
	}
	return false;
}

void URoleBarracksInterface::DismissArmyData(const int32& armyID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::DismissArmyData : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(armyID);
	GetEntity()->CellCall(TEXT("dismissArmyData"), args);
}

void URoleBarracksInterface::CLIENT_OnDismissArmyData_Implementation(const int32& armyID)
{
	if (RoleArmyDatas.Contains(armyID))
	{
		RoleArmyDatas.Remove(armyID);
	}
}

void URoleBarracksInterface::OnArmyDoQuest(const int32 & armyID)
{
	if (RoleArmyDatas.Contains(armyID))
	{
		RoleArmyDatas[armyID].BeBusy = 1;
	}
}

void URoleBarracksInterface::OnArmyDoQuestConsume(const int32 & armyID, const int32 & num)
{
	if (RoleArmyDatas.Contains(armyID))
	{
		for (auto i = num - 1; i > 0; i--)
		{
			RoleArmyDatas[armyID].SoldierIDs.RemoveAt(i);			// 这里的移除不是很严谨，但是不影响功能
		}
	}
}

void URoleBarracksInterface::OnArmyFinishQuestAndBack(const int32 & armyID)
{
	if (RoleArmyDatas.Contains(armyID))
	{
		RoleArmyDatas[armyID].BeBusy = 0;
	}
}

void URoleBarracksInterface::onLeaveWorld()
{
	ClearRoleBarracksData();
	Supper::onLeaveWorld();
}

void URoleBarracksInterface::ClearRoleBarracksData()
{
	RoleBarracksDatas.Empty();
	RoleArmyDatas.Empty();
}

int32 URoleBarracksInterface::GetArmySoldierNumByScriptID(const FString& scriptID)
{
	int32 totalNum = 0;
	for (auto It = RoleArmyDatas.CreateIterator(); It; ++It)
	{
		if (It.Value().SoldierScriptID == scriptID)
		{
			totalNum += It.Value().SoldierIDs.Num();
		}
	}
	return totalNum;
}

void URoleBarracksInterface::EnterTrainSoldierGround()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::EnterTrainSoldierGround : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("enterTrainSoldierGround"), args);
}

void URoleBarracksInterface::Set_isCanOpenBarracks(const uint8& newVal, const uint8& oldVal)
{
	IsCanOpenBarracks = newVal > 0 ? true : false;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateIsCanOpenBarracks.Broadcast();
	}
}

bool URoleBarracksInterface::IsCanOpenRoleBarracks()
{
	return IsCanOpenBarracks;
}

void URoleBarracksInterface::InitBarracksByOccupyTrainGround(const FVariant& Var)
{
	KBEngine::FVariantArray RoleBarrDatas = Var.GetValue<KBEngine::FVariantArray>();
	TArray<FROLEBARRACKSITEMDATA> RoleTempDatas = TArray<FROLEBARRACKSITEMDATA>();
	for (FVariant& data : RoleBarrDatas)
	{
		FBARRACKSSOLDIERDATA element1 = FBARRACKSSOLDIERDATA(data);
		FROLEBARRACKSITEMDATA temp;
		temp.Id = element1.id;
		temp.ScriptID = element1.scriptID;
		temp.Exp = element1.exp;
		temp.IsInArmy = element1.isInArmy != 0 ? true : false;
		temp.Level = element1.level;
		temp.MaxExp = element1.maxExp;
		for (auto skillData : element1.skillIDDatas)
		{
			FPASSIVESKILLDATA tempSkillData;
			tempSkillData.SkillID = skillData.skillID;
			tempSkillData.Exp = skillData.exp;
			tempSkillData.MaxExp = skillData.maxExp;
			temp.PassiveSkillDatas.Add(tempSkillData);
		}
		temp.SoldierType = ENUM_BARRACKS_SOLDIER_TYPE(element1.soldierType);
		temp.IsActive = element1.isActive;
		RoleTempDatas.Add(temp);
	}
	if (RoleTempDatas.Num() > 0)
	{
		if (RoleBarracksDatas.Contains(RoleTempDatas[0].ScriptID))
		{
			RoleBarracksDatas[RoleTempDatas[0].ScriptID].Empty();
			RoleBarracksDatas[RoleTempDatas[0].ScriptID].Append(RoleTempDatas);
		}
		else
		{
			RoleBarracksDatas.Add(RoleTempDatas[0].ScriptID, RoleTempDatas);
		}
	}
}

void URoleBarracksInterface::InitBarracksByOccupyTrainGroundOver(const int32& npcID, const int32& requireSoldierAmount, const int32& requireSoldierLevel)
{
	InitLoadBarracksCfgDatas(int(ENUM_BARRACKS_SOLDIER_TYPE::BARRACKS_SOLDIER_COMMON_TYPE));
	OccupySoldierAmount = requireSoldierAmount;
	OccupySoldierLevel = requireSoldierLevel;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("SpecialBarracksWindow"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOpenSpecialBarracks.Broadcast();
	}
}

TArray<FString> URoleBarracksInterface::GetCanUseOccupySoldierScriptID()
{
	TArray<FString> soldierScriptIDs;
	TArray<FBARRACKS_TABLE_DATA> tempDatas = GetRarracksCfgDatasBySoldierType(ENUM_BARRACKS_SOLDIER_TYPE::BARRACKS_SOLDIER_COMMON_TYPE);
	for (auto tempData:tempDatas)
	{
		TArray<FROLEBARRACKSITEMDATA> soldiers = GetRoleRarracksDatasByScriptID(tempData.ScriptID);
		TArray<FROLEBARRACKSITEMDATA> tempSoldiers;
		for (auto soldier:soldiers )
		{
			if (soldier.Level >= OccupySoldierLevel)
			{
				tempSoldiers.Add(soldier);
			}
		}
		if (tempSoldiers.Num() >= OccupySoldierAmount)
		{
			soldierScriptIDs.Add(tempData.ScriptID);
		}
	}
	return soldierScriptIDs;
}

void URoleBarracksInterface::SureToOccupyTrainGround(const int32& npcID, const FString& soldierScriptID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::SureToOccupyTrainGround : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(npcID);
	args.Add(soldierScriptID);
	GetEntity()->CellCall(TEXT("sureToOccupyTrainGround"), args);
}

void URoleBarracksInterface::InitBlueCB()
{
	ArrBlueFunc.Add("InitRoleBarracksDatas");
	ArrBlueFunc.Add("InitRoleBarracksDataOver");
	ArrBlueFunc.Add("AddRoleBarracksData");
	ArrBlueFunc.Add("InitRoleArmyDatas");
	ArrBlueFunc.Add("RemoveRoleBarracksData");
	ArrBlueFunc.Add("SaveArmyDataCB");
	ArrBlueFunc.Add("RemoveRoleBarracksSoldierData");
	ArrBlueFunc.Add("UpdateSoldierLevelData");
	ArrBlueFunc.Add("UpdateSoldierExpData");
	ArrBlueFunc.Add("UpdateSoldierIsInArmyData");
	ArrBlueFunc.Add("InitRoleBarracksUnLockSoldiers");
	ArrBlueFunc.Add("CLIENT_OnDismissArmyData");
	ArrBlueFunc.Add("OnUpdateGuardSoldierSkill");
	ArrBlueFunc.Add("UpdateSoldierIsActive");
	ArrBlueFunc.Add("InitBarracksByOccupyTrainGround");
	Supper::InitBlueCB();
}
