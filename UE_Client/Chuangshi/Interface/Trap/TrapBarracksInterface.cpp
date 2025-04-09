// Fill out your copyright notice in the Description page of Project Settings.


#include "TrapBarracksInterface.h"
#include "../../GameDevelop/CS3GameInstance.h"
#include "../../Actor/Trap/TrapCharacter.h"
#include "../../Actor/Player/PlayerCharacter.h"
#include "../../Util/GolbalBPFunctionLibrary.h"
#include "Manager/ShapeManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UTrapBarracksInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTrapBarracksInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UTrapBarracksInterface::UTrapBarracksInterface()
{
}

UTrapBarracksInterface::~UTrapBarracksInterface()
{

}

void UTrapBarracksInterface::AddTrap()
{
	AActor* Monster = GetActor();
	if (!IsValid(Monster))
	{
		return;
	}
	UUECS3GameInstance::Instance->ShapeManager->CreateShape(Monster, this, SHAPE_TYPE::SHPERE, FVector(3, 3, 3), &UTrapBarracksInterface::OnPlayerBeginOverlap, &UTrapBarracksInterface::OnPlayerEndOverlap);
}

void UTrapBarracksInterface::OnPlayerBeginOverlap()
{
	ATrapCharacter* TrapActor = Cast<ATrapCharacter>(GetActor());
	if (!IsValid(TrapActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(TrapActor);
}

void UTrapBarracksInterface::OnPlayerEndOverlap()
{
	ATrapCharacter* TrapActor = Cast<ATrapCharacter>(GetActor());
	if (!IsValid(TrapActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(TrapActor);
	OnHideBarracksArmyWin();
}

void UTrapBarracksInterface::OpenBarracksArmyWin(const int32& EntityID_)
{
	if (UGolbalBPFunctionLibrary::GetPlayerID() != EntityID_)return;

	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		entity_->CellCall(TEXT("openBarracksArmyWin"), param);
	}
}
