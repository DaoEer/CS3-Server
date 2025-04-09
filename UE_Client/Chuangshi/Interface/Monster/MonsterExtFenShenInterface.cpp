// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtFenShenInterface.h"
#include "Util\GolbalBPFunctionLibrary.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtFenShenInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(BeginPosSyncServer, &UMonsterExtFenShenInterface::BeginPosSyncServer)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(EndPosSyncServer, &UMonsterExtFenShenInterface::EndPosSyncServer)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtFenShenInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtFenShenInterface::UMonsterExtFenShenInterface()
{
}

UMonsterExtFenShenInterface::~UMonsterExtFenShenInterface()
{

}

void UMonsterExtFenShenInterface::BeginPosSyncServer()
{
	AMonsterCharacter* monster = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(monster))
	{
		UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(monster->GetFilterComponent());
		if (Comp)
		{
			Comp->SetActiveComponentTick(false);
			Comp->ResetComponent();
		}

		UCharacterMovementComponent* moveComponent = Cast<UCharacterMovementComponent>(monster->GetMovementComponent());
		if (!IsValid(moveComponent))return;
		moveComponent->SetActive(true, true);
		moveComponent->SetMovementMode(EMovementMode::MOVE_Walking, 0);
		if (GetOwnerID() == UGolbalBPFunctionLibrary::GetPlayerID())
		{
			UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(UpdateVolHandle, this, &UMonsterExtFenShenInterface::UpdateVolatileDataToServer, 0.05f, true);
		}
	}
}

void UMonsterExtFenShenInterface::EndPosSyncServer()
{
	AMonsterCharacter* monster = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(monster))
	{
		UCharacterMovementComponent* moveComponent = Cast<UCharacterMovementComponent>(monster->GetMovementComponent());
		if (!IsValid(moveComponent))return;
		moveComponent->SetActive(false, true);
		UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(monster->GetFilterComponent());
		if (Comp)
		{
			Comp->SetActiveComponentTick(true);
			Comp->ResetComponent();
		}
		if (GetOwnerID() == UGolbalBPFunctionLibrary::GetPlayerID())
		{
			UpdateVolatileDataToServer();
			UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(UpdateVolHandle);
		}

		
	}
}

void UMonsterExtFenShenInterface::UpdateVolatileDataToServer()
{
	AMonsterCharacter* MyCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(MyCharacter))
	{
		FVector ActorLocation = MyCharacter->GetActorLocation();
		FVector ActorDirection = MyCharacter->GetActorRotation().Euler();
		//每tick都把坐标同步到底层，以便底层能同步最新的位置信息到其它人身上
		float ModelScale = GetEntity()->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
		float DisScale = ModelScale - 1.0;
		float DisHeight = DisScale * MyCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
		GetEntity()->UpdateVolatileDataToServer(ActorLocation - FVector(0.0, 0.0, DisHeight), ActorDirection);
		
	}
}
