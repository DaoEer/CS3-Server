

#include "MonsterExtInteractiveInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ShapeManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtInteractiveInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtInteractiveInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
UMonsterExtInteractiveInterface::UMonsterExtInteractiveInterface()
{
	
}

UMonsterExtInteractiveInterface::~UMonsterExtInteractiveInterface()
{
}

void UMonsterExtInteractiveInterface::AddInitiativeTrap_Implementation()
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return;
	}
	FVector shapeVector = FVector(Radius, Radius, Radius);
	pInitiativeShape = UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SHPERE, shapeVector, &UMonsterExtInteractiveInterface::OnPlayerBeginOverlap, &UMonsterExtInteractiveInterface::OnPlayerEndOverlap);
}



void UMonsterExtInteractiveInterface::OnPlayerBeginOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(MonsterActor);
}

void UMonsterExtInteractiveInterface::OnPlayerEndOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(MonsterActor);
}
void UMonsterExtInteractiveInterface::RPC_InteractiveWith()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCInterface::RPC_gossipWith : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("interactiveWith"), args);
}

void UMonsterExtInteractiveInterface::InitBlueCB()
{
	ArrBlueFunc.Add("AddInitiativeTrap");
	Supper::InitBlueCB();
}