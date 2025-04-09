#include "CombatDamagerLoader.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Chuangshi.h"

CONTROL_COMPILE_OPTIMIZE_START

UCombatDamagerLoader::UCombatDamagerLoader()
{
	
}

UCombatDamagerLoader::~UCombatDamagerLoader()
{
	if (Instance != nullptr)
		Instance->RemoveFromRoot();
}

UCombatDamagerLoader * UCombatDamagerLoader::GetInstance()
{
	if (Instance == nullptr)
	{
		Instance = NewObject<UCombatDamagerLoader>();
		Instance->AddToRoot();
	}
	return Instance;
}

void UCombatDamagerLoader::loadAllData()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* CombatDamagerConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COMBAT_DAMAGER_DATA);
		if (!IsValid(CombatDamagerConfig)) return;
		TArray<FCOMBAT_DAMAGER_DATA*> CombatDamagerDatas;
		CombatDamagerConfig->GetAllRows(CombatDamagerDatas);
		for (auto CombatDamagerData : CombatDamagerDatas)
		{
			if (!CombatDamagerDataDic.Contains(CombatDamagerData->Level))
			{
				FCOMBAT_DAMAGER_DATA_PROFESSION Temps;
				CombatDamagerDataDic.Add(CombatDamagerData->Level, Temps);
			}
			FCOMBAT_DAMAGER_DATA Temp;
			Temp.Level = CombatDamagerData->Level;
			Temp.Profession = CombatDamagerData->Profession;
			Temp.DamRandom = CombatDamagerData->DamRandom;
			Temp.BCritPoint = CombatDamagerData->BCritPoint;
			Temp.BCritRatio = CombatDamagerData->BCritRatio;
			Temp.BParryPoint = CombatDamagerData->BParryPoint;
			Temp.BParryRatio = CombatDamagerData->BParryRatio;
			Temp.BArmorPoint = CombatDamagerData->BArmorPoint;
			Temp.GangQiArmorPoint = CombatDamagerData->GangQiArmorPoint;

			CombatDamagerDataDic[CombatDamagerData->Level].value.Add(Temp.Profession, Temp);
		}
	}
}

FCOMBAT_DAMAGER_DATA UCombatDamagerLoader::GetCombatDamagerData(int32 Level, int32 Profession)
{
	if (CombatDamagerDataDic.Contains(Level) && CombatDamagerDataDic[Level].value.Contains(Profession))
	{
		return CombatDamagerDataDic[Level].value[Profession];
	}
	return FCOMBAT_DAMAGER_DATA();
}

CONTROL_COMPILE_OPTIMIZE_END