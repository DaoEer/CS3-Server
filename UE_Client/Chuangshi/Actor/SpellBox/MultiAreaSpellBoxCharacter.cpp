
// Fill out your copyright notice in the Description page of Project Settings.


#include "MultiAreaSpellBoxCharacter.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Component/AppearanceComponent.h"
#include "Interface/Role/RoleTalkInterface.h"

AMultiAreaSpellBoxCharacter::AMultiAreaSpellBoxCharacter()
{
	CharacterClassName = TEXT("MultiAreaSpellBoxCharacter");
	InitBaseComponent();
}

void AMultiAreaSpellBoxCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

FString AMultiAreaSpellBoxCharacter::GetEntityUName()
{
	return UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityId, TEXT("uname"));
}

void AMultiAreaSpellBoxCharacter::RPC_requestRefreshAreaStatus()
{
	KBEngine::Entity* entity = GetSelfEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMultiAreaSpellBoxCharacter::RPC_requestRefreshAreaStatus : entity!"));
		return;
	}
	URoleTalkInterface * RoleTalkInterface = Cast<URoleTalkInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTalkInterface")));
	if (RoleTalkInterface)
	{
		RoleTalkInterface->CELL_RequestRefreshAreaStatus( entity->ID());
	}
	//KBEngine::Entity* PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity();
	//
	//if (PlayerEntity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:AMultiAreaSpellBoxCharacter::RPC_requestRefreshAreaStatus : PlayerEntity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;

	//args.Add(entity->ID());

	//PlayerEntity->CellCall(TEXT("CELL_RequestRefreshAreaStatus"), args);
}