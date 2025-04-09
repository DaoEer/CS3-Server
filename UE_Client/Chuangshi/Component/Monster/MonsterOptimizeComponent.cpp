// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterOptimizeComponent.h"
#include "Util/GlobalFunctions.h"
#include "Util/CS3Debug.h"
#include "Manager/GameStatus.h"
#include "Components/CapsuleComponent.h"
#include "Actor/Monster/MonsterCharacter.h"


CONTROL_COMPILE_OPTIMIZE_START
UMonsterOptimizeComponent::UMonsterOptimizeComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}
UMonsterOptimizeComponent::~UMonsterOptimizeComponent()
{
}


void UMonsterOptimizeComponent::OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID)
{
	Supper::OnUpdateVolatileData(position, direction, parentID);
}

void UMonsterOptimizeComponent::OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID)
{
	Supper::OnUpdateVolatileDataByParent(position, direction, parentID);
}

void UMonsterOptimizeComponent::SetPosition(const FVector& position, int32 parentID)
{
	Supper::SetPosition(position, parentID); 
}

void UMonsterOptimizeComponent::SetDirection(const FVector& direction, int32 parentID)
{
	Supper::SetDirection(direction, parentID);
}

void UMonsterOptimizeComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------UMonsterPosSyncComponent::TickComponent--------------"));
		return;
	}

	AMonsterCharacter* MyCharacter = Cast<AMonsterCharacter>(GetOwner());
	if (IsValid(MyCharacter) && MyCharacter->GetSelfEntity())
	{
		KBEngine::Entity* myEntity = MyCharacter->GetSelfEntity();
		FVector ActorLocation = MyCharacter->GetActorLocation();
		FVector ActorDirection = myEntity->Direction();
		ActorDirection.Z = GetOwner()->GetActorRotation().Euler().Z;
		//每tick都把坐标同步到底层,虽然这是非control by怪物，但是这种类型的怪物服务器不给客户端同步数据
		//把当前位置同步给entity身上，主要防止别的模块做逻辑判断的时候出错
		float ModelScale = myEntity->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
		float DisScale = ModelScale - 1.0;
		float DisHeight = DisScale * MyCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
		myEntity->UpdateVolatileDataToServer(ActorLocation - FVector(0.0, 0.0, DisHeight), ActorDirection);
	}
}
CONTROL_COMPILE_OPTIMIZE_END