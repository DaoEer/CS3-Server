// Fill out your copyright notice in the Description page of Project Settings.

#include "CMonsterPosSyncComponent.h"
#include "Actor/ServerCharacter.h"
#include "Manager/GameStatus.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Navigation/PathFollowingComponent.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"
#include "Interface/Monster/MonsterInterface.h"
#include "Runtime\Engine\Classes\GameFramework\CharacterMovementComponent.h"
#include "Util/MoveScripts/MoveScriptRandomWalk.h"
#include "Util/MoveScripts/MoveScriptChaseActor.h"
#include "Components/CapsuleComponent.h"

CONTROL_COMPILE_OPTIMIZE_START
UCMonsterPosSyncComponent::UCMonsterPosSyncComponent()
{
	ResetMoveScript();
	PrimaryComponentTick.bCanEverTick = true;
}

UCMonsterPosSyncComponent::~UCMonsterPosSyncComponent() {
	ResetMoveScript();
}

KBEngine::Entity* UCMonsterPosSyncComponent::GetMEntity()
{
	AMonsterCharacter* owner = Cast<AMonsterCharacter>(GetOwner());

	if (!IsValid(owner)) return nullptr;

	return owner->GetSelfEntity();
}
void UCMonsterPosSyncComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (!IsValid(GetOwner()) || !IsValid(Cast<AMonsterCharacter>(GetOwner())) || Cast<AMonsterCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	if (Cast<AMonsterCharacter>(GetOwner())->IsState(ENTITY_STATE::EntityStateDead))return;

	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------UMonsterPosSyncComponent::TickComponent--------------"));
		return;
	}
	if (GetMEntity())
	{
		AMonsterCharacter* MyCharacter = Cast<AMonsterCharacter>(GetOwner());

		if (IsValid(MyCharacter))
		{
			FVector ActorLocation = MyCharacter->GetActorLocation();
			FVector ActorDirection = GetMEntity()->Direction();
			ActorDirection.Z = GetOwner()->GetActorRotation().Euler().Z;
			//每tick都把坐标同步到底层，以便底层能同步最新的位置信息到其它人身上
			float ModelScale = GetMEntity()->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
			float DisScale = ModelScale - 1.0;
			float DisHeight = DisScale * MyCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
			GetMEntity()->UpdateVolatileDataToServer(ActorLocation - FVector(0.0, 0.0, DisHeight), ActorDirection);
		}
		//检测移动是否结束
		if (!MoveScriptBasePtr)
		{
			return;
		}
		if (MoveScriptBasePtr->IsMoveOver()) {
			OnMoveOver();
		}
		else {
			MoveScriptBasePtr->MoveReachCheck();
		}

	}
}


void UCMonsterPosSyncComponent::StartRandomWalk(FVector OriginalPos, float RandomRange, float AcceptanceRadius) {
	ResetMoveScript();
	MoveScriptBasePtr = new(MoveScriptRandomWalk)(Cast<APawn>(GetOwner()), OriginalPos, RandomRange, AcceptanceRadius);
	MoveScriptBasePtr->DoMove();
}

void UCMonsterPosSyncComponent::ChaseActor(AActor* GoalActor, float AcceptanceRadius) {
	ResetMoveScript();
	MoveScriptBasePtr = new(MoveScriptChaseActor)(Cast<APawn>(GetOwner()), GoalActor, AcceptanceRadius);
	MoveScriptBasePtr->DoMove();
}

void UCMonsterPosSyncComponent::OnMoveOver() {

}

void UCMonsterPosSyncComponent::ResetMoveScript()
{
	if (MoveScriptBasePtr) {
		delete MoveScriptBasePtr;
		MoveScriptBasePtr = nullptr;
	}
}
CONTROL_COMPILE_OPTIMIZE_END
