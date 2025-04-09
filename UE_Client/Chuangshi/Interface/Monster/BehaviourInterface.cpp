// Fill out your copyright notice in the Description page of Project Settings.


#include "BehaviourInterface.h"

#include "Runtime/NavigationSystem/Public/NavigationSystem.h"
#include "Runtime/NavigationSystem/Public/NavigationPath.h"

#include "CSkillInterface.h"
#include "Interface/NPCAmbulantInterface.h"
#include "Util/GlobalFunctions.h"
#include "Actor/ServerCharacter.h"
#include "Interface/Monster/MonsterOptimizeInterface.h"
#include "Entity/Monster/MonsterOptimize.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UBehaviourInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD( BehClientSpell, &UBehaviourInterface::BehClientSpell, const int32&, const int32&, const uint8&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UBehaviourInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void UBehaviourInterface::BehClientSpell( const int32& skillID, const int32& targetID, const uint8& isGroupSkill )
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_OnPlayAdmissionAction : entity!"));
		return;
	}

	UCSkillInterface* skillInf = CS3::GetInterface< UCSkillInterface >(EntityID);
	int32 result = skillInf->useCSkillToEntity(skillID, targetID);
	if (result == (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		IsUsingSkill = true;
	}
	KBEngine::FVariantArray Args;
	Args.Add(skillID);
	Args.Add(targetID);
	Args.Add(isGroupSkill);
	Args.Add(result);
	entity->CellCall(TEXT("behClientSpellCB"), Args);
}

void UBehaviourInterface::BehClientSpellOver(const int32& skillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_OnPlayAdmissionAction : entity!"));
		return;
	}

	IsUsingSkill = false;
	KBEngine::FVariantArray Args;
	Args.Add(skillID);
	entity->CellCall(TEXT("behClientSpellOver"), Args);
}

bool UBehaviourInterface::GetIsUsingSkill()
{
	return IsUsingSkill;
}