// Fill out your copyright notice in the Description page of Project Settings.

#include "PetPosSyncComponent.h"
#include "Actor/ServerCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/GameStatus.h"
#include "Actor/Pet/PetCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Components/CapsuleComponent.h"

UPetPosSyncComponent::UPetPosSyncComponent()
{
	//bWantsBeginPlay = false;
	PrimaryComponentTick.bCanEverTick = true;
}
KBEngine::Entity* UPetPosSyncComponent::GetMEntity()
{
	APetCharacter* owner = Cast<APetCharacter>(GetOwner());

	if (!IsValid(owner)) return nullptr;

	return owner->GetSelfEntity();
}
void UPetPosSyncComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (!IsValid(GetOwner()) || !IsValid(Cast<APetCharacter>(GetOwner())) || Cast<APetCharacter>(GetOwner())->GetSelfEntity() == nullptr) return;
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------UPetPosSyncComponent::TickComponent--------------"));
		return; 
	}
	if (KBEngine::Entity* PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity())
	{
		FString RideCarrierId = (FString)PlayerEntity->GetDefinedProperty(TEXT("carrierId"));
		if (!RideCarrierId.IsEmpty())
		{
			return;
		}
	}
	
	if (GetMEntity())
	{
		AServerCharacter* MyCharacter = Cast<AServerCharacter>(GetMEntity()->Actor());

		if (IsValid(MyCharacter))
		{
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
		}
	}
}