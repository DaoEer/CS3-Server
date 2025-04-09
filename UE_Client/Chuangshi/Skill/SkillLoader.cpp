#include "SkillLoader.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/Skill/SkillTableData.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Skill/Skill/CombatSkillClient.h"
#include "Skill/Skill/InstantSkillClient.h"
#include "Skill/Skill/SkillClientCharge.h"
#include "Skill/Skill/SkillClientJump.h"
#include "Skill/Skill/SkillClientSing.h"
#include "Chuangshi.h"

CONTROL_COMPILE_OPTIMIZE_START

USkillLoader::USkillLoader()
{
	
}

USkillLoader::~USkillLoader()
{
	
}

USkillLoader * USkillLoader::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<USkillLoader>();
}

void USkillLoader::loadAllSkill()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* SkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SKILL);
		TArray<FSKILL_TABLE_DATA*> SkillDatas;
		SkillConfig->GetAllRows(SkillDatas);
		for (auto RowName : SkillConfig->GetRowNames())
		{
			FString SkillId = FNAME_TO_FSTRING(RowName);
			const FSKILL_TABLE_DATA* SkillData = SkillConfig->GetRow<FSKILL_TABLE_DATA>(SkillId);
			USkill* skillInstance = CreateSkill(SkillId, SkillData);
			if (nullptr != skillInstance)
			{
				_skills.Add(FSTRING_TO_INT(SkillId), skillInstance);
			}
		}
		const UConfigTable* SkillConfigTest = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SKILL_TEST);
		TArray<FSKILL_TABLE_DATA*> SkillTestDatas;
		SkillConfigTest->GetAllRows(SkillTestDatas);
		for (auto RowName : SkillConfigTest->GetRowNames())
		{
			FString SkillId = FNAME_TO_FSTRING(RowName);
			const FSKILL_TABLE_DATA* SkillData = SkillConfigTest->GetRow<FSKILL_TABLE_DATA>(SkillId);
			USkill* skillInstance = CreateSkill(SkillId, SkillData);
			if (nullptr != skillInstance)
			{
				_skills.Add(FSTRING_TO_INT(SkillId), skillInstance);
			}
		}
	}
}

USkill * USkillLoader::CreateSkill(FString SkillID, const FSKILL_TABLE_DATA * SkillData)
{
	USkill* skillInstance = nullptr;
	if (SkillData->SkillType == ENUM_SKILL_CLASS_TYPE::CombatSkillClient)
	{
		UCombatSkillClient* Temp = NewObject<UCombatSkillClient>();
		Temp->init(SkillID, SkillData);
		skillInstance = (USkill*)Temp;
		skillInstance->AddToRoot();
	}
	else if (SkillData->SkillType == ENUM_SKILL_CLASS_TYPE::InstantSkillClient)
	{
		UInstantSkillClient* Temp = NewObject<UInstantSkillClient>();
		Temp->init(SkillID, SkillData);
		skillInstance = (USkill*)Temp;
		skillInstance->AddToRoot();
	}
	else if (SkillData->SkillType == ENUM_SKILL_CLASS_TYPE::SkillClientCharge)
	{
		USkillClientCharge* Temp = NewObject<USkillClientCharge>();
		Temp->init(SkillID, SkillData);
		skillInstance = (USkill*)Temp;
		skillInstance->AddToRoot();
	}
	else if (SkillData->SkillType == ENUM_SKILL_CLASS_TYPE::SkillClientJump)
	{
		USkillClientJump* Temp = NewObject<USkillClientJump>();
		Temp->init(SkillID, SkillData);
		skillInstance = (USkill*)Temp;
		skillInstance->AddToRoot();
	}
	else if (SkillData->SkillType == ENUM_SKILL_CLASS_TYPE::SkillClientSing)
	{
		USkillClientSing* Temp = NewObject<USkillClientSing>();
		Temp->init(SkillID, SkillData);
		skillInstance = (USkill*)Temp;
		skillInstance->AddToRoot();
	}
	return skillInstance;
}

USkill * USkillLoader::getSkillByID(int32 SkillID)
{
	if (_skills.Contains(SkillID))
	{
		return _skills[SkillID];
	}
	return nullptr;
}

CONTROL_COMPILE_OPTIMIZE_END