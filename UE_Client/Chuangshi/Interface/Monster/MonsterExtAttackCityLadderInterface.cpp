// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtAttackCityLadderInterface.h"
#include "Manager/ShapeManager.h"
#include "../../GameDevelop/CS3GameInstance.h"
#include "../../Actor/Monster/MonsterCharacter.h"
#include "../../Util/GolbalBPFunctionLibrary.h"
#include "../../Actor/Player/PlayerCharacter.h"
#include "../../../../Plugins/KBEngine/Source/KBEngine/Public/ScriptModule.h"
#include "GameData/CharacterData.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "Components/PrimitiveComponent.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtAttackCityLadderInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtAttackCityLadderInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtAttackCityLadderInterface::UMonsterExtAttackCityLadderInterface()
{

}

void UMonsterExtAttackCityLadderInterface::AddTrap()
{
	AActor* Monster = GetActor();
	if (!IsValid(Monster))
	{
		return;
	}
	pShape = UUECS3GameInstance::Instance->ShapeManager->CreateShape(Monster, this, SHAPE_TYPE::SHPERE, FVector(10, 10, 10), &UMonsterExtAttackCityLadderInterface::OnPlayerBeginOverlap, &UMonsterExtAttackCityLadderInterface::OnPlayerEndOverlap);
}

void UMonsterExtAttackCityLadderInterface::OnPlayerBeginOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(MonsterActor);
}

void UMonsterExtAttackCityLadderInterface::OnPlayerEndOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(MonsterActor);
}

void UMonsterExtAttackCityLadderInterface::OperationLadder(const int32& EntityID_)
{
	if (UGolbalBPFunctionLibrary::GetPlayerID() != EntityID_)return;

	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		entity_->CellCall(TEXT("CELL_operationLadder"), param);
	}
}

void UMonsterExtAttackCityLadderInterface::CLIENT_CancelTrap_Implementation()
{
	if (IsValid(pShape))
	{
		pShape->DestoryShape();
		pShape = nullptr;
	}
}

void UMonsterExtAttackCityLadderInterface::CLIENT_LadderMoveFinish_Implementation(const FString& actionID)
{
	AMonsterCharacter* AtckCityLadderActor = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(AtckCityLadderActor))
	{
		//播放-放下梯踏板动作(现在已经不用播放动作了)
		AtckCityLadderActor->GetMesh()->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);//设置梯子与PAWN碰撞，才能生成导航绿色导航层
		AtckCityLadderActor->GetMesh()->SetCanEverAffectNavigation(true);//设置梯子是否影响关卡导航，生成绿色导航层
	}
}

void UMonsterExtAttackCityLadderInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_CancelTrap");
	ArrBlueFunc.Add("CLIENT_LadderMoveFinish");
	Supper::InitBlueCB();
}