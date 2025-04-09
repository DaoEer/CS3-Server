// Fill out your copyright notice in the Description page of Project Settings.

#include "PosSyncComponent.h"
#include "Actor/ServerCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RoleInterface.h"
#include "Manager/GameStatus.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"

UPosSyncComponent::UPosSyncComponent()
{
	//bWantsBeginPlay = false;
	PrimaryComponentTick.bCanEverTick = true;
}
KBEngine::Entity* UPosSyncComponent::GetMEntity()
{
	AServerCharacter* owner = Cast<AServerCharacter>(GetOwner());

	if (!IsValid(owner)) return nullptr;

	return owner->GetSelfEntity();
}
void UPosSyncComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------UPosSyncComponent::TickComponent--------------"));
		return;
	}

	if (GetMEntity())
	{
		AServerCharacter* MyCharacter = Cast<AServerCharacter>(GetOwner());;

		if (IsValid(MyCharacter))
		{
			APlayerCharacter* MyPlayCharacter = Cast<APlayerCharacter>(MyCharacter);
			if (IsValid(MyPlayCharacter) && MyPlayCharacter->ActorIsPlayer() && MyPlayCharacter->bUpdatePos)
				return;

			FVector ActorLocation = GetOwner()->GetActorLocation();
			//float CapsuleHalfHeight = (MyCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight());
			//ActorLocation.Z -= CapsuleHalfHeight;
			FVector ActorDirection = GetMEntity()->Direction();
			ActorDirection.Z = GetOwner()->GetActorRotation().Euler().Z;
			//每tick都把坐标同步到底层，以便底层能同步最新的位置信息到其它人身上
			float ModelScale = GetMEntity()->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
			float DisScale = ModelScale - 1.0;
			float DisHeight = DisScale * MyCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
			GetMEntity()->UpdateVolatileDataToServer(ActorLocation - FVector(0.0, 0.0, DisHeight), ActorDirection);
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UPosSyncComponent::TickComponent: ID=%d,  pos:%f,%f,%f"), MEntityID, ActorLocation.X, ActorLocation.Y, ActorLocation.Z);
	
			if (IsValid(MyPlayCharacter))
			{
				if (MyPlayCharacter->IsMoveing())
				{
					URoleInterface * RoleInterface = Cast<URoleInterface>(MyCharacter->GetEntityInterface_Cache().GameObjectInterface);
					float CurMoveDirection = MyPlayCharacter->CurMoveDirection;
					if (!FMath::IsNearlyEqual(OldBlendMoveDirection, CurMoveDirection))
					{
						RoleInterface->RequestBlendDir(CurMoveDirection);
						OldBlendMoveDirection = CurMoveDirection;
					}
					MyPlayCharacter->UpdateOtherCptPosition();
				}
				
			}
		}
	}
}

void UPosSyncComponent::setTickDoing( bool bDoing)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------setTickDoing--------------:%d"), bDoing);
	if (bDoing)
	{
		this->Activate();
		//PrimaryComponentTick.bCanEverTick = true;
	}
	else
	{
		this->Deactivate();
		//PrimaryComponentTick.bCanEverTick = false;
	}
}