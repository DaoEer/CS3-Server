

#include "MonsterExtSFMJInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ShapeManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtSFMJInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtSFMJInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtSFMJInterface::UMonsterExtSFMJInterface()
{
}

UMonsterExtSFMJInterface::~UMonsterExtSFMJInterface()
{
}

void UMonsterExtSFMJInterface::AddInitiativeRange_Implementation()
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return;
	}
	FVector shapeVector = FVector(Radius, Radius, Radius);
	pInitiativeShape = UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SHPERE, shapeVector, &UMonsterExtSFMJInterface::OnPlayerBeginOverlap, &UMonsterExtSFMJInterface::OnPlayerEndOverlap);
}

void UMonsterExtSFMJInterface::OnPlayerBeginOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(MonsterActor);
}

void UMonsterExtSFMJInterface::OnPlayerEndOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(MonsterActor);
}

void UMonsterExtSFMJInterface::RPC_InteractionResults()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCInterface::RPC_InteractionResults : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("interactionResults"), args);
}

void UMonsterExtSFMJInterface::InitBlueCB()
{
	ArrBlueFunc.Add("AddInitiativeRange");
	Supper::InitBlueCB();
}