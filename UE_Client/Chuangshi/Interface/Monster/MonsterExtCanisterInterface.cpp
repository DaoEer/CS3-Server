// Fill out your copyright notice in the Description page of Project Settings.

#include "MonsterExtCanisterInterface.h"
#include "Manager/ShapeManager.h"
#include "../../Actor/Monster/MonsterCharacter.h"
#include "../../Actor/Player/PlayerCharacter.h"
#include "../../Util/GolbalBPFunctionLibrary.h"
#include "../../../../Plugins/KBEngine/Source/KBEngine/Public/ScriptModule.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtCanisterInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtCanisterInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtCanisterInterface::UMonsterExtCanisterInterface()
{

}

void UMonsterExtCanisterInterface::AddTrap()
{
	AActor* Monster = GetActor();
	if (!IsValid(Monster))
	{
		return;
	}
	UUECS3GameInstance::Instance->ShapeManager->CreateShape(Monster, this, SHAPE_TYPE::SHPERE, FVector(3, 3, 3), &UMonsterExtCanisterInterface::OnPlayerBeginOverlap, &UMonsterExtCanisterInterface::OnPlayerEndOverlap);
}

void UMonsterExtCanisterInterface::OnPlayerBeginOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(MonsterActor);
}

void UMonsterExtCanisterInterface::OnPlayerEndOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(MonsterActor);
}

void UMonsterExtCanisterInterface::OperationCanister(const int32& EntityID_)
{
	if (UGolbalBPFunctionLibrary::GetPlayerID() != EntityID_)return;

	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		entity_->CellCall(TEXT("CELL_operationCanister"), param);
	}
}

void UMonsterExtCanisterInterface::CLIENT_OnOperationCanister_Implementation(const int32& Ammo, float CdTime)
{

}

void UMonsterExtCanisterInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnOperationCanister");
	Supper::InitBlueCB();
}