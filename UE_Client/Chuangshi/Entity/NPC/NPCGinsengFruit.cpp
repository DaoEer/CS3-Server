// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCGinsengFruit.h"
#include "Interface/NPC/NPCGinsengFruitInterface.h"
#include "Actor/ServerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/NPCGinsengFruitInterface.h"


DEF_INTERFACE_BEGIN(NPCGinsengFruit, Supper)
DEF_INTERFACE(UNPCGinsengFruitInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCGinsengFruit, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCGinsengFruit, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCGinsengFruit::NPCGinsengFruit()
{
	_fActorName = FString("NPCGinsengFruit");
	//_fCompontentName = FName("UNPCActorComponent");
	isOnGround_ = false;
}

NPCGinsengFruit::~NPCGinsengFruit()
{

}

UClass* NPCGinsengFruit::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCGinsengFruit")); 
}

CONTROL_COMPILE_OPTIMIZE_END
