// Fill out your copyright notice in the Description page of Project Settings.

#include "NPCBaseCharacter.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "Component/CollisionComponent.h"
#include "Components/CapsuleComponent.h"
#include "Util/CS3Debug.h"
#include "CS3Base/GameObject.h"

ANPCBaseCharacter::ANPCBaseCharacter()
{
	CharacterClassName = TEXT("NPCBaseCharacter");
}

void ANPCBaseCharacter::InitCharacterComponent()
{
	Super::InitCharacterComponent();
}

void ANPCBaseCharacter::UpdateCapsuleComponent()
{
	Super::UpdateCapsuleComponent();

}

int32 ANPCBaseCharacter::GetFinalfaction()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ANPCBaseCharacter::GetFinalfaction : Entity!"));
		return 0;
	}
	int8 tempCamp = Entity->GetDefinedProperty(TEXT("tempFaction")).GetValue<int8>();
	int8 camp = Entity->GetDefinedProperty(TEXT("faction")).GetValue<int8>();
	if (tempCamp != 0)
	{
		return (int32)tempCamp;
	}
	return (int32)camp;
}
