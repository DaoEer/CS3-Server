
#include "MonsterExtClickAndInteractiveInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ShapeManager.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/Shape/BaseShape.h"
#include "CS3Base/CS3InterfaceDeclare.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtClickAndInteractiveInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_AddInteractiveRange, &UMonsterExtClickAndInteractiveInterface::CLIENT_AddInteractiveRange, const float&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtClickAndInteractiveInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void UMonsterExtClickAndInteractiveInterface::onLeaveWorld()
{
	Supper::onLeaveWorld();
	if (IsValid(pInitiativeShape))
	{
		pInitiativeShape->DestoryShape();
		pInitiativeShape = nullptr;
	}
}

void UMonsterExtClickAndInteractiveInterface::CLIENT_AddInteractiveRange(const float& Radius)
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return;
	}
	FVector shapeVector = FVector(Radius, Radius, Radius);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UShapeManager* ShapeManager = UUECS3GameInstance::Instance->ShapeManager;
		if (IsValid(ShapeManager))
		{
			pInitiativeShape = ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SHPERE, shapeVector, &UMonsterExtClickAndInteractiveInterface::OnPlayerBeginOverlap, &UMonsterExtClickAndInteractiveInterface::OnPlayerEndOverlap);
		}
	}
}

void UMonsterExtClickAndInteractiveInterface::OnPlayerBeginOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(MonsterActor);
}

void UMonsterExtClickAndInteractiveInterface::OnPlayerEndOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(MonsterActor);
}

void UMonsterExtClickAndInteractiveInterface::RPC_CELL_RequestInteraction()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCInterface::RPC_CELL_gossipWith : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_RequestInteraction"), args);
}