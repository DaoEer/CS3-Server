// Fill out your copyright notice in the Description page of Project Settings.

#include "BuffEntityVisibleManager.h"
#include "Interface/SkillInterface.h"
#include"Chuangshi.h"
#include "Manager/CfgManager.h"
#include "Manager/VisibleManager.h"
#include "CS3Base/GameObject.h"
#include "Util/GolbalBPFunctionLibrary.h"

DECLARE_CYCLE_STAT(TEXT("UBuffEntityVisibleManager::UpdateAroundActor"), STAT_UpdateAroundActor, STATGROUP_BuffEntityVisibleManager);

UBuffEntityVisibleManager::UBuffEntityVisibleManager()
{

}

UBuffEntityVisibleManager::~UBuffEntityVisibleManager()
{

}

UBuffEntityVisibleManager* UBuffEntityVisibleManager::GetInstance()
{
	cs3_checkNoReentry();

	UBuffEntityVisibleManager* Instance = NewObject<UBuffEntityVisibleManager>();
	Instance->InitBuffVisibleTabel();

	return Instance;
}

void UBuffEntityVisibleManager::InitBuffVisibleTabel()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BUFF_ENTITY_VISIBLE);
	TArray<FName> RowNames = ConfigTable->GetRowNames();
	for (FName Name : RowNames)
	{
		FString ScriptID = Name.ToString();
		const FBEV_CFG_ROW_DATA* RowData = ConfigTable->GetRow<FBEV_CFG_ROW_DATA>(ScriptID);
		int32 vBuffID = RowData->VisibleBuffID;
		int32 ivBuffID = RowData->InvisibleBuffID;
		if (vBuffID)
		{
			BuffVisibleList.AddUnique(vBuffID);
		}
		if (ivBuffID)
		{
			BuffVisibleList.AddUnique(ivBuffID);
		}
		FBEV_CFG_ROW_DATA newRow;
		newRow.VisibleBuffID = RowData->VisibleBuffID;
		newRow.InvisibleBuffID = RowData->InvisibleBuffID;
		newRow.Priority = RowData->Priority;
		BuffVisibleDatas.Add(ScriptID, newRow);
	}
}

void UBuffEntityVisibleManager::OnAddBuff(int32 buffID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Add Buff"));
	UpdateAroundActor(buffID);
}

void UBuffEntityVisibleManager::OnRemoveBuff(int32 buffID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Remove Buff"));
	UpdateAroundActor(buffID);
}

VISIBLE_TYPE UBuffEntityVisibleManager::GetVisibleTypeByScriptID(const FString& ScriptID)
{
	if (BuffVisibleDatas.Contains(ScriptID))
	{
		auto BuffVisibleType = BuffVisibleDatas[ScriptID];
		FString Priority = BuffVisibleType.Priority;
		int32 visibleBuff = BuffVisibleType.VisibleBuffID;
		int32 inVisibleBuff = BuffVisibleType.InvisibleBuffID;
		USkillInterface* skillinterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? 
			UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
		if (!IsValid(skillinterface))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UBuffEntityVisibleManager::GetVisibleTypeByScriptID : skillinterface!"));
			return VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
		}
		if (!Priority.IsEmpty() && visibleBuff && inVisibleBuff)
		{
			TArray<FString> buffIDs = UGolbalBPFunctionLibrary::SplitString(Priority);
			if (buffIDs.Num()>0 && FSTRING_TO_INT(buffIDs[0]) == visibleBuff)
			{
				if (skillinterface->findBuffsByBuffID(visibleBuff).Num() >= 1)
				{
					return VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRUE;
				}

			}
			else
			{
				if (skillinterface->findBuffsByBuffID(inVisibleBuff).Num() >= 1)
				{
					return VISIBLE_TYPE::VISIBLE_TYPE_BUFF_FALSE;
				}
			}

		}
		if (skillinterface->findBuffsByBuffID(visibleBuff).Num() >= 1)
		{
			return VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRUE;
		}
		if (skillinterface->findBuffsByBuffID(inVisibleBuff).Num() >= 1)
		{
			return VISIBLE_TYPE::VISIBLE_TYPE_BUFF_FALSE;
		}

	}
	return VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
}

void UBuffEntityVisibleManager::UpdateAroundActor(int32 buffID)
{
	SCOPE_CYCLE_COUNTER(STAT_UpdateAroundActor);
	if (!BuffVisibleList.Contains(buffID))return;
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (KbeApp == nullptr || KbeApp->Entities() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBuffEntityVisibleManager::UpdateAroundActor : KbeApp||KbeApp->Entities()!"));
		return;
	}

	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* _Entity = Elem.Value;
		if (_Entity && _Entity->ClassName() != FString("Role") && _Entity->ClassName() != FString("VehiclePet"))
		{
			UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(_Entity->Actor());
		}
	}
}
