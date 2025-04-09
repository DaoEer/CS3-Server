
#include "SpaceEntityRelationMgr.h"
#include"Chuangshi.h"
#include "GameData/ConstDataBP.h"
#include "CfgManager.h"

USpaceEntityRelationMgr::USpaceEntityRelationMgr() 
{
}

USpaceEntityRelationMgr::~USpaceEntityRelationMgr() 
{
}

USpaceEntityRelationMgr* USpaceEntityRelationMgr::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<USpaceEntityRelationMgr>();
}

void USpaceEntityRelationMgr::InitDefaultEntityRelationIns()
{
	if (DefaultModeRelationMap.Num() != 0) return;	///只生成一次
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SPACE_ENTITY_RELATION);
	if (ConfigTable)
	{
		TArray<FSpaceEntityRelationTableData*> ConfigRows;
		ConfigTable->GetAllRows(ConfigRows);
		for (auto i : ConfigRows) 
		{
			if (i->RelationMode != "RelationDefault") continue;
			URelationBase* pIns = URelationInsFactory::CreateRelationInsByClass(i->RelationScript);
			if (IsValid(pIns))
			{
				DefaultModeRelationMap.Add(i->EntityFlagExt, pIns);
			}
		}
	}
}

void USpaceEntityRelationMgr::InitEntityRelationIns(FString RelationMode)
{
	InitDefaultEntityRelationIns();

	if (OldRelationMode == RelationMode) return;	///关系模式不变，则不重新加载关系实例
	OldRelationMode = RelationMode;

	///先清空关系实例
	CurrModeRelationMap.Empty();

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SPACE_ENTITY_RELATION);
	if (ConfigTable)
	{
		TArray<FSpaceEntityRelationTableData*> ConfigRows;
		ConfigTable->GetAllRows(ConfigRows);
		for (auto i : ConfigRows)
		{
			if (i->RelationMode != RelationMode) continue;
			URelationBase* pIns = URelationInsFactory::CreateRelationInsByClass(i->RelationScript);
			if (IsValid(pIns))
			{
				CurrModeRelationMap.Add(i->EntityFlagExt, pIns);
			}
		}
	}
}

COMBAT_RELATION USpaceEntityRelationMgr::GetCampRelation(int32 CampA, int32 CampB)
{
	if (CampA == 0 || CampB == 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
	}
	if (CampA == CampB)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	FString StrKey = FString::Printf(TEXT("%i_%i"), CampA, CampB);
	FString StrKey1 = FString::Printf(TEXT("%i_%i"), CampB, CampA);
	TMap<FString, COMBAT_RELATION> tMap = UUECS3GameInstance::Instance->ConstDataBP->CAMP_RELATION_MAP;
	for (auto it = tMap.CreateIterator(); it; ++it)
	{
		if (it.Key() == StrKey || it.Key() == StrKey1)
		{
			return it.Value();
		}
	}
	return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
}

COMBAT_RELATION USpaceEntityRelationMgr::GetFactionRelation(int32 FactionA, int32 FactionB)
{
	if (FactionA == 0 || FactionB == 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
	}
	if (FactionA == FactionB)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_FACTION_RELATION);
	if (ConfigTable)
	{
		TArray<FFACTION_RELATION_DATA*> ConfigRows;
		ConfigTable->GetAllRows(ConfigRows);
		for (auto i : ConfigRows)
		{
			if (i->FactionA == FactionA && i->FactionB == FactionB)
			{
				if (i->Relation == 0)
				{
					return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
				}else{
					return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
				}
			}
		}
	}
	return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
}

URelationBase* USpaceEntityRelationMgr::GetRelationIns(ENTITY_TYPE_EXT EntityFlagExt)
{
	if (CurrModeRelationMap.Num() == 0)
	{
		FString RelationMode = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_RELATION_MODE")));
		CS3_Warning(TEXT("RelationMode(%s) error! "), *RelationMode);
		return nullptr;
	}

	if (CurrModeRelationMap.Contains(EntityFlagExt))
	{
		return CurrModeRelationMap[EntityFlagExt];
	}
	else if (DefaultModeRelationMap.Contains(EntityFlagExt)) 	///当前模式下没有此entity的关系判断实例，则取通用模式下的实例
	{
		return DefaultModeRelationMap[EntityFlagExt];
	}
	else 
	{
		return nullptr;
	}
	
}

URelationBase* USpaceEntityRelationMgr::GetRelationInsByCls(FString RelClsStr)
{
	if (!RelationClsMap.Contains(RelClsStr))
	{
		URelationBase* pIns = URelationInsFactory::CreateRelationInsByClass(RelClsStr);
		if (IsValid(pIns))
		{
			RelationClsMap.Add(RelClsStr, pIns);
			return pIns;
		}
		else 
		{
			return nullptr;
		}
	}
	else 
	{
		return RelationClsMap[RelClsStr];
	}
}